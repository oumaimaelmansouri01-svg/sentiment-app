
"""TP4 — Tests aux limites et propriétés de l'API.

T22 : huit cas limites du contrat HTTP.
T23 : deux propriétés vérifiées avec Hypothesis.

Étiquettes possibles :
- POSITIVE
- NEGATIVE
- INDETERMINE
"""

import pytest
from fastapi.testclient import TestClient
from hypothesis import given, settings
from hypothesis import strategies as st

from api.main import app


@pytest.fixture
def client():
    """Démarrer l'API avec son modèle pour les tests paramétrés."""
    with TestClient(app) as test_client:
        yield test_client


# ---------------------------------------------------------
# T22 — Huit cas limites du contrat HTTP
# ---------------------------------------------------------

@pytest.mark.parametrize(
    "nom,contenu,statut_attendu",
    [
        ("texte-vide", {"text": ""}, 422),
        ("espaces", {"text": "   "}, 422),
        ("un-caractere", {"text": "a"}, 200),
        ("2000-caracteres", {"text": "a" * 2000}, 200),
        ("2001-caracteres", {"text": "a" * 2001}, 422),
        ("champ-absent", {}, 422),
        ("type-numerique", {"text": 123}, 422),
        ("contenu-non-json", "ceci n'est pas du JSON", 422),
    ],
)
def test_frontieres_du_contrat(
    client,
    nom,
    contenu,
    statut_attendu,
):
    """Vérifier les huit cas limites de POST /predict."""

    if nom == "contenu-non-json":
        reponse = client.post(
            "/predict",
            content=contenu,
            headers={"Content-Type": "application/json"},
        )
    else:
        reponse = client.post(
            "/predict",
            json=contenu,
        )

    assert reponse.status_code == statut_attendu, (
        f"{nom} : statut {reponse.status_code}, "
        f"attendu {statut_attendu}"
    )

    resultat = reponse.json()

    if statut_attendu == 200:
        assert resultat["label"] in (
            "POSITIVE",
            "NEGATIVE",
            "INDETERMINE",
        )
        assert isinstance(resultat["score"], (int, float))
        assert 0 <= resultat["score"] <= 1
        assert isinstance(resultat["text"], str)

    else:
        assert isinstance(resultat["detail"], list)


# ---------------------------------------------------------
# T23 — Propriété 1 : tout texte non blanc est accepté
# ---------------------------------------------------------

@given(
    texte=st.text(
        min_size=1,
        max_size=2000,
    ).filter(lambda valeur: bool(valeur.strip()))
)
@settings(
    max_examples=100,
    deadline=None,
)
def test_propriete_texte_valide(texte):
    """Tout texte valide doit produire une réponse HTTP 200."""

    # Client créé dans le test : aucune fixture partagée
    # entre les exemples générés par Hypothesis.
    with TestClient(app) as client:
        reponse = client.post(
            "/predict",
            json={"text": texte},
        )

    assert reponse.status_code == 200

    resultat = reponse.json()

    assert resultat["label"] in (
        "POSITIVE",
        "NEGATIVE",
        "INDETERMINE",
    )

    assert isinstance(resultat["score"], (int, float))
    assert 0 <= resultat["score"] <= 1

    assert resultat["text"] == texte[:100]


# ---------------------------------------------------------
# T23 — Propriété 2 : tout texte blanc est refusé
# ---------------------------------------------------------

@given(
    texte=st.text(
        alphabet=[" ", "\t", "\n", "\r"],
        min_size=1,
        max_size=2000,
    )
)
@settings(
    max_examples=100,
    deadline=None,
)
def test_propriete_texte_blanc_refuse(texte):
    """Tout texte composé uniquement de blancs doit être refusé."""

    with TestClient(app) as client:
        reponse = client.post(
            "/predict",
            json={"text": texte},
        )

    assert reponse.status_code == 422

    resultat = reponse.json()

    assert isinstance(resultat["detail"], list)
