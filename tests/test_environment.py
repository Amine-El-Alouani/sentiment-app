"""Tests d'environnement du TP1 : Python, paquets, structure, .gitignore."""
import importlib
import sys
from pathlib import Path

import pytest

REQUIRED_DIRS = ["data", "models", "app", "ui", "tests", "scripts", "docs/cadrage"]
REQUIRED_FILES = ["README.md", "requirements.txt", ".gitignore", ".env.example"]


def test_python_version():
    assert sys.version_info[:2] >= (3, 10), "Python 3.11 attendu"


def test_virtualenv_active():
    assert sys.prefix != getattr(sys, "base_prefix", sys.prefix), (
        "pytest doit tourner dans le venv : source .venv/bin/activate"
    )


@pytest.mark.parametrize("module", ["pandas", "sklearn", "pytest"])
def test_core_package_importable(module):
    importlib.import_module(module)


@pytest.mark.parametrize("dirname", REQUIRED_DIRS)
def test_required_directory_exists(root: Path, dirname):
    assert (root / dirname).is_dir(), f"dossier manquant : {dirname}/"


@pytest.mark.parametrize("filename", REQUIRED_FILES)
def test_required_file_exists(root: Path, filename):
    assert (root / filename).is_file(), f"fichier manquant : {filename}"


def test_requirements_pins_versions(root: Path):
    lines = [l.strip() for l in (root / "requirements.txt").read_text().splitlines()]
    lines = [l for l in lines if l and not l.startswith("#")]
    assert lines, "requirements.txt est vide"
    for line in lines:
        assert "==" in line, f"version non figée : {line}"


@pytest.mark.parametrize("pattern", [".venv/", "__pycache__/", ".env", "models/", "mlruns/"])
def test_gitignore_contains(root: Path, pattern):
    content = (root / ".gitignore").read_text(encoding="utf-8")
    assert pattern in content, f".gitignore doit contenir {pattern}"


def test_no_real_env_file_committed(root: Path):
    """Un .env peut exister localement, mais il ne doit jamais être suivi par Git."""
    git_dir = root / ".git"
    if not git_dir.exists():
        pytest.skip("pas un dépôt Git")
    import subprocess

    tracked = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True).stdout.split()
    assert ".env" not in tracked, ".env est suivi par Git : git rm --cached .env"
    assert not any(p.startswith(".venv/") for p in tracked), ".venv/ est suivi par Git"
