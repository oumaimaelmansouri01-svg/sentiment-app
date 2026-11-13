
"""Contrats d'entrée et de sortie de l'API (Pydantic v2).

TP4 — T27 : validation stricte et typage des réponses.
"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

SentimentLabel = Literal[
    "POSITIVE",
    "NEGATIVE",
    "INDETERMINE",
]


class PredictRequest(BaseModel):
    """Requête de classification d'un texte."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Texte à classifier (1 à 2000 caractères)",
        examples=[
            "Livraison rapide, produit conforme, très satisfait"
        ],
    )

    @field_validator("text")
    @classmethod
    def verifier_texte(cls, valeur: str) -> str:
        """Refuser les textes vides ou composés uniquement de blancs."""
        if not valeur.strip():
            raise ValueError(
                "Le texte ne peut pas être vide ou contenir uniquement des espaces"
            )

        return valeur


class PredictResponse(BaseModel):
    """Réponse de prédiction avec étiquette contrôlée."""

    label: SentimentLabel = Field(
        ...,
        description=(
            "POSITIVE, NEGATIVE ou INDETERMINE "
            "si la confiance est insuffisante"
        ),
    )

    score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Score de confiance de la prédiction (entre 0 et 1)",
    )

    text: str = Field(
        ...,
        description="Aperçu du texte analysé (100 caractères maximum)",
    )


class HealthResponse(BaseModel):
    """Réponse de vérification de l'état de l'API."""

    status: str = Field(
        ...,
        description="OK lorsque le modèle est chargé",
    )

    model: str = Field(
        ...,
        description="Nom du modèle de classification utilisé",
    )


class ErrorResponse(BaseModel):
    """Format des erreurs renvoyées par l'API."""

    detail: str
