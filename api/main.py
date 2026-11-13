
"""API REST du classificateur de sentiment.

Démarrage :
    python -m uvicorn api.main:app --reload
Documentation :
    http://localhost:8000/docs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.model import load_model
from api.schemas import HealthResponse, PredictRequest, PredictResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("sentiment_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charger le modèle avant de servir les requêtes."""
    logger.info("Démarrage de l'API...")

    app.state.classifier = load_model()

    logger.info(
        "Modèle chargé : %s",
        app.state.classifier.model_name,
    )

    yield

    logger.info("Arrêt de l'API")


app = FastAPI(
    title="Sentiment Analysis API",
    description="Classification de sentiments en français.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _classifier():
    """Obtenir le classificateur ou répondre 503."""
    clf = getattr(app.state, "classifier", None)

    if clf is None:
        raise HTTPException(
            status_code=503,
            detail="Modèle non chargé",
        )

    return clf


@app.get("/", summary="Accueil")
async def root():
    """Afficher les liens utiles de l'API."""
    return {
        "message": "Sentiment Analysis API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Santé de l'API",
)
async def health_check():
    """Répondre 200 si le modèle est chargé, sinon 503."""
    return {
        "status": "OK",
        "model": _classifier().model_name,
    }


@app.post(
    "/predict",
    response_model=PredictResponse,
    summary="Classifier un texte",
)
async def predict(request: PredictRequest):
    """Retourner POSITIVE, NEGATIVE ou INDETERMINE.

    422 : texte invalide, rejeté par Pydantic.
    503 : modèle indisponible.
    500 : erreur interne de prédiction.
    """
    clf = _classifier()

    try:
        result = clf.predict(request.text)

    except Exception as exc:
        logger.exception("Erreur lors de la prédiction")

        raise HTTPException(
            status_code=500,
            detail="Erreur interne du serveur",
        ) from exc

    logger.info(
        "predict: %r -> %s (%.2f)",
        request.text[:50],
        result["label"],
        result["score"],
    )

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
