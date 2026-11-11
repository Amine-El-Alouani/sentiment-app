# TP6 : marche à suivre, étape par étape et contrôle par contrôle

Six étapes, sept contrôles numérotés T35 à T41, dans la suite de ceux du TP5. Les commandes sont écrites pour PowerShell, dans le dossier du dépôt, environnement activé. Adaptez `C:\IA-DEV` à votre dossier de travail.

## Étape A. Installer le kit (T35)

```powershell
Expand-Archive "$HOME\Downloads\tp6-packaging-kit.zip" -DestinationPath C:\IA-DEV -Force
python C:\IA-DEV\tp6-packaging\appliquer_tp6.py C:\IA-DEV\sentiment-app --simulation
python C:\IA-DEV\tp6-packaging\appliquer_tp6.py C:\IA-DEV\sentiment-app
pip install -r requirements-dev.txt
python -m pytest -q
```

Le kit ajoute le paquet `sentiment_app/` (sa version et sa commande), `tests/test_packaging.py`, `CHANGELOG.md`, `docs/semaine6.md` et les documents du TP. Il complète :

- `pyproject.toml` : les métadonnées du paquet, ses dépendances et la commande `sentiment` ;
- `requirements-dev.txt` : `build`, l'outil qui construit la roue ;
- `pytest.ini` : `pythonpath = . src`, pour que les tests trouvent encore `predict` ;
- la CI : scikit-learn épinglé en 1.5, et une étape qui construit la roue, l'installe hors du dépôt et l'essaie.

### Contrôle T35 : deux échecs voulus

pytest affiche **2 failed**, tous les autres tests passent :

- `test_le_modele_se_place_ou_l_on_veut` : `sentiment_app.predict` n'existe pas encore ;
- `test_l_api_ne_bricole_plus_le_chemin_de_python` : `api/model.py` modifie encore `sys.path`.

Ce sont les deux étapes suivantes.

## Étape B. Faire entrer predict.py dans le paquet (T36)

```powershell
git mv src/predict.py sentiment_app/predict.py
Copy-Item C:\IA-DEV\tp6-packaging\extraits\predict_compatibilite.py src\predict.py
notepad sentiment_app\predict.py
```

`git mv` déplace le fichier en gardant son historique. Le fichier de compatibilité recréé dans `src/` garde valides `python src/predict.py "texte"` et `import predict` : il se remplace, à l'import, par le vrai module.

Dans `sentiment_app/predict.py`, rendez le modèle configurable :

1. ajoutez `import os` ;
2. remplacez la ligne `MODELE = ...` par une fonction `chemin_modele()` qui renvoie `Path(os.environ.get("SENTIMENT_MODELE") or RACINE / "models" / "sentiment.joblib")`, avec `RACINE = Path(__file__).resolve().parents[1]`, puis `MODELE = chemin_modele()` ;
3. dans `charger_modele()`, écrivez un message qui aide : le chemin cherché, et les deux façons d'y remédier (`python src/train.py`, ou la variable `SENTIMENT_MODELE`).

```powershell
python -m pytest -q
python src/predict.py "Livraison rapide, produit conforme, très satisfait"
```

### Contrôle T36 : un seul échec restant

pytest affiche **1 failed** : `test_l_api_ne_bricole_plus_le_chemin_de_python`. La commande du TP2 marche toujours : `positive (confiance 78%)`.

## Étape C. Brancher l'API sur le paquet (T37)

Dans `api/model.py`, supprimez les lignes qui ajoutent `src/` au chemin de Python (`RACINE = ...`, `sys.path.insert(...)`, les deux `from predict import ...` avec leur `# noqa: E402`), et les imports devenus inutiles (`sys`, `Path`). Écrivez à la place :

```python
from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as _predict
```

Mettez aussi à jour les deux docstrings qui citent encore `src/predict.py`.

```powershell
python -m pytest -q
Select-String -Path api\*.py -Pattern "sys.path"
ruff check .
mypy api
```

### Contrôle T37 : tout vert

pytest n'affiche **aucun failed** : six tests de plus qu'au TP5. `Select-String` ne trouve rien. ruff et mypy ne signalent rien.

## Étape D. La commande sentiment (T38)

```powershell
pip install -e .
sentiment --version
sentiment predict "Livraison rapide, produit conforme, très satisfait"
sentiment predict "xqzvb wlkptr grombu"
sentiment serve
```

