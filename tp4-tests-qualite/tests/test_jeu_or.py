"""Le jeu d'or : vos avis, écrits à la main, vérifiés à chaque commit (TP4, étape C).

Un avis échoue si l'API se trompe franchement (POSITIVE au lieu de NEGATIVE, ou
l'inverse). Une abstention ne le fait pas échouer : elle est comptée par
src/bilan_jeu_or.py. Une erreur connue reste dans le jeu, déclarée dans la colonne
erreur_connue : le test devient xfail(strict=True) et signalera sa correction.
"""
import csv
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
JEU_OR = RACINE / "data" / "jeu_or.csv"
MODELE = RACINE / "models" / "sentiment.joblib"
FRANCHES = {"POSITIVE", "NEGATIVE"}
MINIMUM_AVIS, MINIMUM_DIFFICILES = 20, 5


def lire_jeu_or() -> list[dict[str, str]]:
    if not JEU_OR.exists():
        return []
    with JEU_OR.open(encoding="utf-8", newline="") as f:
        return [ligne for ligne in csv.DictReader(f) if (ligne.get("text") or "").strip()]


LIGNES = lire_jeu_or()


def cas_du_jeu_or():
    for numero, ligne in enumerate(LIGNES, start=2):  # ligne 1 : l'en-tête
        raison = (ligne.get("erreur_connue") or "").strip()
        marques = [pytest.mark.xfail(strict=True, reason=raison)] if raison else []
        yield pytest.param(ligne["text"], ligne["attendu"], id=f"ligne-{numero}", marks=marques)


def test_jeu_or_complet():
    """20 avis au moins, dont 5 difficiles, chacun avec une étiquette attendue valide."""
    assert len(LIGNES) >= MINIMUM_AVIS, f"jeu d'or incomplet : {len(LIGNES)} avis sur {MINIMUM_AVIS}"
    difficiles = [ligne for ligne in LIGNES if (ligne.get("difficulte") or "").strip()]
    assert len(difficiles) >= MINIMUM_DIFFICILES, (
        f"{len(difficiles)} avis difficiles sur {MINIMUM_DIFFICILES} (colonne difficulte)"
    )
    for ligne in LIGNES:
        assert ligne["attendu"] in FRANCHES, f"étiquette attendue invalide : {ligne['attendu']!r}"


@pytest.fixture(scope="module")
def client():
    if not MODELE.exists():
        pytest.skip("modèle non produit : python src/train.py")
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:
        yield c


@pytest.mark.parametrize("texte, attendu", list(cas_du_jeu_or()))
def test_pas_d_erreur_franche(client, texte, attendu):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200
    label = reponse.json()["label"]
    assert not (label in FRANCHES and label != attendu), f"erreur franche : {label} au lieu de {attendu}"
