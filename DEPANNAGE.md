# Dépannage du TP1

Cherchez votre message dans la première colonne. Les quatre situations les plus fréquentes sont détaillées après le tableau.

| Message ou symptôme | Cause | Correction |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'pandas'` | venv non activé, ou pip d'un autre Python | Activer le venv ; `which python` (Windows : `where python`) doit afficher un chemin contenant `.venv` |
| `test_virtualenv_active` échoue | pytest lancé hors du venv | Activer le venv, ou `.venv/bin/python -m pytest` |
| `No matching distribution found for scikit-learn==1.5.*` | Python 3.12 ou 3.13 | Installer Python 3.11, supprimer `.venv`, le recréer avec `py -3.11 -m venv .venv` |
| `Activate.ps1 cannot be loaded ... running scripts is disabled` | politique PowerShell par défaut | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, ou lancer avec `-ExecutionPolicy Bypass` |
| `python` ouvre le Microsoft Store | alias d'exécution Windows | Paramètres, Applications, Alias d'exécution : désactiver `python.exe`, ou utiliser `py` |
| `git: command not found` | Git absent ou pas dans le PATH | Installer Git, puis fermer et rouvrir le terminal |
| `Please tell me who you are` au commit | identité Git non configurée | `git config --global user.name` et `user.email` |
| `Support for password authentication was removed` | GitHub refuse le mot de passe du compte | Créer un jeton d'accès personnel (portée `repo`) et le coller à la place |
| `403 Forbidden` au push | invitation de collaborateur pas acceptée | Accepter l'invitation reçue par courriel, puis repousser |
| `rejected, non-fast-forward` | l'autre membre a poussé entre-temps | `git pull`, résoudre le conflit éventuel, `git push` |
| `Your local changes would be overwritten: requirements.lock` | le lock a été régénéré sur votre poste | `git restore requirements.lock`, puis `git pull` |
| `1 auteur(s) de commits, 2 attendus` | un seul membre a poussé, ou même `user.name` sur les deux postes | Chaque membre configure son nom et refait un commit |
| `rubriques vides ou trop courtes : ...` | une rubrique de fiche est vide | Remplir la rubrique nommée dans le message |
| `cocher exactement une approche` | zéro ou deux cases `- [x]` | Une seule approche par fiche |
| `la justification doit citer au moins deux critères` | les lettres `(a)` à `(d)` manquent | Les écrire explicitement dans la justification |
| `.venv/ a été commité au moins une fois` | `.venv/` est entré dans l'historique | Voir la situation 1 ci-dessous |
| `4 skipped` alors que le dépôt est sur GitHub | pytest lancé hors du dossier du dépôt | Se placer à la racine du dépôt cloné |
| `pip install` interminable | les paquets du semestre sont lourds | Laisser tourner ; en attendant, `pip install pandas scikit-learn pytest` suffit pour tester |
| Accents cassés dans le terminal Windows (`Ã©`) | invite `cmd` en page de code cp1252 | `chcp 65001`, ou utiliser PowerShell ou Windows Terminal |

## Situation 1. Le dépôt pèse 300 Mo

Symptôme : `git push` dure plusieurs minutes, GitHub refuse un fichier de plus de 100 Mo, et le diagnostic affiche `ERREUR .venv/ est suivi par Git`.

Cause : `.venv/` a été ajouté au dépôt, parce que `.gitignore` manquait ou avait été renommé au moment du `git add -A`.

Le test `test_venv_never_committed` lit tout l'historique : un `git rm -r --cached .venv` ne suffit donc pas, il reste rouge. Au TP1, où l'historique ne contient que quelques commits, la correction est de recommencer le dépôt :

```bash
rm -rf .git                      # Windows : supprimer le dossier caché .git
# vérifier que .gitignore contient bien .venv/
git init
git add -A
git status                       # aucune ligne .venv/
git commit -m "Semaine 1 : structure du dépôt et kit TP1"
git branch -M main
git remote add origin https://github.com/<organisation>/sentiment-app.git
git push --force -u origin main
```

L'autre membre reclone ensuite. Prévenez l'enseignant : un `push --force` efface l'historique distant.

## Situation 2. pandas est installé, mais Python ne le trouve pas

Symptôme : `pip install` s'est terminé sans erreur, et `python scripts/check_setup.py` affiche `ERREUR aucun environnement virtuel actif` puis `ERREUR pandas absent`.

Cause habituelle : vous avez installé dans un terminal, puis ouvert VS Code, dont le terminal intégré démarre sans le venv. Variante : `pip` répond à un Python et `python` à un autre.

Diagnostic :

```bash
which python && which pip        # Windows : where python && where pip
python -c "import sys; print(sys.prefix)"
```

Les trois doivent pointer dans `.venv`. Correction : réactiver le venv, et dans VS Code choisir l'interpréteur `.venv` (commande « Python: Select Interpreter »). Le kit contient déjà un `.vscode/settings.json` qui le fait pour vous. Réflexe à prendre : écrire `python -m pip install ...` plutôt que `pip install ...`.

## Situation 3. Python 3.13 refuse d'installer les paquets

Symptôme : le diagnostic avertit `version 3.13 : le cours cible 3.11`, puis `pip install -r requirements.txt` échoue sur `scikit-learn==1.5.*`, ou tente une compilation et s'arrête faute de compilateur C.

Cause : les versions figées du cours n'ont pas de paquet précompilé pour cette version de Python.

Correction : installer Python 3.11 à côté (les deux versions cohabitent sans conflit), supprimer `.venv`, le recréer avec `py -3.11 -m venv .venv` (macOS et Linux : `python3.11 -m venv .venv`), puis relancer `scripts/setup`. Ne modifiez pas `requirements.txt` : les deux membres doivent avoir les mêmes versions.

## Situation 4. Le push est refusé

Deux messages se ressemblent mais n'ont pas la même cause.

`Support for password authentication was removed` est un problème d'authentification : GitHub ne sait pas qui vous êtes. Créez un jeton d'accès personnel et collez-le à la place du mot de passe ; Git Credential Manager le mémorise ensuite.

`403 Forbidden` est un problème d'autorisation : GitHub sait qui vous êtes, mais vous n'avez pas le droit d'écrire. Le membre A doit vous avoir ajouté en Write, et vous devez avoir accepté l'invitation reçue par courriel.

## Si rien de tout cela ne marche

Appelez l'enseignant avec trois éléments : la commande exacte que vous avez lancée, le message complet, et la sortie de `python scripts/check_setup.py`. Ces trois éléments suffisent presque toujours à identifier la cause en une minute.
