import os
import secrets
from typing import Annotated, Callable, cast

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from api.schemas import Role

EN_TETE = APIKeyHeader(name="X-API-Key", auto_error=False)
ROLES = {"client", "admin"}
LONGUEUR_MIN = 16


def charger_cles(brut: str | None = None) -> dict[str, Role]:
    brut = os.environ.get("API_KEYS", "") if brut is None else brut
    cles: dict[str, Role] = {}
    for morceau in filter(None, (element.strip() for element in brut.split(","))):
        cle, separateur, role = morceau.rpartition(":")
        if not separateur or role not in ROLES:
            raise ValueError(f"rôle inconnu dans API_KEYS : {role!r}")
        if len(cle) < LONGUEUR_MIN:
            raise ValueError(f"clé trop courte dans API_KEYS ({len(cle)} caractères)")
        cles[cle] = cast(Role, role)
    return cles


def identifier(cle: Annotated[str | None, Security(EN_TETE)]) -> Role:
    if not cle:
        raise HTTPException(401, "Clé d'API manquante : en-tête X-API-Key", headers={"WWW-Authenticate": "ApiKey"})
    for connue, role in charger_cles().items():
        if secrets.compare_digest(cle.encode(), connue.encode()):
            return role
    raise HTTPException(401, "Clé d'API invalide", headers={"WWW-Authenticate": "ApiKey"})


def exiger(*autorises: Role) -> Callable[[Role], Role]:
    def verifier(role: Annotated[Role, Security(identifier)]) -> Role:
        if role not in autorises:
            raise HTTPException(403, f"Accès refusé au rôle « {role} »")
        return role

    return verifier
