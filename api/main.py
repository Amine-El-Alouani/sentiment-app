"""API HTTP du modèle de sentiment."""
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

from src.predict import predict

RACINE = Path(__file__).resolve().parents[1]
SEUIL_INDETERMINE = 0.60

app = FastAPI(
    title="API Sentiment",
    description="Classification des avis clients avec le modèle du TP2.",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_non_vide(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("texte vide")
        return value


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "API de sentiment", "docs": "/docs"}


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "OK",
        "model": "tfidf-logreg (TP2, models/sentiment.joblib)",
    }


@app.post("/predict")
def predict_sentiment(request: PredictionRequest) -> dict[str, str | float]:
    result = predict(request.text)
    label = result["label"].upper()
    if result["score"] < SEUIL_INDETERMINE:
        label = "INDETERMINE"
    return {
        "label": label,
        "score": result["score"],
        "text": request.text,
    }
