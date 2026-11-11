from fastapi.testclient import TestClient

from api.main import app

CLIENT_KEY = "client-key-1234567890"
ADMIN_KEY = "admin-key-1234567890"


def client(monkeypatch):
    monkeypatch.setenv("API_KEYS", f"{CLIENT_KEY}:client,{ADMIN_KEY}:admin")
    return TestClient(app)


def test_predict_sans_cle_est_refuse(monkeypatch):
    with client(monkeypatch) as appel:
        response = appel.post("/v1/predict", json={"text": "Très bien"})
    assert response.status_code == 401
    assert response.json()["erreur"]["code"] == "NON_AUTHENTIFIE"


def test_predict_avec_cle_client(monkeypatch):
    with client(monkeypatch) as appel:
        response = appel.post(
            "/v1/predict",
            json={"text": "Livraison rapide, produit conforme, très satisfait"},
            headers={"X-API-Key": CLIENT_KEY},
        )
    assert response.status_code == 200
    assert response.json()["label"] == "POSITIVE"


def test_modele_refuse_le_role_client(monkeypatch):
    with client(monkeypatch) as appel:
        response = appel.get("/v1/modele", headers={"X-API-Key": CLIENT_KEY})
    assert response.status_code == 403
    assert response.json()["erreur"]["code"] == "ACCES_REFUSE"


def test_modele_accepte_le_role_admin(monkeypatch):
    with client(monkeypatch) as appel:
        response = appel.get("/v1/modele", headers={"X-API-Key": ADMIN_KEY})
    assert response.status_code == 200
    assert response.json()["seuil_abstention"] == 0.6


def test_validation_v1_utilise_le_format_unique(monkeypatch):
    with client(monkeypatch) as appel:
        response = appel.post(
            "/v1/predict",
            json={"text": "   "},
            headers={"X-API-Key": CLIENT_KEY},
        )
    assert response.status_code == 422
    assert response.json()["erreur"]["code"] == "ENTREE_INVALIDE"
    assert response.json()["erreur"]["champs"]


def test_charger_cles_ne_recopie_pas_une_cle_invalide(monkeypatch):
    from api.securite import charger_cles

    monkeypatch.setenv("API_KEYS", "abc:client")
    try:
        charger_cles()
    except ValueError as erreur:
        assert "abc" not in str(erreur)
    else:
        raise AssertionError("Une clé trop courte doit refuser la configuration")