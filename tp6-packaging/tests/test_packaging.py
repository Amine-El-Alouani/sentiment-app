"""Tests du paquet (TP6) : installable, une commande, une version, un modèle qu'on peut placer ailleurs."""
import json
import re
import tomllib
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
MODELE = RACINE / "models" / "sentiment.joblib"


def lire_pyproject() -> dict:
    return tomllib.loads((RACINE / "pyproject.toml").read_text(encoding="utf-8"))


def test_metadonnees_du_paquet():
    """pyproject.toml décrit un paquet nommé, installable, avec sa commande."""
    projet = lire_pyproject()["project"]
    assert projet["name"] == "sentiment-app"
    assert projet["scripts"]["sentiment"] == "sentiment_app.cli:main"
    # Le modèle sauvegardé ne se relit qu'avec la version de scikit-learn qui l'a produit
    assert any(dependance.startswith("scikit-learn") for dependance in projet["dependencies"])


def test_une_seule_source_pour_la_version():
    """La version est écrite à un seul endroit, sentiment_app/__init__.py, et pyproject.toml la lit."""
    import sentiment_app

    assert re.fullmatch(r"\d+\.\d+\.\d+", sentiment_app.__version__)
    assert lire_pyproject()["tool"]["setuptools"]["dynamic"]["version"]["attr"] == "sentiment_app.__version__"


def test_l_api_ne_bricole_plus_le_chemin_de_python():
    """L'API importe le paquet ; plus aucun sys.path modifié à la main dans api/."""
    for fichier in sorted((RACINE / "api").glob("*.py")):
        assert "sys.path" not in fichier.read_text(encoding="utf-8"), f"{fichier.name} modifie encore sys.path"


def test_le_modele_se_place_ou_l_on_veut(monkeypatch, tmp_path):
    """Le modèle n'est pas dans le paquet : SENTIMENT_MODELE indique où il est."""
    from sentiment_app import predict

    monkeypatch.setenv("SENTIMENT_MODELE", str(tmp_path / "ailleurs.joblib"))
    assert predict.chemin_modele() == tmp_path / "ailleurs.joblib"
    monkeypatch.delenv("SENTIMENT_MODELE")
    assert predict.chemin_modele() == MODELE


def test_commande_version(capsys):
    from sentiment_app import __version__, cli

    with pytest.raises(SystemExit) as fin:
        cli.main(["--version"])
    assert fin.value.code == 0
    assert capsys.readouterr().out.strip() == f"sentiment-app {__version__}"


@pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")
def test_commande_predict(capsys):
    from sentiment_app import cli

    assert cli.main(["predict", "Livraison rapide, produit conforme, très satisfait"]) == 0
    resultat = json.loads(capsys.readouterr().out)
    assert resultat["label"] == "POSITIVE" and 0.5 <= resultat["score"] <= 1
