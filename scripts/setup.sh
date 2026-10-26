#!/usr/bin/env bash
# Mise en place complète du poste pour le TP1 (Linux / macOS / Git Bash).
# Usage : bash scripts/setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "1/4 Vérification de Python"
PY=$(command -v python3 || command -v python)
"$PY" --version

echo "2/4 Création de l'environnement virtuel"
[ -d .venv ] || "$PY" -m venv .venv
VENV_PY=.venv/bin/python
if [ ! -x "$VENV_PY" ]; then
	rm -rf .venv
	"$PY" -m venv .venv
fi

echo "3/4 Installation des dépendances"
"$VENV_PY" -m pip install -r requirements.txt -r requirements-dev.txt

echo "4/4 Diagnostic"
"$VENV_PY" scripts/check_setup.py
