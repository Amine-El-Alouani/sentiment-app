#!/usr/bin/env python
"""Diagnostic de l'environnement du TP1.

Usage : python scripts/check_setup.py
Affiche une ligne par vérification (OK / ATTENTION / ERREUR) et un code de sortie
non nul si une vérification bloquante échoue. Les mêmes vérifications existent
sous forme de tests dans tests/test_environment.py.
"""
from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRS = ["data", "models", "app", "ui", "tests", "scripts", "docs/cadrage"]
REQUIRED_FILES = ["README.md", "requirements.txt", ".gitignore"]
CORE_PACKAGES = {"pandas": "pandas", "sklearn": "scikit-learn", "pytest": "pytest"}
GITIGNORE_MUST_CONTAIN = [".venv/", "__pycache__/", ".env", "models/", "mlruns/"]
MIN_AUTHORS = 2  # un binôme : deux auteurs de commits

errors = 0
warnings = 0


def ok(msg: str) -> None:
    print(f"  OK         {msg}")


def warn(msg: str) -> None:
    global warnings
    warnings += 1
    print(f"  ATTENTION  {msg}")


def err(msg: str) -> None:
    global errors
    errors += 1
    print(f"  ERREUR     {msg}")


def check_python() -> None:
    print("Python")
    v = sys.version_info
    if (v.major, v.minor) == (3, 11):
        ok(f"version {v.major}.{v.minor}.{v.micro}")
    elif v.major == 3 and v.minor >= 10:
        warn(f"version {v.major}.{v.minor} : le cours cible 3.11, ça devrait fonctionner")
    else:
        err(f"version {v.major}.{v.minor} : installer Python 3.11")
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    if in_venv:
        ok(f"environnement virtuel actif ({sys.prefix})")
    else:
        err("aucun environnement virtuel actif : source .venv/bin/activate")


def check_packages() -> None:
    print("Paquets")
    for module, pip_name in CORE_PACKAGES.items():
        try:
            m = importlib.import_module(module)
            ok(f"{pip_name} {getattr(m, '__version__', '')}")
        except ImportError:
            err(f"{pip_name} absent : pip install -r requirements.txt")


def check_structure() -> None:
    print("Structure du dépôt")
    for d in REQUIRED_DIRS:
        (ok if (ROOT / d).is_dir() else err)(f"dossier {d}/")
    for f in REQUIRED_FILES:
        (ok if (ROOT / f).is_file() else err)(f"fichier {f}")
    gi = ROOT / ".gitignore"
    if gi.is_file():
        content = gi.read_text(encoding="utf-8")
        for pattern in GITIGNORE_MUST_CONTAIN:
            (ok if pattern in content else warn)(f".gitignore contient {pattern}")


def check_git() -> None:
    print("Git")
    if shutil.which("git") is None:
        err("git introuvable dans le PATH")
        return
    if not (ROOT / ".git").exists():
        err("ce dossier n'est pas un dépôt Git : git init ou git clone")
        return
    ok("dépôt Git détecté")
    try:
        out = subprocess.run(
            ["git", "shortlog", "-sn", "--all"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except subprocess.CalledProcessError:
        warn("aucun commit encore")
        return
    authors = [line.split("\t", 1)[1] for line in out.splitlines() if "\t" in line]
    if len(authors) >= MIN_AUTHORS:
        ok(f"{len(authors)} auteurs de commits : {', '.join(authors)}")
    elif authors:
        warn(f"{len(authors)} auteur(s) seulement : les deux membres doivent pousser un commit")
    else:
        warn("aucun commit encore")
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout
    if ".venv/" in tracked or "\n.venv" in tracked:
        err(".venv/ est suivi par Git : git rm -r --cached .venv")
    else:
        ok(".venv/ n'est pas suivi par Git")


def check_cadrage() -> None:
    print("Fiches de cadrage")
    folder = ROOT / "docs" / "cadrage"
    fiches = [p for p in folder.glob("cas*.md")]
    if len(fiches) >= 3:
        ok(f"{len(fiches)} fiches trouvées")
    else:
        warn(f"{len(fiches)} fiche(s) cas*.md, 3 attendues")
    for p in sorted(fiches):
        text = p.read_text(encoding="utf-8")
        checked = text.count("- [x]")
        if checked == 1:
            ok(f"{p.name} : une approche cochée")
        else:
            warn(f"{p.name} : {checked} approche(s) cochée(s), une seule attendue")


def main() -> int:
    print(f"Diagnostic TP1 dans {ROOT}\n")
    check_python()
    check_packages()
    check_structure()
    check_git()
    check_cadrage()
    print(f"\nRésultat : {errors} erreur(s), {warnings} avertissement(s)")
    if errors:
        print("Corriger les erreurs avant de pousser.")
    elif warnings:
        print("Environnement utilisable ; traiter les avertissements avant la fin du TP.")
    else:
        print("Tout est en place.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
