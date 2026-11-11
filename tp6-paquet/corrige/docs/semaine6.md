# Semaine 6 : le paquet, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi le modèle n'est-il pas dans la roue ? Comment le paquet le trouve-t-il ?

Le modèle pèse plus que le code, change à un autre rythme (on le réentraîne sans republier le code) et n'est pas versionné dans Git. La roue ne contient que le code. Le paquet trouve le modèle par la variable SENTIMENT_MODELE ; sans elle, en développement, c'est models/sentiment.joblib à la racine du dépôt. Hors du dépôt, sans la variable, la commande répond « modèle introuvable » avec le chemin cherché : c'est voulu. Le TP7 (MLflow) en fera un artefact suivi.

## 2. Qu'est-ce qui a changé dans api/model.py quand predict() est entré dans le paquet, et pourquoi est-ce mieux ?

Les quatre lignes qui ajoutaient src/ au chemin de Python, avec leurs « noqa: E402 », sont remplacées par deux imports explicites depuis sentiment_app.predict. L'import fonctionne partout où le paquet est installé, sans dépendre du dossier courant ; ruff, mypy et l'éditeur suivent les imports ; et le test test_l_api_ne_bricole_plus_le_chemin_de_python empêche le retour du bricolage.

## 3. La roue installée hors du dépôt : qu'a-t-il fallu lui fournir, et pourquoi scikit-learn est-il épinglé dans pyproject.toml ?

Il a fallu lui fournir le modèle, par SENTIMENT_MODELE. Les dépendances, pip les a installées seul, d'après les métadonnées de la roue. scikit-learn est épinglé parce qu'un modèle sauvegardé ne se relit qu'avec la version qui l'a produit : un modèle entraîné avec scikit-learn 1.9 et relu par la 1.5 provoque « AttributeError: 'LogisticRegression' object has no attribute 'multi_class' ». Pour la même raison, la CI entraîne désormais avec scikit-learn 1.5.
