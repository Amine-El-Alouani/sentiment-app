#!/usr/bin/env bash
# Initialise le dépôt local et le pousse sur GitHub (étape 4 du TP1, membre A).
# Usage : bash scripts/init_depot.sh https://github.com/<organisation>/sentiment-app.git
set -euo pipefail
cd "$(dirname "$0")/.."

URL="${1:-}"
if [ -z "$URL" ]; then
  echo "Usage : bash scripts/init_depot.sh <url du dépôt GitHub>"
  exit 2
fi

if ! git config user.name > /dev/null 2>&1 && ! git config --global user.name > /dev/null 2>&1; then
  echo "ERREUR : identité Git non configurée."
  echo '  git config --global user.name "Prénom Nom"'
  echo '  git config --global user.email "prenom.nom@ecole.ma"'
  exit 1
fi

if [ -d .git ]; then
  echo "Un dépôt Git existe déjà ici. Rien à initialiser."
else
  echo "1/5 git init"
  git init -q
fi

echo "2/5 git add -A"
git add -A

# Garde-fou : refuser d'aller plus loin si .venv/ est sur le point d'être commité.
if git diff --cached --name-only | grep -q "^\.venv/"; then
  echo "ERREUR : .venv/ est en attente de commit."
  echo "Vérifiez que .gitignore contient .venv/ puis relancez :"
  echo "  git rm -r --cached .venv"
  exit 1
fi
echo "      OK : .venv/ n'est pas en attente"

echo "3/5 git commit"
git commit -q -m "Semaine 1 : structure du dépôt et kit TP1" || echo "      (rien à commiter)"

echo "4/5 branche main et dépôt distant"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$URL"

echo "5/5 git push"
git push -u origin main

echo
echo "Terminé. Vérifiez sur GitHub que .venv/ n'apparaît pas,"
echo "puis ajoutez l'autre membre en Write et l'enseignant en Read."
