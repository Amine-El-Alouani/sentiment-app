# Tester la commande `sentiment` (TP6)

Le TP6 fournit une commande, `sentiment`, avec quatre sous-commandes : `--version`, `predict`, `serve`, qui lance l'API, et `ui`, qui lance la page. Ce document explique comment les tester de deux façons :

- **à la main**, pour voir ce que voit l'utilisateur ;
- **automatiquement**, avec `tests/test_commande_sentiment.py`, pour que la CI le vérifie à chaque push.

Les sorties et les codes de sortie indiqués ont été obtenus en exécutant la commande sur un dépôt en fin de TP6, avec le modèle de démonstration.

## 1. Avant de commencer

À la racine du dépôt, environnement activé :

```powershell
pip install -e .
python src/train.py
```

- `pip install -e .` installe le paquet en mode développement et crée la commande `sentiment`.
- `python src/train.py` n'est utile que si le modèle de démonstration manque.

Après chaque commande, `$LASTEXITCODE` affiche son code de sortie : `0` en cas de réussite, `1` pour une erreur gérée par la commande, `2` pour une erreur d'usage détectée par argparse.

## 2. Tester à la main

### 2.1 `sentiment --version`

```powershell
sentiment --version
$LASTEXITCODE
```

Attendu : `sentiment-app 0.6.0`, puis `0`. La version est lue dans `sentiment_app/__init__.py`, sa seule source. Une sous-commande inconnue, par exemple `sentiment danser`, affiche l'usage et renvoie `2`.

### 2.2 `sentiment predict`

```powershell
sentiment predict "Livraison rapide, produit conforme, très satisfait"
sentiment predict "xqzvb wlkptr grombu"
sentiment predict Livraison rapide, produit conforme, très satisfait
sentiment predict
$env:SENTIMENT_MODELE = "C:\nulle\part\modele.joblib"; sentiment predict "Très bien"; $LASTEXITCODE
Remove-Item Env:SENTIMENT_MODELE
```

| Essai | Attendu | Code |
| --- | --- | --- |
| Un avis positif | `{"label": "POSITIVE", "score": 0.777, "text": "Livraison rapide, produit conforme, très satisfait"}` | 0 |
| Des mots inconnus | `{"label": "INDETERMINE", "score": 0.5162, ...}` : le seuil d'abstention de l'API s'applique | 0 |
| Sans guillemets | Le même résultat : les mots sont réunis en un seul avis | 0 |
| Sans texte | `error: the following arguments are required: texte` | 2 |
| Modèle introuvable | `modèle introuvable : C:\nulle\part\modele.joblib. Lancez python src/train.py, ou indiquez son chemin dans la variable SENTIMENT_MODELE` | 1 |

`predict` passe par `api/model.py`, comme l'API : la commande et l'API donnent toujours le même verdict.

### 2.3 `sentiment serve` (deux terminaux)

**Terminal 1**, qui reste ouvert :

```powershell
sentiment serve
```

Attendu :

```text
Modèle chargé avec succès : tfidf-logreg (TP2, models/sentiment.joblib)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Terminal 2**, environnement activé :

```powershell
python -c "import httpx; print(httpx.get('http://127.0.0.1:8000/health').json())"
python -c "import httpx; r = httpx.post('http://127.0.0.1:8000/predict', json={'text': 'Livraison rapide, produit conforme, très satisfait'}); print(r.status_code, r.json())"
```

Attendu :

```text
{'status': 'OK', 'model': 'tfidf-logreg (TP2, models/sentiment.joblib)'}
200 {'label': 'POSITIVE', 'score': 0.777, 'text': 'Livraison rapide, produit conforme, très satisfait'}
```

La page `http://127.0.0.1:8000/docs` permet les mêmes essais dans le navigateur.

- **Pourquoi httpx ?** Sous PowerShell, les guillemets du JSON et les accents passent mal avec `curl` et `Invoke-RestMethod`. httpx est installé avec les dépendances du cours.
- **Les options.** `sentiment serve --port 8011` lance l'API sur un autre port, et `--host` change l'adresse d'écoute.
- **Arrêter l'API** : `Ctrl+C` dans le terminal 1.

