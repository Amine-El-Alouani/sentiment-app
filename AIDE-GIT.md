# Aide-mémoire Git pour le TP1

## Ce que fait Git, en trois phrases

Git enregistre l'état de vos fichiers à des instants que vous choisissez : ce sont les commits. L'historique est la suite de ces commits, et rien n'y est jamais écrasé, ce qui permet de revenir en arrière et de comparer. GitHub héberge une copie de ce même dépôt, qui sert de point de rendez-vous entre les deux membres du binôme.

## Les trois zones

| Zone | Ce qu'elle contient | Comment y entrer |
| --- | --- | --- |
| Dossier de travail | Vos fichiers tels qu'ils sont sur le disque | Vous éditez |
| Index (zone d'attente) | Ce qui partira dans le prochain commit | `git add <fichier>` |
| Historique | Les commits, définitifs | `git commit -m "message"` |

`git status` dit où en est chaque fichier des trois. C'est la commande à lancer en cas de doute, toujours.

## Les commandes du TP1

| Commande | Ce qu'elle fait |
| --- | --- |
| `git config --global user.name "Prénom Nom"` | Définit l'auteur des commits sur ce poste, une fois pour toutes |
| `git init` | Crée le dépôt local (le dossier caché `.git/`) |
| `git status` | Liste les fichiers modifiés, en attente, non suivis |
| `git add -A` | Met tout en attente, sauf ce qu'exclut `.gitignore` |
| `git add README.md` | Met un seul fichier en attente |
| `git commit -m "..."` | Enregistre l'index comme un commit |
| `git branch -M main` | Renomme la branche courante en `main` |
| `git remote add origin <url>` | Enregistre l'adresse GitHub sous le nom `origin` |
| `git push -u origin main` | Envoie `main` vers GitHub et lie les deux |
| `git clone <url>` | Télécharge le dépôt avec tout son historique |
| `git pull` | Récupère les commits de l'autre membre et les fusionne |
| `git push` | Envoie vos nouveaux commits |
| `git log --oneline` | Historique compact, un commit par ligne |
| `git shortlog -sn --all` | Nombre de commits par auteur |
| `git restore <fichier>` | Annule vos modifications locales sur ce fichier |
| `git rm -r --cached .venv` | Retire `.venv/` du suivi sans supprimer le dossier |

## Résoudre un conflit sur README.md

Les deux membres ont modifié le tableau du binôme en même temps. Après `git pull`, le fichier contient :

```text
<<<<<<< HEAD
| Membre A | Sara | @sara | |
=======
| Membre B | Omar | @omar | |
>>>>>>> origin/main
```

Gardez les deux lignes, supprimez les trois marqueurs, puis :

```bash
git add README.md
git commit -m "README : fusion des deux lignes du binôme"
git push
```

Un conflit n'est pas une erreur : Git refuse simplement de choisir à votre place.

## Ce que Git ne fait pas

Il n'enregistre rien tout seul : sans `add` puis `commit`, votre travail n'est que sur votre disque. Il gère mal les gros fichiers binaires, d'où le `.gitignore` qui exclut `.venv/` et `models/`, et d'où DVC en semaine 7 pour les données et les modèles.

## Trois règles pour ne pas perdre de temps

1. `git status` avant chaque commit, et lisez la sortie.
2. `git pull` avant chaque `git push`.
3. Ne commitez jamais un dossier que vous pouvez reconstruire par une commande.
