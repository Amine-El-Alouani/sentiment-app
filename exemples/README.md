# Exemples : à quoi ressemblera la suite

Deux scripts facultatifs, à lancer après le TP1 pour voir où mène le dépôt que vous venez d'installer. Ils ne font pas partie des livrables et ne sont pas notés.

## 1. Entraîner un modèle (ce que sera la semaine 2)

```bash
python exemples/train_sentiment.py
```

Le script télécharge 20 000 avis de films en français depuis une URL publique (jeu Allociné, 7,6 Mo, quelques secondes), découpe les données, entraîne un pipeline TF-IDF et régression logistique, affiche le rapport de classification, puis enregistre `models/sentiment.joblib`.

Résultat attendu : une exactitude d'environ 0,92 et un rappel d'environ 0,91 sur la classe négative, donc **au-dessus du seuil de 0,90** fixé dans la fiche de cadrage du cas 3. Le modèle est accepté, et c'est le point de la démonstration : un classifieur linéaire sur des sacs de mots suffit largement pour ce besoin, sans GPU et sans réseau de neurones.

Si le réseau est coupé ou filtré par un proxy, le script bascule tout seul sur les 30 avis de `data/sample_reviews.csv`. Il tourne alors en une seconde, mais le résultat n'a aucune valeur statistique : six avis en test, une erreur de plus ou de moins déplace le score de 17 points. C'est exactement pourquoi la semaine 2 travaille sur un vrai corpus.

Quatre points de méthode à repérer dans le code : le découpage se fait avant la vectorisation (sinon le jeu de test fuite dans l'entraînement), le `Pipeline` enferme vectoriseur et modèle dans un seul objet, `random_state=42` rend le découpage reproductible, et c'est le pipeline entier qui est sauvegardé, pas seulement le classifieur.

Le modèle produit n'entre pas dans Git : `models/*` est exclu par le `.gitignore`, comme tout artefact lourd et reconstructible.

## 2. Afficher une interface (ce que sera la semaine 5)

```bash
streamlit run exemples/app_streamlit.py
```

Le navigateur s'ouvre sur `http://localhost:8501`. Un onglet analyse un avis saisi à la main, l'autre traite un fichier CSV contenant une colonne `review` et propose le résultat en téléchargement.

Lancez d'abord `train_sentiment.py` : sans `models/sentiment.joblib`, l'interface affiche un message d'erreur et s'arrête.

Chaque interaction réexécute le script de haut en bas, c'est le modèle de fonctionnement de Streamlit. D'où le décorateur `@st.cache_resource` sur le chargement du modèle, qui évite de relire le fichier à chaque clic.

## Prérequis

Ces deux scripts ont besoin de l'installation complète (`pip install -r requirements.txt`), pas seulement des trois paquets du contrôle T1. `joblib`, `pyarrow` (lecture du fichier distant) et `streamlit` y sont déjà.

## Source des données

Jeu Allociné, publié par T. Blard sous licence MIT : `https://huggingface.co/datasets/tblard/allocine`. Avis publics de spectateurs, aucune donnée personnelle, conforme à la règle du cours sur les données.
