# TP1 : cadrer une application IA et préparer l'environnement

**Module :** Développement et déploiement d'applications intelligentes (44 h, 11 semaines)
**Auteur :** A. Larhlimi
**Séance :** semaine 1 · durée 2 h · travail en binôme (membre A et membre B)
**Kit :** `sentiment-app.zip`, également sur `https://github.com/larhlimi2023/sentiment-app.git`

## Objectifs

À la fin de ce TP, chaque binôme dispose :

1. de trois fiches de cadrage argumentées, une par mini-cas ;
2. d'un dépôt GitHub privé `sentiment-app`, structuré, où les deux membres ont poussé au moins un commit ;
3. d'un environnement Python reproductible, vérifié par `python scripts/check_setup.py` et par `pytest`.

Ce dépôt est le point de départ des dix semaines suivantes : rien de ce que vous faites aujourd'hui ne sera jeté.

## Ce que contient ce kit

| Fichier | Rôle |
| --- | --- |
| `README.md` | Porte d'entrée : installation en trois commandes, structure, tableau du binôme |
| `MARCHE-A-SUIVRE.md` | Le pas à pas de la séance : huit étapes, huit contrôles numérotés T0 à T7 |
| `TESTS.md` | La démarche de test en détail et les trois états de référence |
| `AIDE-GIT.md` | Les commandes Git du TP et la résolution d'un conflit |
| `DEPANNAGE.md` | Les messages d'erreur et leur correction |
| `requirements.txt` | Dépendances de tout le semestre, versions figées |
| `.gitignore`, `.env.example`, `.editorconfig`, `pytest.ini` | Configuration, à garder telle quelle |
| `.vscode/` | Interpréteur `.venv` et pytest préconfigurés |
| `Makefile` | Raccourcis : `make setup`, `make check`, `make test` (Linux, macOS, Git Bash) |
| `docs/cadrage/cas1-pharmacie.md`, `cas2-reglement.md`, `cas3-avis-negatifs.md` | **Les trois fiches à remplir** (partie A) |
| `docs/cadrage/TEMPLATE.md`, `EXEMPLE-corrige.md` | Le modèle vierge et un exemple rempli, pour calibrer le niveau |
| `docs/cadrage/GRILLE-DE-DECISION.md` | Feuille de rappel : les quatre critères et l'arbre de choix |
| `docs/cadrage/BANQUE-DE-CAS.md` | Douze cas de rechange : entreprise, citoyens, université, État |
| `scripts/setup.sh`, `setup.ps1` | Mise en place du poste (Linux et macOS, Windows) |
| `scripts/check_setup.py` | Diagnostic lisible de l'environnement |
| `scripts/init_depot.sh` | Initialise et pousse le dépôt, en refusant de commiter `.venv/` |
| `scripts/verif_clone.sh` | Rejoue le test de l'enseignant sur un clone frais |
| `scripts/new_cadrage.py` | Crée une fiche supplémentaire à partir du modèle |
| `tests/` | 38 tests : environnement (23), cadrage (12), historique Git (3) |
| `.github/workflows/ci.yml` | Intégration continue : diagnostic et `pytest` à chaque push |
| `data/sample_reviews.csv` | Trente avis d'exemple, utiles dès la semaine 2 |
| `notebooks/TP1-colab.ipynb` | Le même TP sur Colab, sans installation |
| `exemples/` | Facultatif, non noté : ce que seront les semaines 2 et 5 |

## Partie A : cadrage (50 min, en binôme)

### A1. Lire l'exemple corrigé (5 min)

Ouvrir `docs/cadrage/EXEMPLE-corrige.md`. Chaque rubrique tient en une à trois phrases, et la justification cite les critères de la grille par leur lettre : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur.

### A2. Remplir les trois fiches (40 min)

| Fiche | Cas | Indices à discuter |
| --- | --- | --- |
| `cas1-pharmacie.md` | Une pharmacie veut détecter les ordonnances incomplètes | Les champs obligatoires sont-ils connus ? Que coûte une ordonnance validée à tort ? Données de santé |
| `cas2-reglement.md` | Une école veut répondre aux questions sur le règlement intérieur | Les documents existent déjà. La réponse doit-elle être vérifiable ? A-t-on des questions étiquetées ? |
| `cas3-avis-negatifs.md` | Un site e-commerce veut prioriser les avis négatifs | Des milliers d'avis. Peut-on les étiqueter ? Que coûte un avis mal classé ? |

Règles : une seule case cochée (`- [x]`) ; la justification cite au moins deux critères par leur lettre ; chaque rubrique obligatoire contient au moins une phrase. Deux approches peuvent se défendre pour un même cas : c'est la justification qui est notée, pas la case cochée.

Un membre tient le clavier, l'autre parcourt l'arbre de choix et conteste : logique connue et stable ? règles métier ; données étiquetées ? machine learning ; réponse tirée de documents ? RAG ; sinon génératif seul. Inversez les rôles à chaque fiche.

### A3. Vérifier (5 min)

```bash
pytest tests/test_cadrage.py -q      # attendu : 12 passed
```

