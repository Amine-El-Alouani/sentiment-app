#!/usr/bin/env python
"""Crée une nouvelle fiche de cadrage à partir du modèle.

Usage : python scripts/new_cadrage.py cas4-mon-cas "Titre lisible du cas"
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "cadrage" / "TEMPLATE.md"


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    slug, title = sys.argv[1], sys.argv[2]
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        print("Le nom de fichier ne doit contenir que des minuscules, chiffres et tirets.")
        return 2
    target = TEMPLATE.parent / f"{slug}.md"
    if target.exists():
        print(f"{target} existe déjà.")
        return 1
    target.write_text(TEMPLATE.read_text(encoding="utf-8").replace("<nom du cas>", title), encoding="utf-8")
    print(f"Fiche créée : {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
