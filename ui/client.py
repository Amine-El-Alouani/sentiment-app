"""Client HTTP de l'API (TP5) : tout ce que l'interface sait de l'API passe par ce module.

L'interface n'importe jamais predict() ni le fichier .joblib : elle envoie des requêtes à
l'API du TP3, corrigée au TP4, et traduit chaque réponse en message pour l'utilisateur.
"""
import os
from collections import Counter
from dataclasses import dataclass

import httpx

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
API_KEY = os.environ.get("API_KEY", "")
VERDICTS = {
    "POSITIVE": "Avis positif",
    "NEGATIVE": "Avis négatif",
    "INDETERMINE": "Je ne sais pas : à faire vérifier par un humain",
}
INJOIGNABLE = "API injoignable : lancez d'abord uvicorn api.main:app"
REFUS = "Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères."
SANS_MODELE = "Modèle non chargé : python src/train.py, puis relancer l'API."


@dataclass
class Reponse:
    """Ce que l'interface affiche : un verdict, ou un message d'erreur lisible."""

    ok: bool
    label: str | None = None
    score: float | None = None
    message: str = ""


def creer_session() -> httpx.Client:
    """La connexion à l'API. Les tests la remplacent par un client en mémoire."""
    return httpx.Client(
        base_url=API_URL,
        timeout=10,
        headers={"X-API-Key": API_KEY} if API_KEY else {},
    )


def sante(session: httpx.Client) -> Reponse:
    try:
        r = session.get("/v1/health" if API_KEY else "/health")
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        return Reponse(True, message=r.json()["model"])
    return Reponse(False, message=SANS_MODELE if r.status_code == 503 else f"Erreur de l'API ({r.status_code}).")


def predire(session: httpx.Client, texte: str) -> Reponse:
    try:
        r = session.post("/v1/predict" if API_KEY else "/predict", json={"text": texte})
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        corps = r.json()
        return Reponse(True, label=corps["label"], score=corps["score"])
    if r.status_code == 422:
        return Reponse(False, message=REFUS)
    if r.status_code in (401, 403):
        return Reponse(False, message="Clé d'API absente, invalide ou insuffisante.")
    if r.status_code == 503:
        return Reponse(False, message=SANS_MODELE)
    return Reponse(False, message=f"Erreur interne de l'API ({r.status_code}).")


def predire_lot(session: httpx.Client, textes: list[str]) -> list[Reponse]:
    return [predire(session, texte) for texte in textes]


def resumer(reponses: list[Reponse]) -> dict[str, int]:
    """Nombre d'avis par verdict ; les refus et les erreurs sont comptés à part."""
    compte = Counter(r.label if r.ok else "REFUS OU ERREUR" for r in reponses)
    return dict(sorted(compte.items()))
