# TP1 : marche à suivre, étape par étape et test par test

Huit étapes, huit contrôles numérotés T0 à T7. À chacun, le résultat attendu est écrit. Ne passez à l'étape suivante que lorsque le contrôle précédent est vert.

## Avant de commencer

Sur votre poste : Python 3.11 (3.10 toléré, évitez 3.12 et 3.13), Git, un éditeur. Un compte GitHub avec l'adresse de l'école.

```bash
python --version      # Windows : py -3.11 --version
git --version
```

Décidez tout de suite qui est le **membre A** (il crée le dépôt et pousse le kit) et qui est le **membre B** (il clone). Les étapes 4 et 5 en dépendent.

## Étape 1. Décompresser le kit (5 min, chacun)

```bash
unzip sentiment-app.zip        # Windows : clic droit, Extraire tout
cd sentiment-app
```

Toutes les commandes se lancent depuis ce dossier, celui qui contient `README.md`.

### Contrôle T0 : le kit est complet

```bash
ls
ls -a | grep gitignore         # Windows PowerShell : ls -Force | findstr gitignore
```

Vous devez voir les fichiers du kit, les sept dossiers, et `.gitignore` (qui ne s'affiche pas avec un `ls` simple).

## Étape 2. Créer l'environnement virtuel (10 min, chacun)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install pandas scikit-learn pytest
```

Votre invite doit maintenant commencer par `(.venv)`. Sinon, rien de ce qui suit ne marchera. À refaire dans chaque nouveau terminal.

### Contrôle T1 : l'état de départ

```bash
pytest -q
```

Attendu : **3 failed, 31 passed, 4 skipped**. Les 3 échecs sont les fiches vides (étape 3), les 4 ignorés attendent le dépôt Git (étapes 4 et 6).

## Étape 3. Remplir les trois fiches de cadrage (50 min, à deux)

Lisez d'abord `docs/cadrage/EXEMPLE-corrige.md`, puis remplissez `cas1-pharmacie.md`, `cas2-reglement.md` et `cas3-avis-negatifs.md`. La grille est rappelée dans `docs/cadrage/GRILLE-DE-DECISION.md`.

Les trois règles que les tests vérifient :

1. une seule case cochée par fiche (`- [x]`) ;
2. la justification cite au moins deux critères par leur lettre : `(a)`, `(b)`, `(c)`, `(d)` ;
3. chaque rubrique obligatoire contient au moins une phrase.

### Contrôle T2 : les fiches passent

```bash
pytest tests/test_cadrage.py -q
```

Attendu : **12 passed**. Les messages d'échec nomment la fiche et la rubrique fautives.

## Étape 4. Créer le dépôt et pousser le kit (15 min, membre A)

Sur github.com : New repository, organisation de l'école, nom `sentiment-app`, **Private**, aucune case cochée. Settings, Collaborators : membre B en **Write**, enseignant en **Read**.

Si Git n'est pas encore configuré sur votre poste :

```bash
git config --global user.name "Prénom Nom"
git config --global user.email "prenom.nom@ecole.ma"
```

```bash
git init
git add -A
git status
```

### Contrôle T3 : rien d'indésirable n'entre dans le dépôt

La sortie de `git status` ne doit contenir **aucune ligne commençant par `.venv/`**. Si c'est le cas, arrêtez-vous : le `.gitignore` manque. Un dépôt où `.venv/` a été commité pèse 300 Mo et le test final restera rouge.

```bash
git commit -m "Semaine 1 : structure du dépôt et kit TP1"
git branch -M main
git remote add origin https://github.com/<organisation>/sentiment-app.git
git push -u origin main
```

Le script `bash scripts/init_depot.sh <url>` fait ces cinq commandes et refuse de continuer si `.venv/` est en attente.

Au premier push, le mot de passe du compte est refusé : il faut un jeton d'accès personnel (GitHub, Settings, Developer settings, Personal access tokens, portée `repo`).

## Étape 5. Installer l'environnement complet (15 min, les deux)

Membre B : acceptez l'invitation reçue par courriel, puis clonez.

```bash
git clone https://github.com/<organisation>/sentiment-app.git
cd sentiment-app
```

Les deux membres :

```bash
bash scripts/setup.sh                                          # Linux, macOS, Git Bash
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1     # Windows
```

Comptez 5 à 10 minutes.

### Contrôle T4 : le diagnostic

```bash
python scripts/check_setup.py
```

Attendu : **0 erreur(s)**. L'avertissement « 1 auteur(s) seulement » est normal ici, il disparaît à l'étape 6.

## Étape 6. Un commit par membre (10 min, chacun)

```bash
git pull
# modifiez votre ligne du tableau du binôme dans README.md
git add README.md
git commit -m "README : ajout de <votre nom> au tableau du binôme"
git push
```

### Contrôle T5 : les deux membres sont comptés

```bash
git shortlog -sn --all
pytest tests/test_git_history.py -q
```

Attendu : deux noms différents, puis **3 passed**.

## Étape 7. Vérification finale (10 min, à deux)

```bash
git pull
python scripts/check_setup.py
pytest -q
```

### Contrôle T6 : tout est vert

Attendu : **0 erreur(s), 0 avertissement(s)** et **38 passed**. Poussez, puis vérifiez que l'onglet Actions de GitHub est vert.

## Étape 8. Refaire le test de l'enseignant (5 min)

La note se joue sur un clone frais.

```bash
bash scripts/verif_clone.sh https://github.com/<organisation>/sentiment-app.git
```

Ou à la main :

```bash
cd /tmp
git clone https://github.com/<organisation>/sentiment-app.git verif
cd verif
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_setup.py
pytest -q
```

### Contrôle T7 : le dépôt tient debout tout seul

Attendu : **0 erreur(s)** et **38 passed**, sans aucune intervention manuelle. Si quelque chose manque, c'est qu'un fichier n'a jamais été poussé.

## Récapitulatif des huit contrôles

| Contrôle | Commande | Résultat attendu |
| --- | --- | --- |
| T0 | `ls` et `ls -a` | Les 7 dossiers, les fichiers du kit, `.gitignore` présent |
| T1 | `pytest -q` | 3 failed, 31 passed, 4 skipped |
| T2 | `pytest tests/test_cadrage.py -q` | 12 passed |
| T3 | `git status` avant le commit | aucune ligne `.venv/` |
| T4 | `python scripts/check_setup.py` | 0 erreur(s) |
| T5 | `git shortlog -sn --all` puis `pytest tests/test_git_history.py -q` | deux noms, puis 3 passed |
| T6 | `check_setup.py` et `pytest -q` | 0 erreur, 0 avertissement, 38 passed, CI verte |
| T7 | la suite complète sur un clone frais | 0 erreur et 38 passed, sans intervention |

## Avant de quitter la salle

- [ ] Les trois fiches `docs/cadrage/cas*.md` sont remplies et poussées
- [ ] Le tableau du binôme dans `README.md` est complété
- [ ] `requirements.lock` est présent dans le dépôt
- [ ] `git shortlog -sn` liste les deux membres
- [ ] `pytest -q` affiche 38 passed
- [ ] L'onglet Actions est vert
- [ ] Le test du clone frais (T7) est passé

En cas de blocage, voir `DEPANNAGE.md`. Pour les commandes Git, voir `AIDE-GIT.md`.

## Pour aller plus loin, une fois le TP rendu

Le dossier `exemples/` contient deux scripts facultatifs qui montrent la suite : `train_sentiment.py` entraîne un classifieur sur les 30 avis du kit (ce que sera la semaine 2) et `app_streamlit.py` affiche une interface de démonstration (semaine 5). Voir `exemples/README.md`. Ils ne sont pas notés.
