import streamlit as st
import os
import pandas as pd
from reviewer.ast_engine import ast_analysis
from reviewer.risk_engine import calculate_risk
from reviewer.diff_engine import generate_diff
from reviewer.fix_validator import validate_fix
from reviewer.static_reviewer import review_python_code
from collections import defaultdict
from reviewer.ollama_reviewer import review_with_ollama
from config import AI_REVIEW_API, AI_TIMEOUT
import requests


# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Offline Code Reviewer", 
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ Custom Styling ------------------
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .stCodeBlock { border-radius: 8px; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ------------------ Helpers ------------------
def count_severity(issues):
    summary = {"High": 0, "Medium": 0, "Low": 0}
    for issue in issues:
        summary[issue["severity"]] += 1
    return summary

def render_metric(label, value, color, border_color):
    st.markdown(
        f"""
        <div style="
            background-color: #161b22; 
            border: 1px solid {border_color}; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: left;">
            <p style="margin: 0; font-size: 14px; color: #8b949e;">{label}</p>
            <p style="margin: 0; font-size: 32px; font-weight: bold; color: {color};">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
def get_code_snippet(code, line_no, context=3):
    if line_no is None: return None
    lines = code.splitlines()
    start = max(line_no - context - 1, 0)
    end = min(line_no + context, len(lines))
    
    snippet = ""
    for i in range(start, end):
        prefix = "👉 " if i == line_no - 1 else "   "
        snippet += f"{prefix}{i+1}: {lines[i]}\n"
    return snippet

def call_ai_review(code: str):
    response = requests.post(
        f"{AI_REVIEW_API}/review",
        json={"code": code},
        timeout=AI_TIMEOUT
    )
    response.raise_for_status()
    return response.json()["review"]

# ------------------ Sidebar Settings ------------------
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2103/2103811.png",
        width=80
    )    
    st.title("Settings")
    st.info("This agent runs locally. AI review is optional.")
    st.divider()

    path = st.text_input("📁 Project Path", placeholder="/path/to/your/code")
    review_btn = st.button("🚀 Start Deep Review", use_container_width=True)

    st.divider()
    st.subheader("🤖 AI Review")

    use_remote_ai = st.checkbox(
        "Use GPU AI (Colab)",
        value=True,
        help="Uses CodeLlama"
    )




# ------------------ Main UI ------------------
st.title("🔍 CodeAuditAi")
st.markdown("---")

if review_btn:
    path = path.strip().strip('"').strip("'")

    if not os.path.exists(path):
        st.error("❌ **Invalid Path:** The directory or file does not exist.")
        st.stop()

    files = {}
    with st.status("🔍 Scanning directory for Python files...", expanded=True) as status:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                files[path] = f.read()
        else:
            for root, _, file_list in os.walk(path):
                for file in file_list:
                    if file.endswith(".py"):
                        full_path = os.path.join(root, file)
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            files[full_path] = f.read()
        status.update(label=f"✅ Found {len(files)} files. Analyzing...", state="complete")

    if not files:
        st.warning("⚠️ No Python files found in the specified path.")
        st.stop()

    os.makedirs("reports", exist_ok=True)
    report = "# 📄 Code Review Report\n\n"
    
    # Global metrics summary at the top
    total_issues = 0
    
    # ------------------ Review Loop ------------------
    for file_path, code in files.items():
        rel_path = os.path.relpath(file_path, path) if os.path.isdir(path) else file_path
        
        with st.container():
            st.markdown(f"### 📄 File: `{rel_path}`")
            static_issues = review_python_code(code)
            ast_issues = ast_analysis(code)

            issues = static_issues + ast_issues

            total_issues += len(issues)
            
            # ... inside the loop ...
            summary = count_severity(issues)
            
            
            m1, m2, m3, m4 = st.columns(4)

            with m1:
                render_metric(
                    label="🔴 High Risk", 
                    value=summary["High"], 
                    color="#ff4b4b",       
                    border_color="#3d1818" 
                )

            with m2:
                render_metric(
                    label="🟠 Medium Risk", 
                    value=summary["Medium"], 
                    color="#ffa500",       
                    border_color="#3d2c12" 
                )

            with m3:
                render_metric(
                    label="🟢 Low Risk", 
                    value=summary["Low"], 
                    color="#3dd56d",      
                    border_color="#123d1b"
                )

            with m4:
                render_metric(
                    label="📊 Total Issues", 
                    value=len(issues), 
                    color="#e6edf3",       
                    border_color="#30363d" 
                )
            
            
            st.markdown("<br>", unsafe_allow_html=True)

            # ... continue with your tabs (Summary, Detailed Issues, etc.) ...

            tab_summary, tab_details, tab_ai, tab_code = st.tabs(
                ["📊 Summary", "🛠️ Detailed Issues", "🤖 AI Review", "📝 Raw Code"]
            )

            with tab_summary:
                if not issues:
                    st.success("✨ **Clean Code!** No issues detected in this file.")
                else:
                    # Create a small dataframe for a quick look
                    df_issues = pd.DataFrame(issues)[["severity", "type", "line", "message"]]
                    st.table(df_issues)
                risk_score = calculate_risk(summary)

                st.metric("Project Risk Index", risk_score)


            with tab_details:
                grouped = defaultdict(list)
                for issue in issues:
                    grouped[issue["severity"]].append(issue)

                for sev in ["High", "Medium", "Low"]:
                    for idx, issue in enumerate(grouped[sev]):
                        color = "red" if sev == "High" else "orange" if sev == "Medium" else "blue"
                        with st.expander(f"**[{sev}]** {issue['type']} at Line {issue['line']}"):
                            st.markdown(f"**Message:** {issue['message']}")
                            
                            snippet = get_code_snippet(code, issue["line"])
                            if snippet:
                                st.code(snippet, language="python")
                            
                            if issue.get("fixed_code"):

                                if validate_fix(issue["fixed_code"]):

                                    diff = generate_diff(code, issue["fixed_code"])

                                    st.markdown("### Code Difference")
                                    st.code(diff)

            with tab_ai:
                st.info("🤖 AI review powered by GPU (Colab + Ollama)")

                try:
                    with st.spinner("Sending code to GPU AI server..."):
                        ai_review = call_ai_review(code)  # ✅ code is defined here

                    st.markdown(ai_review)

                except Exception as e:
                    st.error("❌ AI review failed")
                    st.code(str(e))
            with tab_code:
                st.code(code, language="python", line_numbers=True)

            st.divider()

    # Final Footer
    st.balloons()
    st.success(f"✅ Review complete! {total_issues} issues found across {len(files)} files.")
    st.title("Settings")
    st.info("This agent runs locally. AI review is optional.")
    st.divider()

    path = st.text_input("📁 Project Path", placeholder="/path/to/your/code")
    review_btn = st.button("🚀 Start Deep Review", use_container_width=True)

    st.divider()
    st.subheader("🤖 AI Review")

    use_remote_ai = st.checkbox(
        "Use GPU AI (Colab)",
        value=True,
        help="Uses CodeLlama"
    )




