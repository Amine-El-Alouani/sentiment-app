# Kit TP2 : le modèle de sentiment (semaine 2)

Ce kit se superpose au dépôt `sentiment-app` créé au TP1. Il n'écrase rien de la semaine 1.

## Installation, une commande

Depuis ce dossier, en indiquant le chemin de votre dépôt :

```bash
python appliquer_tp2.py ../sentiment-app
```

Le script copie `src/`, `tests/test_model.py` et le notebook dans votre dépôt, puis ajoute une ligne à votre `.gitignore` pour que `models/metrics.json` soit versionné alors que le modèle, lui, reste exclu.

Pour voir ce qu'il ferait sans rien écrire : `python appliquer_tp2.py ../sentiment-app --simulation`.

## Ce que le kit ajoute

| Fichier | Rôle |
| --- | --- |
| `src/make_demo.py` | Génère 290 avis français déterministes, dont 100 mitigés et 30 neutres |
| `src/train.py` | Entraîne et sauvegarde le pipeline, écrit `models/metrics.json` |
| `src/evaluate.py` | Matrice de confusion, rapport de classification, trois erreurs commentées |
| `src/predict.py` | La fonction `predict()` que l'API de la semaine 3 appellera |
| `tests/test_model.py` | Quatre tests : métriques complètes, F1 au-dessus du seuil, prédiction, format de sortie |
| `notebooks/TP2-colab.ipynb` | Le même TP sur Colab, sans installation |
| `TP2-ENONCE.md`, `MARCHE-A-SUIVRE-TP2.md` | L'énoncé et le pas à pas : cinq étapes, cinq contrôles |

## Prérequis

Le dépôt du TP1 avec son environnement complet installé (`pip install -r requirements.txt`). Les paquets nécessaires, `pandas`, `scikit-learn`, `joblib` et `pyarrow`, y sont déjà.
