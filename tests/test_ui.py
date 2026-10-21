"""Tests de l'interface de démonstration (TP3).

Ils portent sur les fonctions pures de ui/helpers.py, pas sur l'affichage :
Streamlit n'est pas lancé pendant les tests.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

RACINE = Path(__file__).resolve().parents[1]
MODELE = RACINE / "models" / "sentiment.joblib"
sys.path.insert(0, str(RACINE / "ui"))


@pytest.fixture(scope="module")
def predire():
    if not MODELE.exists():
        pytest.skip("models/sentiment.joblib absent sur ce poste (normal en CI)")
    from helpers import charger_predicteur
    return charger_predicteur()


def test_helpers_importables():
    """L'interface se charge sans Streamlit : la logique est bien séparée de l'affichage."""
    import helpers
    for nom in ["charger_predicteur", "classer", "predire_lot", "resumer"]:
        assert hasattr(helpers, nom), f"fonction manquante : {nom}"


def test_classer_ajoute_un_verdict(predire):
    from helpers import classer
    r = classer("Service impeccable, je recommande", predire)
    # inclusion et non égalité : predict() peut renvoyer des champs supplémentaires
    assert {"label", "score", "verdict", "incertain"} <= set(r)
    assert r["verdict"] in {"positive", "negative", "à vérifier"}
    with pytest.raises(ValueError):
        classer("   ", predire)


def test_lot_et_resume(predire):
    from helpers import predire_lot, resumer
    df = pd.DataFrame({"review": [
        "Produit cassé, service injoignable",
        "Livraison rapide, très satisfait",
        "",
    ]})
    sortie = predire_lot(df, predire)
    assert len(sortie) == 2, "les lignes vides doivent être écartées"
    assert {"prediction", "confiance", "verdict"} <= set(sortie.columns)
    r = resumer(sortie)
    assert r["total"] == 2 and 0 <= r["part_negatifs"] <= 100
    with pytest.raises(KeyError):
        predire_lot(pd.DataFrame({"texte": ["a"]}), predire)
