
"""Raccord entre l'API et le modèle entraîné au TP2."""

import sys
from pathlib import Path
from typing import Literal, TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from predict import charger_modele  # noqa: E402
from predict import predict as _predict  # noqa: E402

SEUIL_ABSTENTION = 0.60

SentimentLabel = Literal[
    "POSITIVE",
    "NEGATIVE",
    "INDETERMINE",
]


class PredictionResult(TypedDict):
    """Structure de la réponse du classificateur."""

    label: SentimentLabel
    score: float
    text: str


CORRESPONDANCE: dict[str, SentimentLabel] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}

CLASSES_ATTENDUES = {"positive", "negative"}


class SentimentClassifier:
    """Enveloppe du modèle avec un contrat typé."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        """Charger et vérifier les classes du modèle."""
        modele = charger_modele()

        classes = set(modele.classes_)

        if classes != CLASSES_ATTENDUES:
            raise ValueError(
                f"Classes inattendues dans le modèle : {classes}"
            )

    def predict(self, text: str) -> PredictionResult:
        """Prédire le sentiment avec abstention si nécessaire."""
        resultat = _predict(text)

        etiquette = str(resultat["label"])
        score = float(resultat["score"])

        if etiquette not in CORRESPONDANCE:
            raise ValueError("Étiquette de prédiction inconnue")

        label: SentimentLabel = CORRESPONDANCE[etiquette]

        if score < SEUIL_ABSTENTION:
            label = "INDETERMINE"

        return {
            "label": label,
            "score": score,
            "text": text[:100],
        }


def load_model() -> SentimentClassifier:
    """Construire le classificateur utilisé par l'API."""
    return SentimentClassifier()
