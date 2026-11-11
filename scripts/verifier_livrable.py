#!/usr/bin/env python
"""Vérifie les artefacts essentiels du paquet construit."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]


def verifier(condition: bool, message: str) -> bool:
    print(f"[{'OK' if condition else 'ÉCHEC'}] {message}")
    return condition


def main() -> int:
    dist = RACINE / "dist"
    roues = sorted(dist.glob("*.whl"))
    sources = sorted(dist.glob("*.tar.gz"))
    ok = verifier(len(roues) == 1, "une seule roue présente")
    ok &= verifier(len(sources) == 1, "une seule distribution source présente")
    if not roues:
        return 1
    with zipfile.ZipFile(roues[0]) as archive:
        noms = set(archive.namelist())
    ok &= verifier(any(n.endswith("modele/sentiment.joblib") for n in noms), "modèle embarqué dans la roue")
    ok &= verifier("sentiment_app-" in roues[0].name, "nom de roue conforme")
    ok &= verifier((RACINE / "CHANGELOG.md").is_file(), "CHANGELOG.md présent")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())