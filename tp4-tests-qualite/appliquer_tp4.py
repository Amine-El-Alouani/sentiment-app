#!/usr/bin/env python
"""Installe le kit TP4 (tests approfondis et qualité) dans un dépôt sentiment-app existant.

Usage, depuis ce dossier :
  python appliquer_tp4.py ../sentiment-app --simulation   # voir ce qui sera fait, sans rien écrire
  python appliquer_tp4.py ../sentiment-app

Prérequis : le TP3 (l'API FastAPI, dossier api/). N'écrase jamais un fichier existant :
pyproject.toml et .gitignore sont complétés, pas remplacés.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
A_COPIER = [
    "requirements-dev.txt", ".pre-commit-config.yaml",
    "src/courbe_seuil.py", "src/bilan_jeu_or.py",
    "tests/test_limites.py", "tests/test_integration.py", "tests/test_jeu_or.py",
    "data/jeu_or.csv", "docs/semaine4.md",
    "TP4-ENONCE.md", "MARCHE-A-SUIVRE-TP4.md",
]
LIGNES_GITIGNORE = [".hypothesis/", ".coverage", "htmlcov/", ".mypy_cache/", ".ruff_cache/",
                    "!data/jeu_or.csv"]


def sections_toml(texte: str) -> list[tuple[str, str]]:
    """Découpe un fichier TOML en (en-tête de section, bloc complet)."""
    blocs: list[tuple[str, str]] = []
    entete, lignes = "", []
    for ligne in texte.splitlines():
        if ligne.startswith("["):
            if entete:
                blocs.append((entete, "\n".join(lignes).rstrip() + "\n"))
            entete, lignes = ligne.strip(), [ligne]
        elif entete:
            lignes.append(ligne)
    if entete:
        blocs.append((entete, "\n".join(lignes).rstrip() + "\n"))
    return blocs


def completer_pyproject(depot: Path, simulation: bool) -> None:
    cible, modele = depot / "pyproject.toml", (KIT / "pyproject.toml").read_text(encoding="utf-8")
    if not cible.exists():
        print("  ajoute         pyproject.toml (configuration de ruff, mypy et de la couverture)")
        if not simulation:
            cible.write_text(modele, encoding="utf-8")
        return
    existant = cible.read_text(encoding="utf-8")
    presentes = {ligne.strip() for ligne in existant.splitlines() if ligne.startswith("[")}
    a_ajouter = [bloc for entete, bloc in sections_toml(modele) if entete not in presentes]
    deja = [entete for entete, _ in sections_toml(modele) if entete in presentes]
    for entete in deja:
        print(f"  conservé       pyproject.toml : {entete} existe déjà, vérifiez-le à la main")
    if a_ajouter:
        print(f"  complète       pyproject.toml : {len(a_ajouter)} section(s) ajoutée(s)")
        if not simulation:
            cible.write_text(existant.rstrip() + "\n\n# --- TP4 : outils de qualité ---\n"
                             + "\n".join(a_ajouter), encoding="utf-8")


def completer_gitignore(depot: Path, simulation: bool) -> None:
    gitignore = depot / ".gitignore"
    existant = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    manquantes = [ligne for ligne in LIGNES_GITIGNORE if ligne not in existant.splitlines()]
    if not manquantes:
        print("  déjà là        .gitignore")
        return
    print(f"  complète       .gitignore : {', '.join(manquantes)}")
    if not simulation:
        gitignore.write_text(existant.rstrip() + "\n\n# TP4\n" + "\n".join(manquantes) + "\n",
                             encoding="utf-8")


def verifier_jeu_or_suivi(depot: Path) -> None:
    """Le jeu d'or doit entrer dans Git, sinon la CI ne le verra jamais."""
    try:
        ignore = subprocess.run(["git", "check-ignore", "-q", "data/jeu_or.csv"], cwd=depot,
                                capture_output=True).returncode == 0
    except OSError:
        return
    if ignore:
        print("  ATTENTION      data/jeu_or.csv reste ignoré par Git : remplacez la ligne « data/ »"
              " de .gitignore par « data/* »")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("depot", help="chemin du dépôt sentiment-app")
    parser.add_argument("--simulation", action="store_true", help="n'écrit rien, affiche seulement")
    args = parser.parse_args()

    depot = Path(args.depot).expanduser().resolve()
    if not (depot / "README.md").is_file() or not (depot / "tests").is_dir():
        print(f"ERREUR : {depot} ne ressemble pas au dépôt du cours (README.md et tests/ attendus)")
        return 1
    if not (depot / "api" / "main.py").is_file():
        print("ERREUR : api/main.py absent. Faites d'abord le TP3 (l'API FastAPI) : le TP4 la teste.")
        return 1
    print(f"Dépôt cible : {depot}")

    for chemin in A_COPIER:
        src, dst = KIT / chemin, depot / chemin
        if not src.exists():
            print(f"  ABSENT DU KIT  {chemin}")
        elif dst.exists():
            print(f"  conservé       {chemin} (déjà présent, non écrasé)")
        else:
            print(f"  ajoute         {chemin}")
            if not args.simulation:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    completer_pyproject(depot, args.simulation)
    completer_gitignore(depot, args.simulation)
    if not args.simulation:
        verifier_jeu_or_suivi(depot)

    if args.simulation:
        print("\nSimulation : rien n'a été écrit.")
    else:
        print("\nKit installé. Suite, dans le dépôt : pip install -r requirements-dev.txt,"
              " puis MARCHE-A-SUIVRE-TP4.md, contrôle T21.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
