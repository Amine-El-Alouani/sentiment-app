from typing import TypedDict

from api.schemas import Label
from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as predire_modele

SEUIL_ABSTENTION = 0.60
CORRESPONDANCE: dict[str, Label] = {"positive": "POSITIVE", "negative": "NEGATIVE"}


class Prediction(TypedDict):
    label: Label
    score: float
    text: str


class SentimentClassifier:
    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        modele = charger_modele()
        inconnues = {str(classe) for classe in modele.classes_} - set(CORRESPONDANCE)
        if inconnues:
            raise ValueError(f"classes inconnues du contrat : {sorted(inconnues)}")

    def predict(self, text: str) -> Prediction:
        resultat = predire_modele(text)
        label: Label = (
            "INDETERMINE"
            if resultat["score"] < SEUIL_ABSTENTION
            else CORRESPONDANCE[resultat["label"]]
        )
        return {"label": label, "score": resultat["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    return SentimentClassifier()
