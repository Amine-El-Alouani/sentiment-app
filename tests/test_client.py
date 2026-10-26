"""Tests du client de l'API (TP5) : l'API tourne en mémoire, aucun serveur à lancer."""
from pathlib import Path

import httpx
import pytest

from ui import client

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def session():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # un client httpx branché directement sur l'API
        yield c


def test_sante_api_prete(session):
    etat = client.sante(session)
    assert etat.ok and "TP2" in etat.message


def test_avis_positif(session):
    r = client.predire(session, "Livraison rapide, produit conforme, très satisfait")
    assert r.ok and r.label == "POSITIVE" and r.score is not None


def test_texte_inconnu_donne_indetermine(session):
    r = client.predire(session, "xqzvb wlkptr grombu")
    assert r.ok and r.label == "INDETERMINE"


def test_espaces_refuses(session):
    r = client.predire(session, "   ")
    assert not r.ok and r.message == client.REFUS


def test_modele_non_charge(session, monkeypatch):
    from api.main import app

    monkeypatch.setattr(app.state, "classifier", None)
    assert client.predire(session, "Très bien").message == client.SANS_MODELE


def test_api_injoignable():
    with httpx.Client(base_url="http://127.0.0.1:9", timeout=1) as sans_serveur:
        assert client.predire(sans_serveur, "Très bien").message == client.INJOIGNABLE


def test_lot_et_resume(session):
    reponses = client.predire_lot(session, ["Livraison rapide, produit conforme, très satisfait",
                                            "Produit cassé et service injoignable, à fuir", "   "])
    assert client.resumer(reponses) == {"NEGATIVE": 1, "POSITIVE": 1, "REFUS OU ERREUR": 1}
