"""Tests aux limites du contrat d'entrée (TP4, étape B). À COMPLÉTER.

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


# Étape B.1 : huit cas au moins, chacun avec son code attendu. Deux sont donnés.
# À ajouter : texte fait d'espaces, un seul caractère, exactement 2000 caractères,
# champ absent, champ d'un autre type (42), corps qui n'est pas du JSON (b"pas du json").
CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    # Étape B.2 : pour chaque 422, vérifiez aussi la FORME de la réponse :
    # « detail » doit être la liste d'erreurs standard de FastAPI (objets avec loc, msg, type).


# Étape B.5 : deux tests de propriété avec hypothesis, dans ce fichier.
#   from hypothesis import given, settings, strategies as st
#   1. tout texte de 1 à 2000 caractères contenant un caractère non blanc :
#      200, étiquette du contrat, score entre 0 et 1 ;
#   2. tout texte fait uniquement de blancs : 422, sous la forme standard.
# Pensez à @settings(deadline=None) : le premier appel peut être plus lent que les autres.