### 2.4 `sentiment ui` (l'API doit tourner)

Laissez `sentiment serve` dans le terminal 1, puis, dans le terminal 2 :

```powershell
sentiment ui
```

Attendu :

```text
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Au tout premier lancement, Streamlit demande une adresse électronique : appuyez sur Entrée.

Dans la page :

1. saisissez « Livraison rapide, produit conforme, très satisfait », puis analysez : la page affiche « Avis positif » et « 78% » ;
2. arrêtez l'API dans le terminal 1, puis analysez à nouveau : la page affiche « API injoignable : lancez d'abord uvicorn api.main:app ».

La page cherche l'API à l'adresse `http://127.0.0.1:8000`. Si l'API tourne sur un autre port, indiquez-le avant de lancer la page : `$env:API_URL = "http://127.0.0.1:8011"`.

## 3. Tester automatiquement

### 3.1 Ce qui est déjà testé, et ce qui manque

Les six tests du kit, dans `tests/test_packaging.py`, vérifient le paquet :

| Test | Ce qu'il vérifie |
| --- | --- |
| `test_metadonnees_du_paquet` | Le nom du paquet, la commande `sentiment`, scikit-learn dans les dépendances |
| `test_une_seule_source_pour_la_version` | La version est écrite une seule fois, et `pyproject.toml` la lit |
| `test_l_api_ne_bricole_plus_le_chemin_de_python` | Plus aucun `sys.path` dans `api/` |
| `test_le_modele_se_place_ou_l_on_veut` | `SENTIMENT_MODELE` désigne le modèle |
| `test_commande_version` | `sentiment --version` |
| `test_commande_predict` | Un appel à `sentiment predict` |

Restent les cas limites de `predict`, puis `serve` et `ui` : c'est l'objet de `tests/test_commande_sentiment.py`.

### 3.2 Installer et lancer

Copiez `test_commande_sentiment.py` dans `tests/`, puis :

```powershell
python -m pytest tests/test_commande_sentiment.py tests/test_packaging.py -q
```

Attendu : **13 passed**, les 6 tests du kit et les 7 nouveaux. Sans modèle entraîné, `tests/test_commande_sentiment.py` seul donne **5 passed, 2 skipped** : les deux tests qui ont besoin du modèle sont ignorés, comme en CI au TP2.

### 3.3 Les techniques utilisées

Aucun test ne lance de serveur : un serveur bloquerait le test, et la CI n'a ni navigateur ni terminal.

| Technique | À quoi elle sert ici |
| --- | --- |
| `cli.main([...])` | Appeler la commande comme si on la tapait, mais dans le même processus que le test |
| `capsys` | Capturer ce que la commande écrit sur la sortie standard et sur la sortie d'erreur |
| `pytest.raises(SystemExit)` | Récupérer le code de sortie quand argparse arrête le programme |
| `monkeypatch.setattr` | Remplacer, le temps d'un test, une fonction par un faux qui enregistre ses arguments |
| `monkeypatch.setitem(sys.modules, ...)` | Faire croire qu'un module est absent |
| `pytest.mark.skipif`, `pytest.importorskip` | Ignorer un test quand ce dont il a besoin manque, au lieu de le faire échouer |

### 3.4 Chaque test, expliqué

#### `test_predict_reunit_les_mots`

**Ce qu'il vérifie** : sans guillemets, les mots de l'avis sont réunis en un seul texte.

**Comment** : la sous-commande déclare `texte` avec `nargs="+"`, si bien que chaque mot arrive séparément, et `_predire` les joint par des espaces. Le test passe les mots un par un, comme PowerShell quand on oublie les guillemets, puis lit le JSON imprimé : le texte reconstitué, et le verdict `POSITIVE`. Il a besoin du modèle.

#### `test_predict_s_abstient_sur_des_mots_inconnus`

**Ce qu'il vérifie** : sur des mots absents du vocabulaire, `predict` s'abstient, comme l'API.

**Comment** : `_predire` passe par `api/model.py`, donc le seuil d'abstention de 0,60 s'applique aussi en ligne de commande. Aucun mot n'étant connu, la confiance vaut 0,5162, sous le seuil : le verdict est `INDETERMINE`. Il a besoin du modèle.

