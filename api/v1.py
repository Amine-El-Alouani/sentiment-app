import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request

from api.model import Prediction, SentimentClassifier
from api.schemas import ErreurV1, HealthResponse, PredictRequest, PredictResponse
from api.securite import exiger

logger = logging.getLogger(__name__)
ERREURS: dict[int | str, dict[str, object]] = {
    code: {"model": ErreurV1} for code in (401, 403, 422, 500, 503)
}
router = APIRouter(prefix="/v1", tags=["v1"], responses=ERREURS)


def classifier(request: Request) -> SentimentClassifier:
    clf = getattr(request.app.state, "classifier", None)
    if clf is None:
        raise HTTPException(503, "Modèle non chargé")
    return clf


Classifier = Annotated[SentimentClassifier, Depends(classifier)]


@router.get("/health", response_model=HealthResponse)
def sante(clf: Classifier) -> dict[str, str]:
    return {"status": "OK", "model": clf.model_name}


@router.get("/modele", dependencies=[Depends(exiger("admin"))])
def modele(clf: Classifier) -> dict[str, object]:
    from api.main import SEUIL_INDETERMINE

    return {"model": clf.model_name, "seuil_abstention": SEUIL_INDETERMINE}


@router.post(
    "/predict",
    response_model=PredictResponse,
    dependencies=[Depends(exiger("client", "admin"))],
)
def predire(corps: PredictRequest, clf: Classifier) -> Prediction:
    try:
        return clf.predict(corps.text)
    except Exception:
        logger.exception("Erreur lors de la prédiction")
        raise HTTPException(500, "Erreur interne du serveur") from None
