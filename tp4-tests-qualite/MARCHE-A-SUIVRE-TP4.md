# TP4 : marche à suivre, étape par étape et contrôle par contrôle

**Module :** Développement et déploiement d'applications intelligentes · **Auteur :** A. Larhlimi

Cinq étapes, sept contrôles numérotés T21 à T27, dans la suite de ceux du TP3 (T14 à T20). Ne passez à l'étape suivante que lorsque le contrôle précédent est vert.

**Prérequis :** le dépôt `sentiment-app` en fin de TP3 (dossier `api/`), `pytest -q` à `48 passed`, et vos 20 avis du jeu d'or rédigés (voir l'énoncé, étape C).

## Étape A. Installer le kit et mesurer le point de départ (15 min)

Décompressez `tp4-tests-qualite-kit.zip` **à côté** du dépôt, pas dedans :

```text
IA-DEV/
├── sentiment-app/          <- votre dépôt
└── tp4-tests-qualite/      <- le kit
```

```bash
cd tp4-tests-qualite
python appliquer_tp4.py ../sentiment-app --simulation   # voir ce qui sera fait
python appliquer_tp4.py ../sentiment-app
cd ../sentiment-app
pip install -r requirements-dev.txt
python src/train.py
python -m pytest -q
```

Sous Windows, mêmes commandes avec `..\` au lieu de `../`, environnement virtuel activé.

`python src/train.py` n'est pas une formalité : le TP4 se fait avec le modèle du jeu de démonstration, **celui que la CI entraîne**. Si votre poste a gardé le modèle Allociné de la fin du TP2, vos mesures et votre jeu d'or ne correspondront pas à ceux de la CI.

Le kit ajoute ses fichiers sans rien écraser, puis complète `pyproject.toml` et `.gitignore`. Parmi les lignes ajoutées, `!data/jeu_or.csv` : sans elle, votre jeu d'or resterait hors de Git, donc hors de la CI.

### Contrôle T21 : le point de départ, mesuré

Attendu : **1 failed, 51 passed, 1 skipped**.

| Ce que vous voyez | Pourquoi | Quand ça passe au vert |
| --- | --- | --- |
| 51 passed | Les 48 du TP3, plus les 3 exemples donnés dans les fichiers à compléter | Déjà bon |
| 1 failed | `test_jeu_or_complet` : `data/jeu_or.csv` ne contient encore aucun avis | Quand vos 20 avis y sont |
| 1 skipped | Le test « un avis, un cas » n'a encore rien à tester | Idem |

Si vous avez déjà copié vos avis dans `data/jeu_or.csv`, le test complet passe et chaque avis devient un test : les échecs éventuels se traitent à l'étape C.

Puis les trois mesures à recopier dans `docs/semaine4.md`, **sans rien corriger** :

```bash
python -m pytest -q --cov=api --cov-report=term-missing
ruff check .
mypy api
```

Sur le dépôt de référence : couverture de `api/` à 91 % avec 6 lignes jamais exécutées, toutes dans `main.py` ; 8 remarques de ruff sur les fichiers du TP2 et du TP3 (votre dépôt peut en avoir d'autres, sur les fichiers du TP1) ; mypy ne signale rien.

## Étape B. Le contrat d'entrée (30 min)

Ouvrez `tests/test_limites.py` : la fixture `client`, la fonction `en_json` et deux cas sont donnés. Complétez-le comme l'énoncé le demande (B.1, B.2, B.5), puis :

```bash
python -m pytest -q tests/test_limites.py
```

**Avant toute correction, un cas et une propriété échouent, alors que le code de retour du cas est le bon.** C'est ce que l'étape vous fait trouver. Lisez l'exemple qu'hypothesis affiche sous `Falsifying example` : c'est le plus petit texte qu'il ait trouvé pour faire échouer la propriété. Cherchez pourquoi ce caractère-là.

Corrigez `api/schemas.py` (B.4), puis relancez.

### Contrôle T22 : une seule forme de refus

Lancez l'API (`uvicorn api.main:app --reload`), ouvrez `http://localhost:8000/docs`, puis `POST /predict` avec `{"text": "   "}`, puis avec `{"text": ""}`. Les deux réponses sont des **422 dont `detail` est une liste** d'objets `loc`, `msg`, `type`.

### Contrôle T23 : les propriétés tiennent

Relancez `python -m pytest -q tests/test_limites.py` trois fois. Attendu, avec les minimums demandés (8 cas et 2 propriétés) : **10 passed**, trois fois de suite.

## Étape C. Un modèle qui sait dire « je ne sais pas » (25 min)

Dans `/docs`, envoyez trois textes différents faits de mots inventés. Comparez les étiquettes et les confiances : que remarquez-vous, et pourquoi ?

```bash
python src/courbe_seuil.py
```

Les deux premières lignes affichées doivent être :

```text
 seuil  répond à   part  exactitude  erreurs  vers un humain
  0.50        58   100%       0.879        7               0
```

À 0,50, le modèle répond à tout : on retrouve l'exactitude (0,879) et les 7 erreurs du TP2. Si ce n'est pas le cas, votre modèle n'est pas celui du jeu de démonstration : relancez `python src/train.py`.

Implémentez l'abstention dans `api/model.py` (C.4, C.5), puis le jeu d'or :

```bash
python src/bilan_jeu_or.py
python -m pytest -q tests/test_jeu_or.py
```

### Contrôle T24 : le modèle se tait quand il ne sait rien

