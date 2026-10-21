#!/usr/bin/env python
"""Installe le kit TP3 (interface Streamlit) dans un dépôt sentiment-app existant.

Usage :
  python appliquer_tp3.py ../sentiment-app
  python appliquer_tp3.py ../sentiment-app --simulation
"""
import argparse
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
A_COPIER = [
    "ui/app.py", "ui/helpers.py",
    "tests/test_ui.py", "notebooks/TP3-colab-streamlit.ipynb",
    "TP3-ENONCE.md", "MARCHE-A-SUIVRE-TP3.md", "docs/compte-rendu-TEMPLATE.md", "ENONCE-COMPTE-RENDU.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("depot", help="chemin du dépôt sentiment-app")
    parser.add_argument("--simulation", action="store_true", help="n'écrit rien, affiche seulement")
    args = parser.parse_args()

    depot = Path(args.depot).expanduser().resolve()
    if not (depot / "README.md").is_file() or not (depot / "tests").is_dir():
        print(f"ERREUR : {depot} ne ressemble pas au dépôt du TP1 (README.md et tests/ attendus)")
        return 1
    if not (depot / "src" / "predict.py").is_file():
        print("ERREUR : src/predict.py absent. Faites d'abord le TP2 : le TP3 appelle sa fonction predict().")
        return 1
    print(f"Dépôt cible : {depot}")

    for chemin in A_COPIER:
        src, dst = KIT / chemin, depot / chemin
        if not src.exists():
            print(f"  ABSENT DU KIT  {chemin}")
            continue
        print(f"  {'remplace' if dst.exists() else 'ajoute  '}       {chemin}")
        if not args.simulation:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    print("\nSimulation : rien n'a été écrit." if args.simulation
          else "\nKit installé. Suite : streamlit run ui/app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
