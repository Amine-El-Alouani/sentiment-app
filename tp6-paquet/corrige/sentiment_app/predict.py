#!/usr/bin/env python
"""Prédiction unitaire (TP2), entrée dans le paquet au TP6.

Usage :
  sentiment predict "Livraison rapide, très satisfait"      la commande du paquet (TP6)
  python src/predict.py "Livraison rapide, très satisfait"  toujours valable
  >>> from sentiment_app.predict import predict ; predict("texte")

Le modèle n'est pas dans le paquet : la variable d'environnement SENTIMENT_MODELE indique son
chemin ; sans elle, c'est models/sentiment.joblib à la racine du dépôt.
"""
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import TypedDict

import joblib

RACINE = Path(__file__).resolve().parents[1]


def chemin_modele() -> Path:
    """SENTIMENT_MODELE si elle est définie, sinon le modèle entraîné dans le dépôt."""
    return Path(os.environ.get("SENTIMENT_MODELE") or RACINE / "models" / "sentiment.joblib")


MODELE = chemin_modele()


class Resultat(TypedDict):
    """Ce que predict() renvoie : un type précis, que mypy peut suivre (TP4, étape E)."""

    label: str
    score: float


@lru_cache(maxsize=1)
def charger_modele():
    """Chargé une seule fois par processus, pas à chaque appel."""
    if not MODELE.exists():
        raise FileNotFoundError(
            f"modèle introuvable : {MODELE}. Lancez python src/train.py, "
            "ou indiquez son chemin dans la variable SENTIMENT_MODELE"
        )
    return joblib.load(MODELE)


def predict(texte: str) -> Resultat:
    """Renvoie {'label': 'positive'|'negative', 'score': float}."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": str(etiquette), "score": round(score, 4)}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
