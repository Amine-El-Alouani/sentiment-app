"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() du paquet (sentiment_app/predict.py), qui charge le modèle une seule fois.
"""
from typing import TypedDict

from api.schemas import Label

from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as _predict

# Choisi sur la courbe du seuil (python src/courbe_seuil.py) : voir docs/semaine4.md, partie 3
SEUIL_ABSTENTION = 0.60
# Étiquettes du modèle -> étiquettes du contrat : une correspondance explicite, vérifiée au démarrage
CORRESPONDANCE: dict[str, Label] = {"positive": "POSITIVE", "negative": "NEGATIVE"}


class Prediction(TypedDict):
    label: Label
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        modele = charger_modele()  # FileNotFoundError si le joblib manque : on ne démarre pas
        inconnues = {str(c) for c in modele.classes_} - set(CORRESPONDANCE)
        if inconnues:  # un modèle réentraîné sur d'autres étiquettes casserait le contrat
            raise ValueError(f"classes inconnues du contrat : {sorted(inconnues)}")

    def predict(self, text: str) -> Prediction:
        """Renvoie l'étiquette du contrat, ou INDETERMINE quand le modèle hésite."""
        r = _predict(text)
        label: Label = "INDETERMINE" if r["score"] < SEUIL_ABSTENTION else CORRESPONDANCE[r["label"]]
        return {"label": label, "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans sentiment_app/predict.py)."""
    return SentimentClassifier()
