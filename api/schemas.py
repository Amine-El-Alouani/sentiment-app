from typing import Literal

from pydantic import BaseModel, Field, field_validator

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
Role = Literal["client", "admin"]


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

    @field_validator("text")
    @classmethod
    def refuser_texte_blanc(cls, valeur: str) -> str:
        if not valeur.strip():
            raise ValueError("texte vide une fois les blancs retirés")
        return valeur


class PredictResponse(BaseModel):
    label: Label
    score: float
    text: str


class HealthResponse(BaseModel):
    status: str
    model: str


class ChampInvalide(BaseModel):
    champ: str
    message: str


class DetailErreur(BaseModel):
    code: str
    message: str
    champs: list[ChampInvalide] = Field(default_factory=list)


class ErreurV1(BaseModel):
    erreur: DetailErreur
