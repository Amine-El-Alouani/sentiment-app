#!/usr/bin/env bash
# Mise en place complète du poste pour le TP1 (Linux / macOS / Git Bash).
# Usage : bash scripts/setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "1/4 Vérification de Python 3.11"
PY=$(command -v python3.11 || command -v python3 || command -v python)
"$PY" --version

echo "2/4 Création de l'environnement virtuel"
[ -d .venv ] || "$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate

echo "3/4 Installation des dépendances"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip freeze > requirements.lock

echo "4/4 Diagnostic"
python scripts/check_setup.py
