
"""TP4 - Tests aux limites du contrat de l'API."""

import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "sentiment.joblib"
)

pytestmark = pytest.mark.skipif(
    not MODELE.exists(),
    reason="Modèle absent : python src/train.py",
)


@pytest.fixture(scope="module")
def client():
    from api.main import app
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c


def en_json(valeur: object) -> bytes:
    return json.dumps(valeur).encode("utf-8")


# B.1 - Huit cas limites
CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="espaces"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="mauvais-type"),
    pytest.param(b"pas du json", 422, id="json-invalide"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post(
        "/predict",
        content=corps,
        headers={"Content-Type": "application/json"},
    )

    assert reponse.status_code == code_attendu

    if code_attendu == 422:
        detail = reponse.json()["detail"]

        assert isinstance(detail, list)

        for erreur in detail:
            assert "loc" in erreur
            assert "msg" in erreur
            assert "type" in erreur


# B.5 - Propriété 1 : tout texte non vide est accepté
@given(
    texte=st.text(min_size=1, max_size=2000).filter(
        lambda t: bool(t.strip())
    )
)
@settings(max_examples=100, deadline=None)
def test_propriete_texte_valide(client, texte):
    reponse = client.post("/predict", json={"text": texte})

    assert reponse.status_code == 200

    resultat = reponse.json()

    assert resultat["label"] in ("POSITIVE", "NEGATIVE")
    assert 0 <= resultat["score"] <= 1


# B.5 - Propriété 2 : les blancs sont refusés
@given(
    texte=st.lists(
        st.sampled_from([" ", "\t", "\n", "\r", "\u00a0"]),
        min_size=1,
        max_size=2000,
    ).map("".join)
)
@settings(max_examples=100, deadline=None)
def test_propriete_espaces_refuses(client, texte):
    reponse = client.post("/predict", json={"text": texte})

    assert reponse.status_code == 422

    detail = reponse.json()["detail"]

    assert isinstance(detail, list)

    for erreur in detail:
        assert "loc" in erreur
        assert "msg" in erreur
        assert "type" in erreur
