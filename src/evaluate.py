#!/usr/bin/env python
"""Évalue le modèle sauvegardé et affiche la matrice de confusion.

Usage :
  python src/evaluate.py             # sur le jeu de démonstration
  python src/evaluate.py --allocine  # sur le jeu Allociné
"""
import argparse
import sys
from pathlib import Path

import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent))   # pour lancer depuis la racine
from train import GRAINE, MODELE, charger  # mêmes constantes que l'entraînement

RACINE = Path(__file__).resolve().parents[1]
ETIQUETTES = ["negative", "positive"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allocine", action="store_true")
    args = parser.parse_args()

    if not MODELE.exists():
        raise SystemExit("Modèle absent : lancez d'abord python src/train.py")
    pipeline = joblib.load(MODELE)

    df, source = charger(args.allocine)
    # Même découpage que l'entraînement : même graine, mêmes proportions
    _, X_test, _, y_test = train_test_split(
        df["review"], df["label"], test_size=0.2, random_state=GRAINE, stratify=df["label"]
    )
    y_pred = pipeline.predict(X_test)

    print(f"Évaluation sur {len(X_test)} avis ({source})\n")
    print(classification_report(y_test, y_pred, digits=3, zero_division=0))
    mc = confusion_matrix(y_test, y_pred, labels=ETIQUETTES)
    print("Matrice de confusion (lignes = vérité, colonnes = prédiction)")
    print(f"{'':>10}{ETIQUETTES[0]:>10}{ETIQUETTES[1]:>10}")
    for nom, ligne in zip(ETIQUETTES, mc, strict=True):
        print(f"{nom:>10}{ligne[0]:>10}{ligne[1]:>10}")

    faux_negatifs = mc[1][0]
    faux_positifs = mc[0][1]
    print(f"\n{faux_positifs} négatifs classés positifs, {faux_negatifs} positifs classés négatifs")

    # Trois erreurs à lire, pour comprendre ce que le sac de mots ne voit pas
    erreurs = [(t, v, p) for t, v, p in zip(X_test, y_test, y_pred, strict=True) if v != p]
    print(f"\n{len(erreurs)} erreurs au total. Trois exemples :")
    for texte, vrai, predit in erreurs[:3]:
        print(f"  vérité={vrai:9s} prédit={predit:9s} | {texte[:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
