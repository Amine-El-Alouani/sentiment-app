# TP6 : corrigé et valeurs de référence (enseignant)

Valeurs mesurées sur la chaîne complète TP1 à TP5 (corrigés), Python 3.11 et 3.12, scikit-learn 1.5.2.

## Fichiers du corrigé

| Fichier | Ce qui change |
| --- | --- |
| `sentiment_app/predict.py` | `src/predict.py` déplacé par `git mv` ; `chemin_modele()` lit `SENTIMENT_MODELE` ; message d'erreur qui donne le chemin cherché et les deux remèdes |
| `src/predict.py` | Le fichier de compatibilité de `extraits/`, sans modification |
| `api/model.py` | Plus de `sys.path` : `from sentiment_app.predict import charger_modele` et `predict as _predict` ; imports `sys` et `Path` retirés ; docstrings à jour |
| `CHANGELOG.md` | La version 0.6.0 décrite pour trois publics |
| `docs/semaine6.md` | Les trois réponses attendues |

## Contrôle par contrôle

| Contrôle | Mesuré |
| --- | --- |
| T35 | 2 failed : `test_le_modele_se_place_ou_l_on_veut` (ImportError), `test_l_api_ne_bricole_plus_le_chemin_de_python` |
| T36 | 1 failed (le second) ; `python src/predict.py "Livraison rapide, produit conforme, très satisfait"` affiche `positive (confiance 78%)` |
| T37 | Aucun failed : 6 tests de plus qu'au TP5 (avec les corrigés : 101 passed, 2 xfailed) ; ruff et mypy muets |
| T38 | `sentiment-app 0.6.0` ; `{"label": "POSITIVE", "score": 0.777, ...}` ; `{"label": "INDETERMINE", "score": 0.5162, ...}` ; `sentiment serve` : `/health` répond `OK` |
| T39 | `sentiment_app-0.6.0-py3-none-any.whl`, qui contient `api`, `sentiment_app`, `ui` et `sentiment_app-0.6.0.dist-info` ; dépendances déclarées : fastapi <0.116, uvicorn <0.31, pydantic <3, scikit-learn <1.6, joblib <2 ; extra `ui` : streamlit, pandas, httpx |
| T40 | Sans `SENTIMENT_MODELE` : « modèle introuvable : .../site-packages/models/sentiment.joblib. Lancez python src/train.py, ou indiquez son chemin dans la variable SENTIMENT_MODELE », code 1 ; avec : `POSITIVE` 0.777 |
| T41 | CI rejouée sur un clone neuf : les huit étapes vertes, la dernière se termine par `{"label": "POSITIVE", "score": 0.777, ...}` |

## Ce que la CI aurait raté sans l'épinglage

Avant le TP6, la CI installait scikit-learn sans version : elle entraînait avec la 1.9.1. La roue, elle, installe la 1.5.2. Relu par la roue, ce modèle provoque `AttributeError: 'LogisticRegression' object has no attribute 'multi_class'`. C'est pourquoi `appliquer_tp6.py` épingle `scikit-learn==1.5.*` dans la CI : un bon exemple, pour le cours, de dépendance entre un code et un artefact.

## Points de correction

- Le déplacement doit passer par `git mv` : `git log --follow sentiment_app/predict.py` remonte alors jusqu'au TP2.
- Un `api/model.py` qui garde `sys.path` mais passe les autres tests perd les points du paquet.
- `docs/semaine6.md` : la réponse 3 doit citer la version de scikit-learn, ou l'erreur observée, pas seulement « pour la reproductibilité ».
