"""Tests de la page Streamlit (TP5), avec l'outil de test de Streamlit (AppTest)."""
from pathlib import Path

import httpx
import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

from ui import client  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
PAGE = str(RACINE / "ui" / "app.py")
pytestmark = pytest.mark.skipif(not (RACINE / "models" / "sentiment.joblib").exists(),
                                reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def api():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def page(api, monkeypatch):
    monkeypatch.setattr(client, "creer_session", lambda: api)  # la page parle à l'API en mémoire
    return AppTest.from_file(PAGE, default_timeout=30).run()


def analyser(page, texte):
    page.text_area[0].input(texte).run()
    page.button[0].click().run()
    return page


def test_page_annonce_api_prete(page):
    assert "API prête" in page.caption[0].value


def test_avis_positif(page):
    assert analyser(page, "Livraison rapide, produit conforme, très satisfait").metric[0].label == "Avis positif"


def test_texte_inconnu_je_ne_sais_pas(page):
    resultat = analyser(page, "xqzvb wlkptr grombu")
    assert resultat.metric[0].label.startswith("Je ne sais pas")
    assert "seuil d'abstention" in resultat.info[0].value


def test_espaces_avertissement(page):
    assert analyser(page, "   ").warning[0].value == client.REFUS


def test_api_injoignable(monkeypatch):
    monkeypatch.setattr(client, "creer_session",
                        lambda: httpx.Client(base_url="http://127.0.0.1:9", timeout=1))
    page = AppTest.from_file(PAGE, default_timeout=30).run()
    assert page.error[0].value == client.INJOIGNABLE
