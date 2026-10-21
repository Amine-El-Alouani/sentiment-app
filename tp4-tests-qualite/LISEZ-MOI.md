# Kit TP4 : tests approfondis et qualité (semaine 4)

Ce kit se superpose au dépôt `sentiment-app` en fin de TP3 (l'API FastAPI, dossier `api/`). Il n'écrase rien.

## Installation, depuis ce dossier

```bash
python appliquer_tp4.py ../sentiment-app --simulation   # voir sans rien écrire
python appliquer_tp4.py ../sentiment-app
```

Puis, dans le dépôt : `pip install -r requirements-dev.txt` et `MARCHE-A-SUIVRE-TP4.md`, contrôle T21.

## Ce que le kit ajoute

| Fichier | Rôle |
| --- | --- |
| `requirements-dev.txt` | pytest-cov, hypothesis, ruff, mypy, pre-commit, versions épinglées |
| `pyproject.toml` | Configuration de ruff, mypy et de la couverture (complété s'il existe déjà) |
| `.pre-commit-config.yaml` | ruff et mypy lancés à chaque commit |
| `src/courbe_seuil.py` | La courbe du seuil d'abstention sur le jeu de test du TP2 |
| `src/bilan_jeu_or.py` | Ce que l'API répond à chacun de vos avis du jeu d'or |
| `tests/test_limites.py` | Tests aux limites et tests de propriété, à compléter |
| `tests/test_integration.py` | Démarrage, modèle absent, pannes, à compléter |
| `tests/test_jeu_or.py` | Un cas de test par avis du jeu d'or |
| `data/jeu_or.csv` | L'en-tête du jeu d'or : `text,attendu,difficulte,erreur_connue` |
| `docs/semaine4.md` | Le canevas du compte rendu |
| `TP4-ENONCE.md`, `MARCHE-A-SUIVRE-TP4.md` | L'énoncé et le pas à pas |
| `ci-tp4.yml` | Les quatre étapes qui remplacent l'étape « Tests » de la CI (étape E), à recopier, pas copié dans le dépôt |
