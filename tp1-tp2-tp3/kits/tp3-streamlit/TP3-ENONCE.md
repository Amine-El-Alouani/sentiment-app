# TP3 : l'interface de démonstration

**Module :** Développement et déploiement d'applications intelligentes
**Auteur :** A. Larhlimi
**Séance :** TP de 2 h, en binôme

## Objectif

Rendre le modèle du TP2 utilisable par quelqu'un qui n'ouvrira jamais un terminal. L'interface Streamlit charge `models/sentiment.joblib` et appelle la fonction `predict()` écrite au TP2 : **aucune logique de prédiction n'est réécrite ici**.

C'est le premier contact du modèle avec un utilisateur. Deux questions de conception vous occupent toute la séance : que montrer quand le modèle hésite, et quel chiffre l'équipe métier regarde en premier.

## Prérequis

Le dépôt `sentiment-app`, TP1 et TP2 terminés, avec `pytest -q` à `42 passed` et un modèle entraîné.

## Déroulé, quatre étapes

| Étape | Durée | Ce que vous faites | Contrôle |
| --- | --- | --- | --- |
| A | 15 min | Installer le kit, lancer l'interface | S1 : la page s'ouvre sur localhost:8501 |
| B | 30 min | Onglet « un avis » : verdict, confiance, seuil d'incertitude | S2 : un avis mitigé affiche « à vérifier » |
| C | 40 min | Onglet « un fichier CSV » : lot, résumé, export | S3 : les trois métriques et le tableau trié |
| D | 35 min | Tests, documentation, push | S4 : 45 passed, CI verte |

## Livrables

- [ ] `ui/app.py` et `ui/helpers.py` présents et fonctionnels
- [ ] `tests/test_ui.py` : 3 tests verts
- [ ] `pytest -q` affiche `45 passed`
- [ ] `docs/semaine3.md` : trois phrases sur le seuil d'incertitude et son effet
- [ ] CI verte sur GitHub

## Grille de notation (sur 10)

| Critère | Points |
| --- | --- |
| L'interface charge le modèle et prédit sans erreur | 3 |
| Séparation logique et affichage : les tests passent sans lancer Streamlit | 3 |
| Traitement du lot : résumé chiffré et export exploitables | 2 |
| Analyse du seuil d'incertitude dans `docs/semaine3.md` | 2 |

## Pièges fréquents

| Piège | Conséquence | Correction |
| --- | --- | --- |
| Recharger le modèle à chaque interaction | Interface lente | `@st.cache_resource` sur le chargement |
| Mettre la logique dans `app.py` | Impossible à tester sans lancer Streamlit | Fonctions pures dans `helpers.py` |
| Afficher une prédiction tranchée à 51 % de confiance | L'utilisateur croit le modèle sûr | Seuil d'incertitude, verdict « à vérifier » |
| Commiter le modèle pour que l'interface marche ailleurs | Dépôt qui gonfle | Le modèle se réentraîne : `python src/train.py` |
