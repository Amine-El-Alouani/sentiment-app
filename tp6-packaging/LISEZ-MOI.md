# Kit TP6 : packager l'application (semaine 6)

Ce kit se superpose au dépôt `sentiment-app` en fin de TP5. Il n'écrase rien.

```bash
python appliquer_tp6.py ../sentiment-app --simulation   # voir sans rien écrire
python appliquer_tp6.py ../sentiment-app
```

Si Windows a ajouté un dossier en décompressant l'archive, donnez le chemin complet du dépôt.

| Fichier | Rôle |
| --- | --- |
| `sentiment_app/__init__.py` | Le paquet et sa version, `0.6.0`, écrite à un seul endroit |
| `sentiment_app/cli.py`, `__main__.py` | La commande `sentiment` : `--version`, `predict`, `serve`, `ui` |
| `tests/test_packaging.py` | Six tests du paquet |
| `CHANGELOG.md` | Le journal des versions, de 0.1.0 à 0.6.0, à compléter |
| `docs/semaine6.md` | Les trois questions du compte rendu |
| `extraits/pyproject-tp6.toml` | Le bloc ajouté à `pyproject.toml` |
| `extraits/ci-tp6.yml` | L'étape ajoutée à la CI |
| `extraits/predict_compatibilite.py` | Le fichier à recréer dans `src/predict.py` après le déplacement (étape B) |
| `TP6-ENONCE.md`, `MARCHE-A-SUIVRE-TP6.md` | L'énoncé et le pas à pas, contrôles T35 à T41 |

Le déplacement de `predict.py` dans le paquet et le branchement de l'API restent au binôme : c'est le cœur du TP.