#### `test_predict_sans_texte_est_refuse`

**Ce qu'il vérifie** : sans texte, la commande est refusée avec le code 2.

**Comment** : argparse lève `SystemExit(2)` et écrit l'usage sur la sortie d'erreur. `pytest.raises` récupère le code ; `capsys` capture le message, qui doit nommer l'argument manquant, `texte`.

#### `test_predict_sans_modele`

**Ce qu'il vérifie** : si le modèle est introuvable, `predict` l'explique et renvoie le code 1, sans afficher de trace d'exception.

**Comment** : `monkeypatch` remplace le chemin du modèle par un fichier qui n'existe pas. Un point délicat : `charger_modele` garde le modèle en cache après son premier chargement (`lru_cache`). Le test vide donc le cache avant l'appel, pour forcer une nouvelle recherche, et après, dans un bloc `finally`, pour que les tests suivants rechargent le vrai modèle.

#### `test_serve_lance_uvicorn_sur_l_api`

**Ce qu'il vérifie** : `serve` lance uvicorn sur `api.main:app`, avec l'hôte et le port demandés.

**Comment** : `uvicorn.run` est remplacé par une petite fonction qui enregistre ses arguments au lieu de démarrer un serveur. Le test fait deux appels : sans option, il attend les valeurs par défaut, `127.0.0.1` et `8000` ; avec `--host 0.0.0.0 --port 8011`, il attend ces valeurs.

#### `test_ui_lance_streamlit_sur_la_page`

**Ce qu'il vérifie** : `ui` lance Streamlit sur la page du dépôt, `ui/app.py`, avec le Python de l'environnement.

**Comment** : `subprocess.call` est remplacé par une fonction qui enregistre la commande au lieu de l'exécuter. Le test vérifie que la commande commence par `sys.executable -m streamlit run`, puis qu'elle désigne bien `ui/app.py`. Il est ignoré si Streamlit n'est pas installé.

#### `test_ui_sans_streamlit`

**Ce qu'il vérifie** : sans Streamlit, `ui` renvoie le code 1 et indique comment l'installer.

**Comment** : placer `None` dans `sys.modules` sous le nom `streamlit` fait échouer `import streamlit` par une `ImportError`, comme sur un poste où Streamlit manque. La commande affiche alors « Streamlit absent », suivi de la commande pip qui installe la variante `ui` du paquet.

## 4. Erreurs fréquentes

| Symptôme | Cause | Correction |
| --- | --- | --- |
| `sentiment` n'est pas reconnu | Paquet non installé, ou environnement désactivé | `pip install -e .`, environnement activé |
| `modèle introuvable` dans le dépôt | Le modèle n'a pas été entraîné | `python src/train.py` |
| `serve` échoue au démarrage : adresse déjà utilisée | Une autre API tourne déjà sur le port 8000 | L'arrêter, ou `sentiment serve --port 8011` |
| La page affiche « API injoignable » | L'API n'est pas lancée, ou tourne sur un autre port | `sentiment serve` dans un autre terminal, ou `$env:API_URL` |
| Streamlit attend une saisie au premier lancement | Il demande une adresse électronique | Appuyer sur Entrée |
| Le JSON envoyé à l'API est refusé ou ses accents sont abîmés | Guillemets et encodage de PowerShell | Utiliser les commandes httpx de la section 2.3 |
| `test_predict_sans_modele` fait échouer les tests suivants | Le cache de `charger_modele` n'a pas été vidé | Garder le `cache_clear()` du bloc `finally` |

## Annexe : le fichier de tests complet

```python
"""Tests des sous-commandes de sentiment, sans lancer de serveur (TP6).

tests/test_packaging.py vérifie déjà --version et un appel à predict. Ce fichier couvre le reste :
predict dans ses cas limites, puis serve et ui. Aucun serveur n'est lancé : uvicorn et Streamlit sont
remplacés par des faux, qui enregistrent la façon dont la commande les appelle.

Lancer :  python -m pytest tests/test_commande_sentiment.py -q
Attendu : 7 passed ; 5 passed et 2 skipped tant que le modèle n'a pas été entraîné.
"""
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
```
