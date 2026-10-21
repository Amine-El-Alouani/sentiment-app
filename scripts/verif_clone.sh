#!/usr/bin/env bash
# Rejoue le test de l'enseignant : clone frais, installation, diagnostic, tests.
# Usage : bash scripts/verif_clone.sh https://github.com/<organisation>/sentiment-app.git
set -euo pipefail

URL="${1:-}"
if [ -z "$URL" ]; then
  echo "Usage : bash scripts/verif_clone.sh <url du dépôt GitHub>"
  exit 2
fi

DOSSIER=$(mktemp -d)
trap 'rm -rf "$DOSSIER"' EXIT
echo "Clone frais dans $DOSSIER"

git clone -q "$URL" "$DOSSIER/verif"
cd "$DOSSIER/verif"

PY=$(command -v python3.11 || command -v python3 || command -v python)
"$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

echo
echo "=== Diagnostic ==="
python scripts/check_setup.py || true
echo
echo "=== Tests ==="
python -m pytest -q || true
echo
echo "Attendu : 0 erreur(s) au diagnostic et 38 passed."
echo "Le dossier temporaire est supprimé automatiquement."
