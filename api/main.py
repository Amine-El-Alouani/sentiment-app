import os
from collections.abc import Mapping
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field, field_validator
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.model import load_model
from api.securite import charger_cles
from api.v1 import router as v1_router
from sentiment_app.predict import charger_modele

try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]
except ImportError:
    def load_dotenv() -> bool:
        return False

RACINE = Path(__file__).resolve().parents[1]
SEUIL_INDETERMINE = 0.60


@asynccontextmanager
async def lifespan(application: FastAPI):
    load_dotenv()
    charger_cles()
    application.state.model = charger_modele()
    application.state.classifier = load_model()
    yield


app = FastAPI(
    title="API Sentiment",
    description="Classification des avis clients avec le modèle du TP2.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:5500").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_router)
try:
    app.state.model = charger_modele()
    app.state.classifier = load_model()
except FileNotFoundError:
    app.state.model = None
    app.state.classifier = None


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


CODES = {
    400: "REQUETE_INVALIDE",
    401: "NON_AUTHENTIFIE",
    403: "ACCES_REFUSE",
    404: "INTROUVABLE",
    405: "METHODE_NON_AUTORISEE",
    422: "ENTREE_INVALIDE",
    500: "ERREUR_INTERNE",
    503: "MODELE_INDISPONIBLE",
}


def erreur_v1(
    statut: int,
    message: str,
    champs: list[dict[str, str]] | None = None,
    en_tetes: Mapping[str, str] | None = None,
) -> JSONResponse:
    corps = {
        "erreur": {
            "code": CODES.get(statut, f"HTTP_{statut}"),
            "message": message,
            "champs": champs or [],
        }
    }
    return JSONResponse(corps, status_code=statut, headers=en_tetes)


@app.exception_handler(StarletteHTTPException)
async def gerer_erreur_http(request: Request, exc: StarletteHTTPException) -> Response:
    if request.url.path.startswith("/v1"):
        return erreur_v1(exc.status_code, str(exc.detail), en_tetes=exc.headers)
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def gerer_erreur_validation(request: Request, exc: RequestValidationError) -> Response:
    if request.url.path.startswith("/v1"):
        champs = [
            {"champ": ".".join(str(element) for element in erreur["loc"]), "message": erreur["msg"]}
            for erreur in exc.errors()
        ]
        return erreur_v1(422, "Entrée refusée par le contrat de l'API", champs)
    return await request_validation_exception_handler(request, exc)


def _modele_disponible(request: Request) -> bool:
    """Les deux noms d'état sont conservés pour les contrats TP3 et TP5."""
    return (
        hasattr(request.app.state, "model")
        and hasattr(request.app.state, "classifier")
        and request.app.state.model is not None
        and request.app.state.classifier is not None
    )
