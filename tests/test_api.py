from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app

ROOT = Path(__file__).resolve().parents[1]
MODELE = ROOT / "models" / "sentiment.joblib"

client = TestClient(app)


def test_root_indique_la_documentation():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"


@pytest.mark.skipif(not MODELE.exists(), reason="modèle absent")
def test_predict_positif():
    response = client.post(
        "/predict",
        json={"text": "Livraison rapide, produit conforme, très satisfait"},
    )

    assert response.status_code == 200
    assert response.json()["label"] == "POSITIVE"
    assert response.json()["score"] >= 0.5


@pytest.mark.skipif(not MODELE.exists(), reason="modèle absent")
def test_predict_negatif():
    response = client.post(
        "/predict",
        json={"text": "Produit cassé et service injoignable, à fuir"},
    )

    assert response.status_code == 200
    assert response.json()["label"] == "NEGATIVE"


@pytest.mark.parametrize("payload", [{"text": ""}, {}, {"text": 42}])
def test_predict_requete_invalide(payload):
    response = client.post("/predict", json=payload)

    assert response.status_code == 422
