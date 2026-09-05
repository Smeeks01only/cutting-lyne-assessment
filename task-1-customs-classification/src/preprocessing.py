# src/preprocessing.py

import re


def clean_text(text: str) -> str:
    """
    Clean a product description before classification.
    """

    if text is None:
        return ""

    text = str(text).lower()

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Replace punctuation with spaces
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text