import ast
import os

def suggest_fix(issue_type, context=None):
    fixes = {
        "Best Practice": "Wrap executable code inside `if __name__ == '__main__':`.",
        "Resource Management": "Use `with open(path, 'r') as f:` so the file is closed automatically.",
        "Logic Risk": "Add a guard condition before division, e.g. `if len(nums) == 0: return 0`.",
        "Type Risk": "Use f-strings or explicit string conversion, e.g. `print(f'Average is {avg}')`.",
        "Code Smell": "Remove unused imports or variables to improve readability.",
        "Design Issue": "Reduce the number of parameters by grouping related values.",
        "Error Handling": "Avoid empty except blocks; log or re-raise the exception.",
        "Portability Issue": "Use `os.path.join()` instead of hardcoded paths."
    }

    return fixes.get(issue_type, "Refactor this section following Python best practices.")

def generate_fixed_snippet(issue_type):
    fixes = {
        "Logic Risk": """if len(nums) == 0:
    return 0
return total / len(nums)""",

        "Type Risk": """print(f"Average is {avg}")""",

        "Resource Management": """with open(path, "r") as f:
    data = f.read()""",
    }

    return fixes.get(issue_type)

def review_python_code(code: str):
    issues = []
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        issues.append({
            "line": e.lineno,
            "type": "Syntax Error",
            "severity": "High",
            "message": str(e),
            "fix": suggest_fix("Syntax Error")

        })
        return issues

    # Rule 1: Missing main guard
    if "__main__" not in code:
        issues.append({
            "line": None,
            "type": "Best Practice",
            "severity": "Medium",
            "message": "Missing `if __name__ == '__main__'` guard.",
            "fix": suggest_fix("Best Practice")

        })

    # Rule 2: open() without with
    if "open(" in code and "with open" not in code:
        issues.append({
            "line": None,
            "type": "Resource Management",
            "severity": "Medium",
            "message": "File opened without using `with` statement.",
            "fix": suggest_fix("Resource Management")

        })

    # Rule 3: Possible division by zero
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            issues.append({
                "line": node.lineno,
                "type": "Logic Risk",
                "severity": "High",
                "message": "Possible division by zero.",
                "fix": suggest_fix("Logic Risk"),
                "fixed_code": generate_fixed_snippet("Logic Risk")


            })

    # Rule 4: Print + string concat risk
    if "print(" in code and "+" in code:
        issues.append({
            "line": None,
            "type": "Type Risk",
            "severity": "High",
            "message": "Possible string and integer concatenation.",
            "fix": "Use f-strings: `print(f'Average is {avg}')`"
        })

    # Rule 5: Unused imports
    imports = set()
    used_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name)
        elif isinstance(node, ast.ImportFrom):
            for n in node.names:
                imports.add(n.name)
        elif isinstance(node, ast.Name):
            used_names.add(node.id)

    unused_imports = imports - used_names

    for imp in unused_imports:
        issues.append({
            "line": None,
            "type": "Code Smell",
            "severity": "Low",
            "message": f"Unused import detected: {imp}",
            "fix": suggest_fix("Code Smell")

        })
    
    # RULE 6: Too many parameters
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if len(node.args.args) > 5:
                issues.append({
                    "line": node.lineno,
                    "type": "Design Issue",
                    "severity": "Medium",
                    "message": f"Function `{node.name}` has too many parameters ({len(node.args.args)}).",
                    "fix": suggest_fix("Design Issue")
                })
    
    # Rule 7: Empty except block
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                if len(handler.body) == 0:
                    issues.append({
                        "line": handler.lineno,
                        "type": "Error Handling",
                        "severity": "High",
                        "message": "Empty except block detected. Errors are being silently ignored.",
                        "fix": suggest_fix("Error Handling")

                    })
    
    # Rule 8: Hardcoded paths
    if "/" in code or "\\" in code:
        issues.append({
            "line": None,
            "type": "Portability Issue",
            "severity": "Low",
            "message": "Hardcoded file path detected. Consider using os.path.",
            "fix": suggest_fix("Portability Issue")

        })

    return issues

    