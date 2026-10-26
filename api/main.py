"""API HTTP du modèle de sentiment."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, field_validator

from src.predict import charger_modele

RACINE = Path(__file__).resolve().parents[1]
SEUIL_INDETERMINE = 0.60


@asynccontextmanager
async def lifespan(application: FastAPI):
    modele = charger_modele()
    application.state.model = modele
    application.state.classifier = modele
    yield


app = FastAPI(
    title="API Sentiment",
    description="Classification des avis clients avec le modèle du TP2.",
    version="1.0.0",
    lifespan=lifespan,
)
app.state.model = charger_modele()
app.state.classifier = app.state.model


class PredictionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

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
def health(request: Request) -> dict[str, str]:
    if not _modele_disponible(request):
        raise HTTPException(status_code=503, detail="modèle non chargé")
    return {
        "status": "OK",
        "model": "tfidf-logreg (TP2, models/sentiment.joblib)",
    }


@app.post("/predict")
def predict_sentiment(request: Request, prediction: PredictionRequest) -> dict[str, str | float]:
    if not _modele_disponible(request):
        raise HTTPException(status_code=503, detail="modèle non chargé")
    try:
        model = request.app.state.model
        label = str(model.predict([prediction.text])[0]).upper()
        score = round(float(model.predict_proba([prediction.text]).max()), 4)
    except (RuntimeError, ValueError) as error:
        raise HTTPException(status_code=500, detail="erreur interne du modèle") from error
    if score < SEUIL_INDETERMINE:
        label = "INDETERMINE"
    return {
        "label": label,
        "score": score,
        "text": prediction.text,
    }


def _modele_disponible(request: Request) -> bool:
    """Les deux noms d'état sont conservés pour les contrats TP3 et TP5."""
    return (
        hasattr(request.app.state, "model")
        and hasattr(request.app.state, "classifier")
        and request.app.state.model is not None
        and request.app.state.classifier is not None
    )
