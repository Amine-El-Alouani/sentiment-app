# TP5 : l'interface Streamlit

**Module :** Développement et déploiement d'applications intelligentes
**Auteur :** A. Larhlimi
**Séance :** semaine 5, TP de 2 h, en binôme

## Objectif

Donner au service client une page web pour analyser un avis, ou tout un fichier d'avis. La page est un client de l'API : elle envoie `POST /predict` et traduit chaque réponse en message clair, y compris l'abstention (`INDETERMINE`) et les erreurs. Elle n'importe jamais `predict()` ni le fichier `.joblib` : un modèle réentraîné ne demande aucune modification de l'interface.

## Prérequis

Le dépôt `sentiment-app` en fin de TP4 : `pytest -q` sans aucun `failed`, CI verte, verdict `INDETERMINE` en place.

## Déroulé

| Étape | Durée | Ce que vous faites | Contrôle |
| --- | --- | --- | --- |
| A | 15 min | Installer le kit, lancer les douze nouveaux tests | T28 : aucun failed, 12 tests de plus |
| B | 20 min | Lire `ui/client.py` puis `ui/app.py` | (lecture) |
| C | 30 min | Lancer l'API et la page, analyser des avis | T29 : API prête ; T30 : verdicts ; T31 : abstention |
| D | 20 min | Provoquer les erreurs | T32 : refus et API injoignable |
| E | 20 min | Analyser un fichier d'avis | T33 : tableau, résumé, téléchargement |
| F | 15 min | Compte rendu, push, CI | T34 : CI verte |

## Livrables, sur `main`

- [ ] `ui/client.py`, `ui/app.py`, `tests/test_client.py`, `tests/test_interface.py`
- [ ] `pytest -q` sans `failed`, CI verte (Streamlit installé par la CI)
- [ ] `docs/semaine5.md` : les trois réponses

## Grille de notation (TP5 sur 10)

| Critère | Points | Vérification |
| --- | --- | --- |
| La page fonctionne : un avis, verdict, confiance, abstention | 3 | T29 à T31 |
| Les erreurs sont traduites pour l'utilisateur : 422, 503, API injoignable | 2 | T32 |
| Le lot d'avis : tableau, résumé, téléchargement | 2 | T33 |
| Tests du client et de la page verts, en local et en CI | 1,5 | T28, T34 |
| `docs/semaine5.md` : les trois réponses, appuyées sur des observations | 1,5 | Lecture |

## Pièges fréquents

| Piège | Conséquence | Correction |
| --- | --- | --- |
| Lancer la page sans l'API | « API injoignable » en haut de la page | `uvicorn api.main:app` dans un autre terminal |
| Importer `predict()` dans l'interface | Le modèle entre dans l'interface : deux endroits à changer à chaque réentraînement | Passer par l'API, toujours |
| Afficher le verdict brut `INDETERMINE` | L'utilisateur ne sait pas quoi faire | « Je ne sais pas : à faire vérifier par un humain » |
| Oublier `!data/avis_exemple.csv` | Le fichier d'exemple reste hors de Git | Le kit ajoute la ligne au `.gitignore` |
