# src/predictor.py

from pathlib import Path
import joblib
import numpy as np

from .preprocessing import clean_text
from .validation import validate_description


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"


# Load trained artifacts
vectorizer = joblib.load(
    MODEL_DIR / "tfidf_vectorizer.joblib"
)

classifier = joblib.load(
    MODEL_DIR / "classifier.joblib"
)

hs_description_lookup = joblib.load(
    MODEL_DIR / "hs_description_lookup.joblib"
)


def get_top_predictions(
    description: str,
    top_k: int = 3
):
    """
    Return the top-k HS-code candidates ranked
    by Linear SVM decision score.

    decision_score is a ranking score, NOT a probability.
    """

    cleaned = clean_text(description)

    X = vectorizer.transform(
        [cleaned]
    )

    scores = classifier.decision_function(X)

    if scores.ndim > 1:
        scores = scores[0]

    indices = np.argsort(scores)[::-1][:top_k]

    predictions = []

    for index in indices:

        hs_code = str(
            classifier.classes_[index]
        )

        predictions.append({
            "hs_code": hs_code,
            "description": hs_description_lookup.get(
                hs_code,
                "Description unavailable"
            ),
            "decision_score": round(
                float(scores[index]),
                4
            )
        })

    return predictions


def classify_product(
    description: str,
    top_k: int = 3
):
    """
    Classify a product description into an HS code.
    """

    status, risk_flags = validate_description(
        description
    )

    if status in ("invalid", "manual_review"):

        return {
            "input": description,
            "status": status,
            "hs_code": None,
            "description": None,
            "risk_flags": risk_flags,
            "alternatives": []
        }

    candidates = get_top_predictions(
        description,
        top_k=top_k
    )

    best = candidates[0]

    return {
        "input": description,
        "status": status,
        "hs_code": best["hs_code"],
        "description": best["description"],
        "risk_flags": [],
        "alternatives": candidates[1:]
    }