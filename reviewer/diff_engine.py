import difflib

def generate_diff(original, fixed):

    diff = difflib.unified_diff(
        original.splitlines(),
        fixed.splitlines(),
        lineterm=""
    )

    return "\n".join(diff)
