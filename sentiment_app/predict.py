#!/usr/bin/env python
"""Prédiction unitaire : la fonction que l'API de la semaine 3 appellera.

Usage :
  python src/predict.py "Livraison rapide, très satisfait"
  >>> from predict import predict ; predict("texte")
"""
import os
import sys
from functools import lru_cache
from pathlib import Path

import joblib

RACINE = Path(__file__).resolve().parents[1]


def chemin_modele() -> Path:
    configure = os.environ.get("SENTIMENT_MODELE")
    if configure:
        return Path(configure)
    depot = RACINE / "models" / "sentiment.joblib"
    if depot.exists():
        return depot
    return Path(__file__).with_name("modele") / "sentiment.joblib"


MODELE = chemin_modele()


@lru_cache(maxsize=1)
def charger_modele():
    """Chargé une seule fois par processus, pas à chaque appel."""
    if not MODELE.exists():
        raise FileNotFoundError(
            f"modèle introuvable : {MODELE}. Lancez python src/train.py, "
            "ou indiquez son chemin dans la variable SENTIMENT_MODELE"
        )
    return joblib.load(MODELE)


def predict(texte: str) -> dict:
    """Renvoie {'label': 'positive'|'negative', 'score': float}."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": etiquette, "score": round(score, 4)}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
