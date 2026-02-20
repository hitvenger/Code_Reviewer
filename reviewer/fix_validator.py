def validate_fix(code: str):
    try:
        compile(code, "<string>", "exec")
        return True
    except:
        return False
