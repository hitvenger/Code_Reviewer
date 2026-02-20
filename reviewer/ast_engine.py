import ast

def ast_analysis(code: str):
    issues = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            if isinstance(node, ast.Try):
                if not node.handlers:
                    issues.append({
                        "severity": "High",
                        "type": "Exception Handling",
                        "line": node.lineno,
                        "message": "Try block without exception handler"
                    })

            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id == "eval":
                    issues.append({
                        "severity": "High",
                        "type": "Security",
                        "line": node.lineno,
                        "message": "Dangerous use of eval()"
                    })

    except Exception:
        pass

    return issues
