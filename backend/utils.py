import re

def preprocess_text(text: str) -> str:
    """
    Clean the raw sentence.
    
    Steps:
    1. Lowercase the text.
    2. Remove punctuation.
    3. Collapse whitespace.
    
    Returns a single cleaned string (TF-IDF expects strings, not lists).
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    
    # Return as a joined string rather than a list of tokens
    return " ".join(text.split())