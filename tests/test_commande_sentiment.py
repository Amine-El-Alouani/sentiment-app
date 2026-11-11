import json
import sys
from pathlib import Path

import pytest

from sentiment_app import cli

RACINE = Path(__file__).resolve().parents[1]  # la racine du dépôt
MODELE = RACINE / "models" / "sentiment.joblib"  # le modèle de démonstration, produit par src/train.py

# Les tests qui ont besoin du vrai modèle sont ignorés tant qu'il n'existe pas, comme en CI au TP2.
avec_modele = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@avec_modele
def test_predict_reunit_les_mots(capsys):
    """Sans guillemets, les mots de l'avis sont réunis en un seul texte.

    La sous-commande déclare texte avec nargs="+" : chaque mot arrive séparément, et _predire les
    joint par des espaces. Le test passe les mots un par un, comme PowerShell quand on oublie les
    guillemets, puis lit le JSON imprimé : le texte reconstitué et le verdict POSITIVE.
    """
    assert cli.main(["predict", "Livraison", "rapide,", "produit", "conforme,", "très", "satisfait"]) == 0
    resultat = json.loads(capsys.readouterr().out)
    assert resultat["text"] == "Livraison rapide, produit conforme, très satisfait"
    assert resultat["label"] == "POSITIVE"


@avec_modele
def test_predict_s_abstient_sur_des_mots_inconnus(capsys):
    """Sur des mots absents du vocabulaire, predict s'abstient, comme l'API.

    _predire passe par api/model.py : le seuil d'abstention de 0,60 s'applique donc aussi en ligne
    de commande. Aucun mot n'étant connu, la confiance vaut 0,5162, sous le seuil : le verdict est
    INDETERMINE.
    """
    assert cli.main(["predict", "xqzvb wlkptr grombu"]) == 0
    assert json.loads(capsys.readouterr().out)["label"] == "INDETERMINE"


def test_predict_sans_texte_est_refuse(capsys):
    """Sans texte, argparse refuse la commande avec le code 2.

    argparse lève SystemExit(2) et écrit l'usage sur la sortie d'erreur ; capsys la capture, pour
    vérifier que le message nomme l'argument manquant, texte.
    """
    with pytest.raises(SystemExit) as fin:
        cli.main(["predict"])
    assert fin.value.code == 2
    assert "texte" in capsys.readouterr().err


def test_predict_sans_modele(monkeypatch, tmp_path, capsys):
    """Si le modèle est introuvable, predict l'explique et renvoie le code 1, sans trace d'exception.

    Le chemin du modèle est remplacé par un fichier qui n'existe pas. charger_modele garde le modèle
    en cache (lru_cache) : le cache est vidé avant l'appel, pour forcer une nouvelle recherche, et
    après, pour que les tests suivants rechargent le vrai modèle.
    """
    from sentiment_app import predict

    monkeypatch.setattr(predict, "MODELE", tmp_path / "absent.joblib")
    predict.charger_modele.cache_clear()
    try:
        assert cli.main(["predict", "Très bien"]) == 1
    finally:
        predict.charger_modele.cache_clear()
    assert "modèle introuvable" in capsys.readouterr().err


def test_serve_lance_uvicorn_sur_l_api(monkeypatch):
    """serve lance uvicorn sur api.main:app, avec l'hôte et le port demandés.

    uvicorn.run est remplacé par une fonction qui enregistre ses arguments, au lieu de démarrer un
    serveur qui bloquerait le test. Deux appels : les valeurs par défaut, 127.0.0.1 et 8000, puis
    les options --host et --port.
    """
    import uvicorn

    appels = []
    monkeypatch.setattr(uvicorn, "run", lambda app, host, port: appels.append((app, host, port)))
    assert cli.main(["serve"]) == 0
    assert cli.main(["serve", "--host", "0.0.0.0", "--port", "8011"]) == 0
    assert appels == [("api.main:app", "127.0.0.1", 8000), ("api.main:app", "0.0.0.0", 8011)]


def test_ui_lance_streamlit_sur_la_page(monkeypatch):
    """ui lance Streamlit sur la page du dépôt, ui/app.py, avec le Python de l'environnement.

    subprocess.call est remplacé par une fonction qui enregistre la commande au lieu de l'exécuter.
    Le test vérifie sys.executable, le module streamlit et le chemin de la page. Il est ignoré si
    Streamlit n'est pas installé.
    """
    pytest.importorskip("streamlit")
    commandes = []
    monkeypatch.setattr(cli.subprocess, "call", lambda commande: commandes.append(commande) or 0)
    assert cli.main(["ui"]) == 0
    assert commandes[0][:4] == [sys.executable, "-m", "streamlit", "run"]
    assert Path(commandes[0][4]) == RACINE / "ui" / "app.py"


def test_ui_sans_streamlit(monkeypatch, capsys):
    """Sans Streamlit, ui renvoie le code 1 et indique comment l'installer.

    Placer None dans sys.modules fait échouer import streamlit par une ImportError, comme sur un
    poste où Streamlit manque. La commande affiche alors : Streamlit absent, puis la commande pip
    qui installe la variante ui du paquet.
    """
    monkeypatch.setitem(sys.modules, "streamlit", None)
    assert cli.main(["ui"]) == 1
    assert "Streamlit absent" in capsys.readouterr().err
