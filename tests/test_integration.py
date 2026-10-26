"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_le_demarrage(monkeypatch):
    from fastapi.testclient import TestClient

    import src.predict as predict_module
    from api.main import app

    monkeypatch.setattr(predict_module, "MODELE", MODELE / "absent")
    predict_module.charger_modele.cache_clear()
    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass


def test_modele_retire_de_app_state():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        del app.state.model
        assert client.get("/health").status_code == 503
        reponse = client.post("/predict", json={"text": "test"})
        assert reponse.status_code == 503


@pytest.mark.parametrize("erreur", [RuntimeError("panne"), ValueError("bug interne")])
def test_modele_en_panne_ne_revele_pas_les_details(erreur, monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    class ModeleEnPanne:
        def predict(self, textes):
            raise erreur

        def predict_proba(self, textes):
            raise AssertionError("predict_proba ne devrait pas être appelé")

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "model", ModeleEnPanne())
        reponse = client.post("/predict", json={"text": "test"})

    assert reponse.status_code == 500
    assert "bug interne" not in reponse.text
    assert "panne" not in reponse.text