`-e` installe le paquet en mode développement : il pointe vers vos fichiers, toute modification est prise en compte. Lisez `sentiment_app/cli.py` : `predict` passe par `api/model.py`, comme l'API, si bien que le seuil d'abstention s'applique aussi en ligne de commande.

### Contrôle T38

- `sentiment-app 0.6.0`
- `{"label": "POSITIVE", "score": 0.777, "text": "Livraison rapide, produit conforme, très satisfait"}`
- `{"label": "INDETERMINE", "score": 0.5162, "text": "xqzvb wlkptr grombu"}`
- `sentiment serve` lance l'API : `http://127.0.0.1:8000/health` répond `OK`. Arrêtez-la avec `Ctrl+C`. Dans un autre terminal, `sentiment ui` lance la page du TP5.

## Étape E. La roue, installée hors du dépôt (T39, T40)

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build --wheel
python -c "import zipfile, glob; print(sorted({n.split('/')[0] for n in zipfile.ZipFile(glob.glob('dist/*.whl')[0]).namelist()}))"
```

### Contrôle T39 : la roue

`Successfully built sentiment_app-0.6.0-py3-none-any.whl`, et la roue contient `api`, `sentiment_app`, `ui` (plus ses métadonnées) : ni `tests`, ni `data`, ni `models`, ni `src`.

Puis, dans un environnement neuf, hors du dépôt :

```powershell
cd $env:TEMP
py -3.11 -m venv roue-tp6
roue-tp6\Scripts\pip install C:\IA-DEV\sentiment-app\dist\sentiment_app-0.6.0-py3-none-any.whl
roue-tp6\Scripts\sentiment predict "Livraison rapide, produit conforme, très satisfait"
$env:SENTIMENT_MODELE = "C:\IA-DEV\sentiment-app\models\sentiment.joblib"
roue-tp6\Scripts\sentiment predict "Livraison rapide, produit conforme, très satisfait"
Remove-Item Env:SENTIMENT_MODELE
```

### Contrôle T40 : ailleurs que dans le dépôt

- `pip` installe la roue **et ses dépendances**, lues dans ses métadonnées (FastAPI, uvicorn, Pydantic, scikit-learn 1.5, joblib).
- Sans `SENTIMENT_MODELE` : `modèle introuvable : ...\roue-tp6\Lib\site-packages\models\sentiment.joblib. Lancez python src/train.py, ou indiquez son chemin dans la variable SENTIMENT_MODELE`, code de sortie 1.
- Avec : `{"label": "POSITIVE", "score": 0.777, ...}`.

## Étape F. Version, compte rendu, push (T41)

Décrivez la version 0.6.0 dans `CHANGELOG.md`, répondez aux trois questions de `docs/semaine6.md`, puis :

```powershell
cd C:\IA-DEV\sentiment-app
git add -A
git commit -m "Semaine 6 : paquet installable, version 0.6.0"
git tag -a v0.6.0 -m "TP6 : paquet installable"
git push
git push origin v0.6.0
```

### Contrôle T41

L'onglet Actions est vert, y compris la nouvelle étape « Roue installée hors du dépôt (TP6) », dont le journal se termine par la prédiction `POSITIVE`. Sur GitHub, l'étiquette `v0.6.0` apparaît dans la liste des étiquettes du dépôt.

Un avertissement `OptimizeWarning: Unknown solver options: iprint` peut apparaître pendant l'entraînement : il vient d'une version récente de SciPy et reste sans conséquence.

## Récapitulatif

| Contrôle | Commande | Attendu |
| --- | --- | --- |
| T35 | `python -m pytest -q` | 2 failed, voulus |
| T36 | `python -m pytest -q` | 1 failed ; `python src/predict.py` marche toujours |
| T37 | `python -m pytest -q`, `Select-String`, ruff, mypy | Aucun failed ; plus de `sys.path` dans `api/` |
| T38 | `sentiment --version`, `predict`, `serve` | `0.6.0` ; `POSITIVE` 0.777 ; `INDETERMINE` 0.5162 ; l'API répond |
| T39 | `python -m build --wheel` | Une roue `0.6.0` avec `api`, `sentiment_app`, `ui` seulement |
| T40 | La roue dans un environnement neuf | « modèle introuvable » sans la variable ; `POSITIVE` avec |
| T41 | `git push`, `git push origin v0.6.0` | CI verte, étape de la roue comprise ; étiquette visible |
