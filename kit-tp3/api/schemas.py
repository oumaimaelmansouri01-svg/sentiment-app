
"""Contrats d'entrée et de sortie de l'API (Pydantic v2)."""

from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    """Requête de prédiction."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Texte à classifier",
        examples=["Livraison rapide, produit conforme, très satisfait"],
    )

    @field_validator("text")
    @classmethod
    def verifier_texte(cls, valeur: str) -> str:
        """Refuser un texte composé uniquement de blancs."""
        if not valeur.strip():
            raise ValueError("Le texte ne peut pas être vide")
        return valeur


class PredictResponse(BaseModel):
    """Réponse de prédiction."""

    label: str = Field(
        ...,
        description="POSITIVE ou NEGATIVE",
    )

    score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confiance de la classe prédite",
    )

    text: str = Field(
        ...,
        description="Aperçu du texte analysé (100 caractères)",
    )


class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé."""

    status: str = Field(
        ...,
        description="OK si le modèle est chargé",
    )

    model: str = Field(
        ...,
        description="Nom du modèle servi",
    )


class ErrorResponse(BaseModel):
    """Format des erreurs applicatives."""

    detail: str
