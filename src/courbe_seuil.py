#!/usr/bin/env python
"""Courbe du seuil d'abstention, mesurée sur le jeu de test du TP2 (TP4, étape C).

Le modèle ne répond que si sa confiance atteint le seuil ; sinon l'avis part vers
un humain. Pour chaque seuil, on lit la part des avis auxquels il répond, et son
exactitude sur ces seuls avis.

Usage, depuis la racine du dépôt :
  python src/courbe_seuil.py              # jeu de démonstration
  python src/courbe_seuil.py --allocine   # jeu Allociné
Le modèle doit avoir été entraîné sur les mêmes données que la courbe.
"""
import argparse
import json
import sys
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train import GRAINE, METRIQUES, MODELE, charger  # noqa: E402  (même découpage que train.py)

SEUILS = [round(0.50 + 0.05 * i, 2) for i in range(10)]  # de 0,50 à 0,95


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allocine", action="store_true", help="courbe sur le jeu Allociné")
    args = parser.parse_args()

    if not MODELE.exists():
        raise SystemExit("Modèle absent : lancez d'abord python src/train.py")
    df, source = charger(args.allocine)
    if METRIQUES.exists():
        entraine_sur = str(json.loads(METRIQUES.read_text(encoding="utf-8")).get("source", "?"))
        if entraine_sur.lower()[:4] != str(source).lower()[:4]:
            print(f"ATTENTION : modèle entraîné sur « {entraine_sur} », courbe calculée sur « {source} ».")
            print("Réentraînez sur les mêmes données : sinon la courbe ne mesure pas votre modèle.\n")

    # Même découpage que l'entraînement : seul le jeu de test, jamais vu par le modèle, est mesuré
    _, X_test, _, y_test = train_test_split(
        df["review"], df["label"], test_size=0.2, random_state=GRAINE, stratify=df["label"]
    )
    pipeline = joblib.load(MODELE)
    probas = pipeline.predict_proba(X_test)
    confiance = probas.max(axis=1)
    justes = pipeline.classes_[probas.argmax(axis=1)] == y_test.to_numpy()
    n = len(y_test)

    print(f"Jeu de test : {n} avis ({source})\n")
    print(f"{'seuil':>6} {'répond à':>9} {'part':>6} {'exactitude':>11} {'erreurs':>8} {'vers un humain':>15}")
    for seuil in SEUILS:
        repond = confiance >= seuil
        k = int(repond.sum())
        exactitude = f"{justes[repond].mean():.3f}" if k else "-"
        erreurs = int((~justes[repond]).sum())
        print(f"{seuil:>6.2f} {k:>9d} {k / n:>6.0%} {exactitude:>11} {erreurs:>8d} {n - k:>15d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