Note : au tout premier `pytest -q`, avant d'avoir rempli les fiches, le résultat attendu est `3 failed, 31 passed, 4 skipped`. Ce rouge est voulu : il décrit le travail de la séance.

## Partie B : environnement et dépôt (70 min)

### B1. Outils système (10 min, chacun)

```bash
python --version      # 3.11.x attendu, 3.10 toléré
git --version
code --version        # VS Code, facultatif mais recommandé
```

Windows : installer Python depuis python.org en cochant « Add python.exe to PATH » ; utiliser `py -3.11` si plusieurs versions cohabitent.

### B2. Créer le dépôt GitHub (10 min, membre A)

1. Dans l'organisation GitHub de l'école : « New repository », nom `sentiment-app`, visibilité **Private**, sans README ni `.gitignore`.
2. Settings › Collaborators : le membre B en **Write**, l'enseignant en **Read**.
3. Copier l'URL HTTPS de clonage.

### B3. Initialiser le dépôt à partir du kit (15 min, membre A)

```bash
cd sentiment-app
git init
git add -A
git commit -m "Semaine 1 : structure du dépôt et kit TP1"
git branch -M main
git remote add origin https://github.com/votre-compte/sentiment-app.git
git push -u origin main
```

Si Git refuse le commit faute d'identité : `git config --global user.name "Prénom Nom"` et `git config --global user.email "prenom.nom@ecole.ma"`. Chaque membre utilise son propre nom : c'est ce nom que `git shortlog` compte en B6.

Remplacez `votre-compte` par votre compte ou organisation GitHub : les chevrons d'un exemple laissés dans l'URL donnent une erreur 400. Au premier push, le mot de passe du compte est refusé, il faut un jeton d'accès personnel (Settings, Developer settings, Personal access tokens, portée `repo`).

Vérifier sur GitHub que `.venv/` n'apparaît pas et que `docs/cadrage/` contient les fiches.

### B4. Installer l'environnement (15 min, chacun)

Le membre B clone, puis chacun lance le script de mise en place ; le membre A le lance dans son dossier existant.

```bash
git clone https://github.com/votre-compte/sentiment-app.git
cd sentiment-app
bash scripts/setup.sh                                          # Linux, macOS, Git Bash
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1     # Windows
```

Résultat attendu : `0 erreur(s)` au diagnostic. `requirements.lock` est régénéré sur chaque poste : un seul membre le commite.

### B5. Un commit par membre (10 min, chacun)

```bash
git pull
git add README.md
git commit -m "README : ajout de <nom> au tableau du binôme"
git push
```

En cas de conflit sur `README.md` : garder les deux lignes du tableau, supprimer les marqueurs `<<<<<<<`, `=======`, `>>>>>>>`, puis `git add`, `git commit`, `git push`.

### B6. Vérification finale (10 min, à deux)

```bash
git pull
python scripts/check_setup.py        # attendu : 0 erreur(s), 0 avertissement(s)
pytest -q                            # attendu : 38 passed
```

Pousser une dernière fois et vérifier que la CI est verte dans l'onglet Actions. La démarche de test complète, avec les résultats attendus à chaque étape, est dans `TESTS.md`.

## Livrables (sur la branche `main`, à la fin de la séance)

- [ ] `docs/cadrage/cas1-pharmacie.md`, `cas2-reglement.md`, `cas3-avis-negatifs.md` remplies
- [ ] `README.md` avec le tableau du binôme complété
- [ ] `requirements.lock` généré
- [ ] Structure de dossiers conforme
- [ ] Un commit par membre visible dans `git shortlog -sn`
- [ ] CI verte sur GitHub

## Grille de notation (TP1 sur 10)

| Critère | Points | Vérification |
| --- | --- | --- |
| Fiches de cadrage : approche justifiée par deux critères, rubriques remplies | 4 | Lecture + `pytest tests/test_cadrage.py` |
| Dépôt clonable, `pip install -r requirements.txt` sans erreur | 2 | Clone frais par l'enseignant |
| Structure et `.gitignore` conformes, `.venv/` absent de l'historique | 2 | `pytest tests/test_environment.py` |
| Un commit par membre, messages de commit explicites | 2 | `git shortlog -sn`, `git log --oneline` |

## Pièges fréquents

| Symptôme | Cause | Correction |
| --- | --- | --- |
| Le dépôt pèse 300 Mo | `.venv/` commité | `git rm -r --cached .venv`, vérifier `.gitignore`, commit |
| `ModuleNotFoundError: pandas` | venv non activé | `source .venv/bin/activate`, puis `which python` dans `.venv` |
| `test_virtualenv_active` échoue | pytest lancé hors du venv | activer le venv, ou `.venv/bin/python -m pytest` |
| `2 attendus (un par membre du binôme)` | un seul membre a poussé | chaque membre fait un vrai commit (B5) |
| `la justification doit citer au moins deux critères` | justification sans `(a)`, `(b)`... | citer les lettres explicitement |
| `pip install` très long | sentence-transformers et mlflow sont lourds | `pip install pandas scikit-learn pytest` d'abord, le reste en fin de séance |
