
"""Tests d'environnement du TP1 : Python, paquets, structure, .gitignore."""

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

REQUIRED_DIRS = [
    "data",
    "models",
    "app",
    "ui",
    "tests",
    "scripts",
    "docs/cadrage",
]

REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    ".env.example",
]


def test_python_version():
    """Vérifier la version minimale de Python."""
    assert sys.version_info[:2] >= (3, 10), "Python 3.11 attendu"


def test_virtualenv_active():
    """Vérifier que les tests sont exécutés dans le venv."""
    assert sys.prefix != getattr(
        sys,
        "base_prefix",
        sys.prefix,
    ), "pytest doit tourner dans le venv : source .venv/bin/activate"


@pytest.mark.parametrize(
    "module",
    ["pandas", "sklearn", "pytest"],
)
def test_core_package_importable(module):
    """Vérifier la disponibilité des dépendances essentielles."""
    importlib.import_module(module)


@pytest.mark.parametrize(
    "dirname",
    REQUIRED_DIRS,
)
def test_required_directory_exists(root: Path, dirname):
    """Vérifier la structure du projet."""
    assert (root / dirname).is_dir(), (
        f"dossier manquant : {dirname}/"
    )


@pytest.mark.parametrize(
    "filename",
    REQUIRED_FILES,
)
def test_required_file_exists(root: Path, filename):
    """Vérifier la présence des fichiers obligatoires."""
    assert (root / filename).is_file(), (
        f"fichier manquant : {filename}"
    )


def test_requirements_pins_versions(root: Path):
    """Vérifier que les versions des dépendances sont figées."""
    requirements_path = root / "requirements.txt"

    lines = [
        ligne.strip()
        for ligne in requirements_path.read_text(
            encoding="utf-8"
        ).splitlines()
    ]

    lines = [
        ligne
        for ligne in lines
        if ligne and not ligne.startswith("#")
    ]

    assert lines, "requirements.txt est vide"

    for ligne in lines:
        assert "==" in ligne, (
            f"version non figée : {ligne}"
        )


@pytest.mark.parametrize(
    "pattern",
    [
        ".venv/",
        "__pycache__/",
        ".env",
        "models/",
        "mlruns/",
    ],
)
def test_gitignore_contains(root: Path, pattern):
    """Vérifier les exclusions obligatoires de Git."""
    content = (root / ".gitignore").read_text(
        encoding="utf-8"
    )

    assert pattern in content, (
        f".gitignore doit contenir {pattern}"
    )


def test_no_real_env_file_committed(root: Path):
    """Vérifier que les fichiers sensibles ne sont pas suivis par Git."""
    git_dir = root / ".git"

    if not git_dir.exists():
        pytest.skip("pas un dépôt Git")

    resultat = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )

    tracked = resultat.stdout.split()

    assert ".env" not in tracked, (
        ".env est suivi par Git : git rm --cached .env"
    )

    assert not any(
        chemin.startswith(".venv/")
        for chemin in tracked
    ), ".venv/ est suivi par Git"
