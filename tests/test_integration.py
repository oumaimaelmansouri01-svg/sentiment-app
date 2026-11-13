
"""Tests d'intégration de l'API — TP4, étape D."""

from importlib import import_module
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app

MODELE = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "sentiment.joblib"
)

pytestmark = pytest.mark.skipif(
    not MODELE.exists(),
    reason="Modèle absent : lancer python src/train.py",
)


def test_demarrage_reel_charge_le_modele():
    """D.1 : le lifespan charge le modèle au démarrage."""

    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "OK"
        assert "TP2" in response.json()["model"]


def test_modele_absent_empeche_demarrage(monkeypatch, tmp_path):
    """D.2 : absence du joblib = échec au démarrage."""

    module_predict = import_module("predict")

    chemin_inexistant = tmp_path / "modele_absent.joblib"

    monkeypatch.setattr(
        module_predict,
        "MODELE",
        chemin_inexistant,
    )

    module_predict.charger_modele.cache_clear()

    try:
        with pytest.raises(FileNotFoundError):
            with TestClient(app):
                pass

    finally:
        # Restaurer un état de cache sain pour les autres tests.
        module_predict.charger_modele.cache_clear()


def test_modele_non_charge_retourne_503(monkeypatch):
    """D.3 : /health et /predict retournent 503."""

    with TestClient(app) as client:
        monkeypatch.setattr(
            app.state,
            "classifier",
            None,
        )

        response_health = client.get("/health")

        response_predict = client.post(
            "/predict",
            json={"text": "Produit excellent"},
        )

        assert response_health.status_code == 503
        assert response_predict.status_code == 503

        assert response_health.json()["detail"] == (
            "Modèle non chargé"
        )

        assert response_predict.json()["detail"] == (
            "Modèle non chargé"
        )


@pytest.mark.parametrize(
    "erreur",
    [
        RuntimeError("panne interne du modèle"),
        ValueError("bug interne"),
    ],
)
def test_panne_modele_retourne_500(
    monkeypatch,
    erreur,
):
    """D.4 : cacher les détails des erreurs internes."""

    with TestClient(app) as client:

        def prediction_en_panne(_texte):
            raise erreur

        monkeypatch.setattr(
            app.state.classifier,
            "predict",
            prediction_en_panne,
        )

        response = client.post(
            "/predict",
            json={"text": "Produit excellent"},
        )

        assert response.status_code == 500

        assert response.json() == {
            "detail": "Erreur interne du serveur"
        }

        assert str(erreur) not in response.text
