"""
text_cleaner.py
----------------
Cleans and normalizes raw resume text while preserving
important technical symbols like C++, C#, .NET, etc.
"""

import re

# Technical tokens that must NOT be stripped of their symbols
PROTECTED_TOKENS = [
    "c++", "c#", ".net", "node.js", "next.js", "vue.js",
    "asp.net", "d3.js", "three.js", "express.js"
]


def _protect_tokens(text: str) -> str:
    """Temporarily replace protected tokens with placeholders."""
    protected_map = {}
    for i, token in enumerate(PROTECTED_TOKENS):
        placeholder = f"__protected_{i}__"
        pattern = re.escape(token)
        if re.search(pattern, text, flags=re.IGNORECASE):
            protected_map[placeholder] = token
            text = re.sub(pattern, placeholder, text, flags=re.IGNORECASE)
    return text, protected_map


def _restore_tokens(text: str, protected_map: dict) -> str:
    for placeholder, token in protected_map.items():
        text = text.replace(placeholder, token)
    return text


def clean_text(raw_text: str) -> str:
    """
    Clean and normalize resume text.

    Steps:
    1. Protect important technical symbols (C++, C#, .NET, etc.)
    2. Lowercase the text
    3. Remove unwanted symbols / bullets while keeping protected tokens
    4. Collapse repeated whitespace
    """
    if not raw_text:
        return ""

    text = raw_text.strip()

    # Step 1: protect technical tokens before lowercasing/stripping symbols
    text, protected_map = _protect_tokens(text)

    # Step 2: lowercase
    text = text.lower()

    # Step 3: remove bullet characters and non-essential symbols
    # Keep letters, numbers, spaces, periods, plus signs, hashes, hyphens
    text = re.sub(r"[•●▪◦‣∙·]", " ", text)
    text = re.sub(r"[^a-z0-9\s\.\+\#\-\_/]", " ", text)

    # Step 4: collapse multiple spaces/newlines into one space
    text = re.sub(r"\s+", " ", text).strip()

    # Restore protected tokens (placeholders are lowercase-safe already)
    text = _restore_tokens(text, protected_map)

    return text


def split_into_lines(raw_text: str) -> list:
    """Split raw text into non-empty, stripped lines (useful for section detection)."""
    if not raw_text:
        return []
    lines = [line.strip() for line in raw_text.splitlines()]
    return [line for line in lines if line]


if __name__ == "__main__":
    sample = """
    SKILLS: Python, C++, Machine Learning!!
    Experience with Node.js && .NET   framework.
    """
    print(clean_text(sample))
