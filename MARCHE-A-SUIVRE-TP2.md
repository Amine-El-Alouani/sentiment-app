# TP2 : marche à suivre, étape par étape et test par test

Cinq étapes, cinq contrôles numérotés C1 à C5. Ne passez à l'étape suivante que lorsque le contrôle précédent est vert.

## Étape A. Installer le kit dans votre dépôt (15 min, à deux)

Décompressez le kit à côté de votre dépôt, pas dedans, puis :

```bash
cd tp2-semaine2
python appliquer_tp2.py ../sentiment-app --simulation   # voir ce qui sera copié
python appliquer_tp2.py ../sentiment-app                # copier pour de bon
cd ../sentiment-app
source .venv/bin/activate          # Windows : .venv\Scripts\Activate.ps1
```

### Contrôle C1 : le point de départ

```bash
python -m pytest -q
```

Attendu : **2 failed, 38 passed, 2 skipped**.

Les 38 verts sont ceux du TP1, inchangés. Les 2 échecs réclament `models/metrics.json`, qui n'existe pas encore : c'est le travail de l'étape C. Les 2 ignorés attendent le modèle lui-même.

## Étape B. Générer le jeu de démonstration (15 min)

```bash
python src/make_demo.py
head -5 data/demo_reviews.csv
```

### Contrôle C2 : le jeu est là

Attendu : **290 avis, 145 positifs et 145 négatifs**. Le fichier contient 80 avis nettement positifs, 80 nettement négatifs, 100 mitigés et 30 neutres.

Ouvrez le fichier et lisez trois avis mitigés. Ils ont tous la même forme : une première moitié d'un sentiment, un retournement (« mais finalement », « sauf que ensuite »), une seconde moitié de l'autre sentiment. L'étiquette suit la seconde moitié, celle qui conclut. Retenez cette structure : elle explique toutes les erreurs de l'étape D.

## Étape C. Entraîner et sauvegarder (25 min)

```bash
python src/train.py
```

### Contrôle C3 : le modèle existe et vaut quelque chose

Attendu :

```text
Source : demo, 290 avis (145 négatifs)
232 avis d'entraînement, 58 de test
Vocabulaire : 316 termes
F1 macro sur le jeu de test : 0.879 (seuil 0.85)
```

Deux fichiers sont produits : `models/sentiment.joblib`, qui n'entre pas dans Git, et `models/metrics.json`, qui y entre. Vérifiez-le :

```bash
git status --short
```

Dans la liste, `models/metrics.json` doit apparaître, et `models/sentiment.joblib` ne doit **pas** y être. Si le modèle apparaît, la ligne `!models/metrics.json` a été mal placée dans le `.gitignore`.

`data/demo_reviews.csv` n'apparaît pas non plus : il est exclu par `data/*`, parce qu'il se régénère en une commande. Deux artefacts reconstructibles restent donc hors de Git, et seule la mesure, elle, est versionnée.

Trois lignes du code méritent une lecture attentive avant de continuer : le `train_test_split` **avant** toute vectorisation, le `Pipeline` qui enferme vectoriseur et modèle dans un seul objet, et le `random_state=42` qui rend le découpage reproductible.

## Étape D. Évaluer et comprendre les erreurs (30 min)

```bash
python src/evaluate.py
```

### Contrôle C4 : la matrice de confusion

Attendu :

```text
            negative  positive
  negative        27         2
  positive         5        24
```

**7 erreurs sur 58 avis.** Lisez les trois exemples affichés par le script : ce sont tous des avis mitigés. Le modèle compte des mots positifs et des mots négatifs, mais il ne voit pas le retournement, parce qu'un sac de mots n'a pas d'ordre. C'est la limite annoncée en cours, et elle est ici mesurable.

Écrivez vos observations dans `docs/semaine2.md`, trois phrases : quelles erreurs, pourquoi, et ce qu'il faudrait pour les corriger (des embeddings, semaine 9).

## Étape E. Le vrai jeu, les tests, le push (35 min)

```bash
python src/train.py --allocine
```

### Contrôle C5 : tout est vert

Attendu : **F1 macro 0,920** sur 4 000 avis de test, puis

```bash
python -m pytest -q          # 42 passed
git add -A
git commit -m "Semaine 2 : modele de sentiment, metriques et tests"
git push
```

L'onglet Actions doit passer au vert. Remarquez que la CI exécute les 42 tests sans jamais avoir le modèle : les deux tests de prédiction sont ignorés, les deux tests de métriques lisent `metrics.json`, qui, lui, est versionné. C'est la raison d'être de ce fichier.

## Récapitulatif des cinq contrôles

| Contrôle | Commande | Résultat attendu |
| --- | --- | --- |
| C1 | `pytest -q` | 2 failed, 38 passed, 2 skipped |
| C2 | `python src/make_demo.py` | 290 avis, 145 de chaque classe |
| C3 | `python src/train.py` | F1 macro 0,879 ; metrics.json seul en attente de commit |
| C4 | `python src/evaluate.py` | 7 erreurs, toutes sur des avis mitigés |
| C5 | `python src/train.py --allocine` puis `pytest -q` | F1 macro 0,920 ; 42 passed ; CI verte |

## En cas de blocage

| Message | Cause | Correction |
| --- | --- | --- |
| `data/demo_reviews.csv absent` | étape B sautée | `python src/make_demo.py` |
| `models/metrics.json absent` | étape C sautée | `python src/train.py` |
| `F1 macro ... sous le seuil` | jeu trop petit ou modèle mal configuré | relancer avec `--allocine` |
| `ModuleNotFoundError: joblib` | installation partielle du TP1 | `pip install -r requirements.txt` |
| `No module named 'train'` | `evaluate.py` lancé depuis `src/` avec un ancien kit | relancer depuis la racine du dépôt |
| Le modèle apparaît dans `git status` | `.gitignore` mal ajusté | vérifier `models/*` et `!models/metrics.json` |
