import re
def sanitize_var(name: str) -> str:
    s = re.sub(r"[^\w]+", "_", name)
    return f"_{s}" if s and s[0].isdigit() else s