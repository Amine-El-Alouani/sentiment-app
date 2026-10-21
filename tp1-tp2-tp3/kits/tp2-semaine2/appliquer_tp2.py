#!/usr/bin/env python
"""Installe le kit TP2 dans un dépôt sentiment-app existant.

Usage :
  python appliquer_tp2.py ../sentiment-app
  python appliquer_tp2.py ../sentiment-app --simulation
"""
import argparse
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
A_COPIER = [
    "src/make_demo.py", "src/train.py", "src/evaluate.py", "src/predict.py",
    "tests/test_model.py", "notebooks/TP2-colab.ipynb",
    "TP2-ENONCE.md", "MARCHE-A-SUIVRE-TP2.md",
]
LIGNE_GITIGNORE = "!models/metrics.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("depot", help="chemin du dépôt sentiment-app")
    parser.add_argument("--simulation", action="store_true", help="n'écrit rien, affiche seulement")
    args = parser.parse_args()

    depot = Path(args.depot).expanduser().resolve()
    if not (depot / "README.md").is_file() or not (depot / "tests").is_dir():
        print(f"ERREUR : {depot} ne ressemble pas au dépôt du TP1 (README.md et tests/ attendus)")
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

    gitignore = depot / ".gitignore"
    if gitignore.is_file():
        contenu = gitignore.read_text(encoding="utf-8")
        if LIGNE_GITIGNORE in contenu:
            print(f"  déjà là        .gitignore : {LIGNE_GITIGNORE}")
        else:
            print(f"  ajoute         .gitignore : {LIGNE_GITIGNORE}")
            if not args.simulation:
                nouveau = contenu.replace("!models/.gitkeep\n", f"!models/.gitkeep\n{LIGNE_GITIGNORE}\n")
                if LIGNE_GITIGNORE not in nouveau:
                    nouveau = contenu + f"\n{LIGNE_GITIGNORE}\n"
                gitignore.write_text(nouveau, encoding="utf-8")
    else:
        print("  ATTENTION      .gitignore introuvable")

    print("\nSimulation : rien n'a été écrit." if args.simulation
          else "\nKit installé. Suite : lire MARCHE-A-SUIVRE-TP2.md, puis python src/make_demo.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
