# src/validation.py

GENERIC_TERMS = {
    "goods",
    "good",
    "product",
    "products",
    "item",
    "items",
    "cargo",
    "machine",
    "machinery",
    "equipment",
    "parts",
    "part"
}


def validate_description(description: str) -> tuple[str, list[str]]:
    """
    Validate a cargo/product description before classification.
    Returns a tuple containing the status and a list of risk flags.
    """

    flags = []

    if description is None:
        return "invalid", ["Missing product description"]

    text = str(description).strip().lower()

    if not text:
        return "invalid", ["Missing product description"]

    words = text.split()

    if len(text) < 8:
        flags.append(
            "Description is very short"
        )

    if len(words) < 3:
        flags.append(
            "Description may be too general"
        )

    if text in GENERIC_TERMS:
        flags.append(
            "Description is too generic"
        )

    if flags:
        return "manual_review", flags

    return "classified", []