"""Tests du modèle de la semaine 2.

Deux tests lisent models/metrics.json, qui est versionné dans Git : ils tournent
donc aussi dans la CI, où le modèle lui-même n'existe pas. Les deux autres sont
ignorés tant que models/sentiment.joblib n'a pas été produit sur le poste.
"""
import json
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
METRIQUES = RACINE / "models" / "metrics.json"
MODELE = RACINE / "models" / "sentiment.joblib"
SEUIL_F1 = 0.85

sys.path.insert(0, str(RACINE / "src"))


def lire_metriques() -> dict:
    """Lue dans le test lui-même : un fichier absent donne un échec lisible."""
    assert METRIQUES.exists(), "models/metrics.json absent : lancez python src/train.py"
    return json.loads(METRIQUES.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def predicteur():
    if not MODELE.exists():
        pytest.skip("models/sentiment.joblib absent sur ce poste (normal en CI)")
    from predict import predict
    return predict


def test_metriques_completes():
    metriques = lire_metriques()
    for cle in ["source", "f1_macro", "accuracy", "recall_negative", "n_train", "n_test"]:
        assert cle in metriques, f"clé absente de metrics.json : {cle}"
    assert metriques["n_test"] > 0


def test_f1_au_dessus_du_seuil():
    metriques = lire_metriques()
    f1 = metriques["f1_macro"]
    assert f1 >= SEUIL_F1, f"F1 macro {f1} sous le seuil {SEUIL_F1} : réentraînez ou améliorez le modèle"


def test_prediction_evidente(predicteur):
    assert predicteur("Service impeccable, livraison rapide, je recommande")["label"] == "positive"
    assert predicteur("Produit cassé et service client injoignable")["label"] == "negative"


def test_format_de_sortie(predicteur):
    sortie = predicteur("Conforme à la description")
    assert set(sortie) == {"label", "score"}
    assert sortie["label"] in {"positive", "negative"}
    assert 0.0 <= sortie["score"] <= 1.0
    with pytest.raises(ValueError):
        predicteur("   ")
