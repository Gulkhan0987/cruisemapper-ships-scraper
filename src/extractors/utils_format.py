thonpython
def clean_text(text: str) -> str:
    if not text:
        return "N/A"
    return " ".join(text.split())