Dans `/docs`, un texte fait de mots inventés reçoit `INDETERMINE`, avec la même confiance qu'avant.

### Contrôle T25 : le jeu d'or est vert

`pytest -q tests/test_jeu_or.py` n'affiche aucun `failed`. Une erreur franche que vous ne savez pas corriger apparaît en `xfailed`, avec sa raison dans la colonne `erreur_connue`. Recopiez le bilan de `src/bilan_jeu_or.py` dans `docs/semaine4.md`.

## Étape D. L'API telle qu'elle tourne (25 min)

Écrivez les tests de `tests/test_integration.py` (D.1 à D.4 de l'énoncé), puis :

```bash
python -m pytest -q tests/test_integration.py
```

Un de vos tests de panne échoue avant toute correction de `main.py` : lequel, et que reçoit le client ? Corrigez (D.5), puis :

```bash
python -m pytest -q --cov=api --cov-report=term-missing --cov-fail-under=95
```

### Contrôle T26 : panne en 500, couverture à 95 %

Les deux pannes répondent 500, sans le message interne. La sortie se termine par `Required test coverage of 95% reached`. Sur le dépôt de référence : 97 % sans aucune exclusion (seul le bloc `if __name__ == "__main__":` reste non couvert), 100 % une fois ce bloc exclu et l'exclusion justifiée.

## Étape E. Qualité statique et automatisation (25 min)

Typez le contrat (E.1 à E.3), puis rendez ruff muet (E.4) :

```bash
mypy api
ruff check . --fix
ruff check .
```

Ce que `--fix` ne règle pas se corrige à la main : lisez le code de chaque règle et sa page d'aide, plutôt que d'ajouter un `# noqa`.

Installez le crochet et vérifiez qu'il refuse un commit fautif (E.5) :

```bash
pre-commit install
```

Ajoutez par exemple `import os` en tête d'un fichier, `git add -A`, `git commit -m "essai"` : la ligne `ruff` passe en `Failed` et le commit n'est pas créé. Retirez la ligne.

Enfin, dans `.github/workflows/ci.yml`, remplacez l'étape « Tests » par les quatre étapes de `ci-tp4.yml` (E.6) : chacune active l'environnement virtuel, comme les étapes du TP1.

### Contrôle T27 : tout est vert, en local et en CI

```bash
ruff check .           # All checks passed!
mypy api               # Success: no issues found in 4 source files
python -m pytest -q    # aucun failed
```

Sur le dépôt de référence, le corrigé donne **83 passed, 2 xfailed**. Vos nombres peuvent être plus grands, jamais avec un `failed`. Puis `git push` : l'onglet Actions passe au vert avec ruff, mypy et le seuil de couverture.

## Après la séance

```bash
git add -A
git commit -m "Semaine 4 : tests approfondis et qualite"
git push
```

`docs/semaine4.md` complet, avec vos chiffres, pas ceux de ce document.

## Récapitulatif des contrôles

| Contrôle | Commande | Résultat attendu |
| --- | --- | --- |
| T21 | `pytest -q`, puis couverture, ruff, mypy | 1 failed, 51 passed, 1 skipped ; mesures recopiées |
| T22 | `/docs`, `{"text": "   "}` | 422, `detail` en liste, comme pour `{"text": ""}` |
| T23 | `pytest -q tests/test_limites.py`, trois fois | 10 passed, trois fois |
| T24 | `/docs`, mots inventés | `INDETERMINE` |
| T25 | `pytest -q tests/test_jeu_or.py` | aucun failed ; erreurs connues en xfailed |
| T26 | `pytest --cov=api --cov-fail-under=95` | pannes en 500 ; seuil de 95 % atteint |
| T27 | `ruff check .`, `mypy api`, `pytest -q`, push | muets ; aucun failed ; CI verte |

## En cas de blocage

| Message | Cause | Correction |
| --- | --- | --- |
| `ERREUR : api/main.py absent` | Le TP3 (l'API) n'est pas dans le dépôt | Appliquer d'abord le kit du TP3 |
| `No module named 'hypothesis'` ou `ruff` introuvable | Outils de la semaine non installés | `pip install -r requirements-dev.txt`, environnement activé |
| `FailedHealthCheck` et `function_scoped_fixture` | Fixture de portée `function` dans un test hypothesis | `@pytest.fixture(scope="module")` |
| `DeadlineExceeded` | Un exemple dépasse le délai par défaut d'hypothesis | `@settings(deadline=None)` |
| mypy : `Cannot find implementation or library stub for module named "predict"` | mypy lancé ailleurs qu'à la racine, ou section `[tool.mypy]` absente | Lancer depuis la racine ; vérifier `pyproject.toml` |
| pre-commit : exécutable `ruff` ou `mypy` introuvable | Commit lancé sans l'environnement virtuel | Activer l'environnement, puis recommiter |
| Un test du TP3 échoue (`POSITIVE` attendu) | Modèle Allociné resté sur le poste | `python src/train.py` |
| Jeu d'or vert en local, rouge en CI (`XPASS(strict)`) | `xfail` réglés avec un autre modèle que celui de la CI | Entraîner le modèle de démonstration, refaire le bilan |
| `data/jeu_or.csv` absent de `git status` | `.gitignore` exclut tout le dossier (`data/`) | Remplacer `data/` par `data/*` ; garder `!data/jeu_or.csv` |
| `DeprecationWarning` venant de joblib ou starlette | Versions des bibliothèques | Sans conséquence pour le TP |
