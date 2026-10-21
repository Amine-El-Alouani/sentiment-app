# Démarche à suivre pour le test

Ce dépôt se vérifie de deux façons, qui contrôlent les mêmes choses : `scripts/check_setup.py` parle aux humains (lignes OK, ATTENTION, ERREUR) et `pytest` parle à la machine (38 tests, repris par la CI et par la notation).

Huit contrôles, T0 à T7. Le pas-à-pas complet de la séance est dans `MARCHE-A-SUIVRE.md` ; ce document détaille les tests eux-mêmes.

## T0. Le kit est complet

```bash
ls
ls -a | grep gitignore         # Windows PowerShell : ls -Force | findstr gitignore
```

Les sept dossiers (`app`, `data`, `docs`, `models`, `scripts`, `tests`, `ui`), les fichiers de documentation, `requirements.txt`, `pytest.ini`, et `.gitignore`, qui ne s'affiche pas avec un `ls` simple.

## T1. L'état de départ

```bash
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\Activate.ps1
pip install pandas scikit-learn pytest
pytest -q
```

Attendu : **3 failed, 31 passed, 4 skipped**.

- les 3 échecs sont dans `tests/test_cadrage.py` : les fiches sont vides (partie A) ;
- les 4 tests ignorés attendent un dépôt Git : 3 dans `tests/test_git_history.py`, 1 dans `tests/test_environment.py` ;
- les 31 verts confirment la structure, les paquets et le `.gitignore`.

## T2. Les fiches de cadrage

```bash
pytest tests/test_cadrage.py -q
```

Attendu : **12 passed**. Les quatre contrôles : trois fichiers `docs/cadrage/cas*.md` ; les huit rubriques obligatoires présentes dans chacun ; chaque rubrique remplie (au moins 20 caractères hors consigne) ; exactement une case `- [x]` et au moins deux critères `(a)` à `(d)` cités dans la justification.

## T3. Rien d'indésirable dans le dépôt

```bash
git add -A
git status
```

Aucune ligne commençant par `.venv/`. Le script `bash scripts/init_depot.sh <url>` refuse d'ailleurs de pousser si `.venv/` est en attente.

## T4. Le diagnostic

```bash
python scripts/check_setup.py
```

Cinq blocs (Python, Paquets, Structure, Git, Fiches), puis `N erreur(s), M avertissement(s)`. Code de sortie 1 s'il reste une erreur.

| Ligne | Sens |
| --- | --- |
| `OK` | rien à faire |
| `ATTENTION` | ne bloque pas, mais doit disparaître avant la fin de la séance |
| `ERREUR` | bloque : venv non activé, paquet absent, dossier manquant, pas de dépôt Git, `.venv/` suivi |

## T5. Les deux membres ont commité

```bash
git shortlog -sn --all
pytest tests/test_git_history.py -q
```

Attendu : deux noms distincts, puis **3 passed**. Le message `1 auteur(s) de commits, 2 attendus` signale soit qu'un membre n'a pas poussé, soit que les deux postes partagent le même `user.name`.

## T6. Tout, comme la CI

```bash
pytest -q
```

Attendu : **38 passed** (23 + 12 + 3), et `0 erreur(s), 0 avertissement(s)` au diagnostic. Poussez, puis vérifiez l'onglet Actions : le workflow rejoue ces 38 tests sur une machine neuve, en Python 3.11.

## T7. Le test de l'enseignant

```bash
bash scripts/verif_clone.sh https://github.com/<organisation>/sentiment-app.git
```

Le script clone dans un dossier temporaire, installe `requirements.txt`, lance le diagnostic et les tests, puis nettoie. Attendu : **0 erreur(s)** et **38 passed**, sans aucune intervention manuelle.

À la main, si vous préférez voir chaque commande :

```bash
cd /tmp
git clone https://github.com/<organisation>/sentiment-app.git verif
cd verif
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_setup.py
pytest -q
```

## Les trois états de référence

| État | check_setup.py | pytest |
| --- | --- | --- |
| Kit décompressé, pas de dépôt Git, fiches vides | 1 erreur, 3 avertissements | 3 failed, 31 passed, 4 skipped |
| Dépôt initialisé, un seul auteur, fiches vides | 0 erreur, 4 avertissements | 4 failed, 34 passed |
| Fin du TP : fiches remplies, deux auteurs | 0 erreur, 0 avertissement | 38 passed |

En cas d'échec, `DEPANNAGE.md` liste les messages et leur correction.
