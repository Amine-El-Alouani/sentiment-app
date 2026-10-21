# TP2 : entraîner, évaluer et sauvegarder un modèle de sentiment

**Module :** Développement et déploiement d'applications intelligentes
**Auteur :** A. Larhlimi
**Séance :** semaine 2, TP de 2 h, en binôme

## Objectif

Produire un modèle de sentiment **reproductible**, **évalué correctement** et **sauvegardé** dans un fichier que l'API de la semaine 3 pourra charger. Pas un bon modèle : un modèle dont vous savez ce qu'il vaut, et pourquoi il se trompe.

La fiche de cadrage du cas 3, rédigée au TP1, devient le cahier des charges : approche machine learning, métrique de rappel sur la classe négative, seuil d'acceptation.

## Prérequis

Le dépôt `sentiment-app` du TP1, poussé sur GitHub, avec l'environnement complet installé. Si `pytest -q` n'affiche pas `38 passed` chez vous, réglez cela d'abord.

## Déroulé, cinq étapes

| Étape | Durée | Ce que vous faites | Contrôle |
| --- | --- | --- | --- |
| A | 15 min | Installer le kit dans votre dépôt | C1 : 2 failed, 38 passed, 2 skipped |
| B | 15 min | Générer et explorer le jeu de démonstration | C2 : 290 avis, 145 de chaque classe |
| C | 25 min | Entraîner le pipeline et sauvegarder le modèle | C3 : F1 macro 0,879, metrics.json écrit |
| D | 30 min | Évaluer : matrice de confusion et lecture des erreurs | C4 : 7 erreurs, toutes sur des avis mitigés |
| E | 35 min | Passer au vrai jeu Allociné, tests verts, push | C5 : 42 passed, CI verte |

## Livrables, sur la branche `main`

- [ ] `src/make_demo.py`, `train.py`, `evaluate.py`, `predict.py` présents et exécutables
- [ ] `models/metrics.json` versionné, avec un F1 macro au-dessus de 0,85
- [ ] `models/sentiment.joblib` produit sur chaque poste, **jamais commité**
- [ ] `tests/test_model.py` : 4 tests verts
- [ ] `pytest -q` affiche `42 passed`
- [ ] CI verte sur GitHub
- [ ] `docs/semaine2.md` : trois phrases sur les erreurs observées et ce qu'elles révèlent

## Grille de notation (TP2 sur 10)

| Critère | Points | Vérification |
| --- | --- | --- |
| Modèle entraîné, sauvegardé, rechargeable par `predict()` | 3 | `python src/predict.py "..."` sur un clone frais |
| Évaluation correcte : découpage avant vectorisation, métriques sur le jeu de test | 3 | Lecture du code et de `metrics.json` |
| Les 4 tests du modèle passent, CI verte | 2 | `pytest -q`, onglet Actions |
| Analyse des erreurs dans `docs/semaine2.md` | 2 | Lecture : les avis mitigés doivent être identifiés |

## Pièges fréquents

| Piège | Conséquence | Correction |
| --- | --- | --- |
| Vectoriser avant de découper | Le score grimpe artificiellement, le modèle s'effondre en production | `train_test_split` d'abord, `fit` ensuite |
| Sauvegarder le classifieur sans le vectoriseur | Le modèle est inutilisable : plus de vocabulaire | Sauvegarder le `Pipeline` entier |
| Commiter `models/sentiment.joblib` | Dépôt qui gonfle à chaque réentraînement | `models/*` est ignoré ; seul `metrics.json` est versionné |
| Évaluer sur les données d'entraînement | Un F1 proche de 1 qui ne veut rien dire | Toujours le jeu de test, jamais vu pendant l'entraînement |
| Oublier `random_state` | Deux exécutions, deux scores, aucune comparaison possible | `random_state=42` partout |
