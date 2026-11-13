
"""Tests des fiches de cadrage du TP1.

Vérifie :
- La présence d'au moins trois fiches.
- La présence des rubriques obligatoires.
- Le remplissage des rubriques.
- La sélection d'une seule approche.
- La justification avec au moins deux critères.

Compatible avec Ruff et pytest.
"""

import re
from pathlib import Path

import pytest

REQUIRED_SECTIONS = [
    "Besoin en une phrase",
    "Utilisateur final",
    "Approche retenue",
    "Justification",
    "Données nécessaires",
    "Métrique de succès",
    "Conséquence d'une erreur",
    "Risques éthiques",
]

CRITERIA = ["(a)", "(b)", "(c)", "(d)"]


def fiches(cadrage_dir: Path) -> list[Path]:
    """Récupérer toutes les fiches de cadrage."""
    return sorted(cadrage_dir.glob("cas*.md"))


def section_body(text: str, title: str) -> str:
    """Extraire le contenu d'une rubrique Markdown."""
    pattern = re.compile(
        rf"^## {re.escape(title)}.*?$\n(.*?)(?=^## |\Z)",
        re.M | re.S,
    )

    match = pattern.search(text)

    return match.group(1).strip() if match else ""


def test_three_fiches_exist(cadrage_dir: Path):
    """Vérifier la présence d'au moins trois fiches."""
    assert len(fiches(cadrage_dir)) >= 3, (
        "Trois fiches cas*.md attendues dans docs/cadrage/"
    )


@pytest.mark.parametrize("title", REQUIRED_SECTIONS)
def test_sections_present_in_every_fiche(
    cadrage_dir: Path,
    title: str,
):
    """Vérifier que chaque fiche contient toutes les rubriques."""
    for fiche in fiches(cadrage_dir):
        contenu = fiche.read_text(encoding="utf-8")

        assert f"## {title}" in contenu, (
            f"{fiche.name} : rubrique '{title}' absente"
        )


def test_sections_are_filled(cadrage_dir: Path):
    """Vérifier que les rubriques contiennent du texte pertinent."""
    rubriques_vides = []

    for fiche in fiches(cadrage_dir):
        contenu = fiche.read_text(encoding="utf-8")

        for title in REQUIRED_SECTIONS:
            if title == "Approche retenue":
                continue

            body = section_body(contenu, title)

            # Ignorer les consignes et les cases à cocher.
            body = "\n".join(
                ligne
                for ligne in body.splitlines()
                if ligne.strip()
                and not ligne.startswith(">")
                and not ligne.startswith("- [")
            )

            if len(body) < 20:
                rubriques_vides.append(
                    f"{fiche.name} / {title}"
                )

    assert not rubriques_vides, (
        "Rubriques vides ou trop courtes : "
        + ", ".join(rubriques_vides)
    )


def test_exactly_one_approach_checked(cadrage_dir: Path):
    """Vérifier qu'une seule approche est cochée par fiche."""
    for fiche in fiches(cadrage_dir):
        contenu = fiche.read_text(encoding="utf-8")

        nombre_approches = contenu.count("- [x]")

        assert nombre_approches == 1, (
            f"{fiche.name} : cocher exactement une approche"
        )


def test_justification_cites_two_criteria(cadrage_dir: Path):
    """Vérifier que la justification cite au moins deux critères."""
    for fiche in fiches(cadrage_dir):
        contenu = fiche.read_text(encoding="utf-8")

        body = section_body(
            contenu,
            "Justification",
        )

        criteres_cites = [
            critere
            for critere in CRITERIA
            if critere in body
        ]

        assert len(criteres_cites) >= 2, (
            f"{fiche.name} : la justification doit citer "
            "au moins deux critères (a), (b), (c), (d)"
        )
