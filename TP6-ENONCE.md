# TP6 : packager l'application

**Module :** Développement et déploiement d'applications intelligentes
**Auteur :** A. Larhlimi
**Séance :** semaine 6, TP de 2 h, en binôme

## Objectif

Faire du dépôt un **paquet Python installable** : une roue (`.whl`) que l'on installe avec `pip`, qui fournit une commande, `sentiment`, et qui fonctionne hors du dépôt. Au passage, l'API cesse de bricoler le chemin de Python : elle importe le paquet.

À la fin du TP, on peut, sur une machine qui n'a jamais vu le dépôt :

```bash
pip install sentiment_app-0.6.0-py3-none-any.whl
SENTIMENT_MODELE=/chemin/vers/sentiment.joblib sentiment predict "Livraison rapide, très satisfait"
```

## Ce que le TP fait comprendre

1. **Ce qui entre dans un paquet, et ce qui n'y entre pas.** Le code, oui ; les tests, les données et le modèle, non. Le modèle a son propre cycle de vie : on le réentraîne sans republier le code. Le paquet le trouve grâce à une variable d'environnement, `SENTIMENT_MODELE`.
2. **Les imports propres.** Depuis le TP3, `api/model.py` ajoute `src/` au chemin de Python pour importer `predict`. Une fois `predict.py` dans le paquet `sentiment_app`, l'API écrit simplement `from sentiment_app.predict import predict`.
3. **Une seule source pour la version**, lue par `pyproject.toml`, affichée par `sentiment --version`, gravée dans une étiquette Git `v0.6.0`.
4. **Les dépendances déclarées.** `pip` installe ce que le paquet déclare. scikit-learn y est épinglé : un modèle sauvegardé ne se relit qu'avec la version qui l'a produit.

## Prérequis

Le dépôt en fin de TP5 : `pytest -q` sans `failed`, CI verte.

## Déroulé

| Étape | Durée | Ce que vous faites | Contrôle |
| --- | --- | --- | --- |
| A | 15 min | Installer le kit, mesurer le départ | T35 : deux échecs voulus |
| B | 25 min | Déplacer `predict.py` dans le paquet, rendre le modèle configurable | T36 : un seul échec restant |
| C | 15 min | Brancher l'API sur le paquet | T37 : tout vert, plus aucun `sys.path` dans `api/` |
| D | 20 min | Installer le paquet en mode développement, essayer la commande | T38 : `sentiment` répond |
| E | 30 min | Construire la roue, l'installer dans un environnement neuf, hors du dépôt | T39, T40 |
| F | 15 min | Journal des versions, compte rendu, étiquette, push | T41 : CI verte, roue comprise |

## Livrables, sur `main`

- [ ] `sentiment_app/predict.py` (déplacé), `src/predict.py` (compatibilité), `api/model.py` sans `sys.path`
- [ ] `pyproject.toml` complété ; `pytest -q` sans `failed` ; CI verte, avec l'étape de la roue
- [ ] `CHANGELOG.md` : la version 0.6.0 décrite ; l'étiquette `v0.6.0` poussée
- [ ] `docs/semaine6.md` : les trois réponses

## Grille de notation (TP6 sur 10)

| Critère | Points | Vérification |
| --- | --- | --- |
| Le paquet : `predict()` dans `sentiment_app`, l'API sans `sys.path`, le modèle configurable | 2,5 | T36, T37 |
| La commande `sentiment` : version, predict, serve, ui | 2 | T38 |
| La roue : construite sans tests ni données ni modèle, installée et essayée hors du dépôt | 2,5 | T39, T40 |
| Tests et CI verts, dont l'étape de la roue | 1,5 | T35, T41 |
| `CHANGELOG.md`, étiquette `v0.6.0`, `docs/semaine6.md` | 1,5 | T41 |

## Pièges fréquents

| Piège | Conséquence | Correction |
| --- | --- | --- |
| Oublier le fichier de compatibilité `src/predict.py` | `No module named 'predict'` dans les tests du TP2 et du TP4 | Le recréer à partir de `extraits/predict_compatibilite.py` |
| `pip install .` sans `-e` pendant le développement | Les modifications du code ne sont pas prises en compte : le paquet installé est une copie figée | `pip install -e .` |
| Une ancienne roue dans `dist/` | On installe autre chose que ce qu'on croit | Vider `dist/` avant de construire |
| `SENTIMENT_MODELE` non définie hors du dépôt | « modèle introuvable », code de sortie 1 | Indiquer le chemin du modèle |
| Un modèle entraîné avec une autre version de scikit-learn | `AttributeError: 'LogisticRegression' object has no attribute 'multi_class'` | Entraîner et relire avec la même version (1.5) : le paquet et la CI l'épinglent |
| `git push` seul | L'étiquette `v0.6.0` reste sur le poste | `git push origin v0.6.0` |
