#!/usr/bin/env python
"""Installe le kit TP5 (l'interface Streamlit) dans un dépôt sentiment-app existant.

Usage, depuis ce dossier :
  python appliquer_tp5.py ../sentiment-app --simulation   # voir ce qui sera fait, sans rien écrire
  python appliquer_tp5.py ../sentiment-app

Prérequis : le TP3 (l'API) et, de préférence, le TP4 (le verdict INDETERMINE). Le script copie
ui/, deux fichiers de tests, un fichier d'avis d'exemple et les documents du TP, sans rien écraser ;
il versionne l'exemple malgré « data/* », et ajoute Streamlit à l'installation de la CI.
"""
import argparse
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
A_COPIER = [
    "ui/__init__.py", "ui/client.py", "ui/app.py",
    "tests/test_client.py", "tests/test_interface.py",
    "data/avis_exemple.csv", "docs/semaine5.md",
    "TP5-ENONCE.md", "MARCHE-A-SUIVRE-TP5.md",
]
EXCEPTION = "!data/avis_exemple.csv"
PAQUET_CI = '"streamlit==1.39.*"'


def completer_gitignore(depot: Path, simulation: bool) -> None:
    gitignore = depot / ".gitignore"
    texte = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if EXCEPTION in texte.splitlines():
        print("  déjà là        .gitignore")
        return
    print(f"  complète       .gitignore : {EXCEPTION}")
    if not simulation:
        gitignore.write_text(texte.rstrip() + "\n\n# TP5\n" + EXCEPTION + "\n", encoding="utf-8")


def adapter_ci(depot: Path, simulation: bool) -> None:
    ci = depot / ".github" / "workflows" / "ci.yml"
    if not ci.is_file():
        print("  ATTENTION      ci.yml introuvable : ajoutez streamlit à l'installation de la CI")
        return
    lignes = ci.read_text(encoding="utf-8").splitlines()
    if any("streamlit" in ligne for ligne in lignes):
        print("  déjà là        .github/workflows/ci.yml : streamlit")
        return
    for i, ligne in enumerate(lignes):
        if "pip install" in ligne and "requirements" not in ligne:
            lignes[i] = ligne.rstrip() + " " + PAQUET_CI
            print("  complète       .github/workflows/ci.yml : installation de streamlit")
            if not simulation:
                ci.write_text("\n".join(lignes) + "\n", encoding="utf-8")
            return
    print("  déjà là        .github/workflows/ci.yml : la CI installe requirements.txt")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("depot", help="chemin du dépôt sentiment-app")
    parser.add_argument("--simulation", action="store_true", help="n'écrit rien, affiche seulement")
    args = parser.parse_args()

    depot = Path(args.depot).expanduser().resolve()
    if not (depot / "README.md").is_file() or not (depot / "tests").is_dir():
        print(f"ERREUR : {depot} ne ressemble pas au dépôt du cours (README.md et tests/ attendus)")
        return 1
    if not (depot / "api" / "main.py").is_file():
        print("ERREUR : api/main.py absent. Faites d'abord le TP3 (l'API) : l'interface l'appelle.")
        return 1
    contrat = (depot / "api" / "schemas.py").read_text(encoding="utf-8") if (depot / "api" / "schemas.py").exists() else ""
    if "INDETERMINE" not in contrat:
        print("ATTENTION : le TP4 n'est pas terminé (pas de verdict INDETERMINE dans api/schemas.py) :")
        print("            l'interface fonctionnera, mais deux tests du TP5 échoueront.")
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
    completer_gitignore(depot, args.simulation)
    adapter_ci(depot, args.simulation)

    print("\nSimulation : rien n'a été écrit." if args.simulation else
          "\nKit installé. Suite, dans le dépôt : python -m pytest -q, puis MARCHE-A-SUIVRE-TP5.md, contrôle T28.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
