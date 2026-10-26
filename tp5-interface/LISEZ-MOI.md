# Kit TP5 : l'interface Streamlit (semaine 5)

Ce kit se superpose au dépôt `sentiment-app` en fin de TP4. Il n'écrase rien.

```bash
python appliquer_tp5.py ../sentiment-app --simulation   # voir sans rien écrire
python appliquer_tp5.py ../sentiment-app
```

Si Windows a ajouté un dossier en décompressant l'archive, donnez le chemin complet du dépôt.

| Fichier | Rôle |
| --- | --- |
| `ui/client.py` | Le client de l'API : santé, prédiction, lot d'avis, résumé ; chaque réponse traduite en message |
| `ui/app.py` | La page Streamlit : un avis, ou un fichier d'avis ; elle n'importe jamais le modèle |
| `tests/test_client.py` | Sept tests du client, contre l'API en mémoire |
| `tests/test_interface.py` | Cinq tests de la page, avec l'outil de test de Streamlit |
| `data/avis_exemple.csv` | Six avis pour essayer l'onglet « Un fichier d'avis » |
| `docs/semaine5.md` | Les trois questions du compte rendu |
| `TP5-ENONCE.md`, `MARCHE-A-SUIVRE-TP5.md` | L'énoncé et le pas à pas, contrôles T28 à T34 |

Le script ajoute aussi `!data/avis_exemple.csv` au `.gitignore` et Streamlit à l'installation de la CI.
