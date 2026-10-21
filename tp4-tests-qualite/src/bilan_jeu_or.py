#!/usr/bin/env python
"""Bilan du jeu d'or : ce que l'API répond à chacun de vos avis (TP4, étape C).

Usage, depuis la racine du dépôt, modèle entraîné :
  python src/bilan_jeu_or.py
Les chiffres affichés vont dans docs/semaine4.md, partie 4.
"""
import csv
import logging
import sys
from collections import Counter
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
JEU_OR = RACINE / "data" / "jeu_or.csv"
FRANCHES = {"POSITIVE", "NEGATIVE"}


def main() -> int:
    sys.path.insert(0, str(RACINE))
    from fastapi.testclient import TestClient

    from api.main import app

    logging.disable(logging.INFO)  # pas de journal (API, httpx) dans le bilan
    with JEU_OR.open(encoding="utf-8", newline="") as f:
        lignes = [ligne for ligne in csv.DictReader(f) if (ligne.get("text") or "").strip()]
    if not lignes:
        raise SystemExit("data/jeu_or.csv ne contient aucun avis : écrivez vos 20 avis d'abord")

    bilan: Counter[str] = Counter()
    with TestClient(app) as client:
        for ligne in lignes:
            reponse = client.post("/predict", json={"text": ligne["text"]})
            corps = reponse.json()
            label = corps.get("label") if reponse.status_code == 200 else f"refus {reponse.status_code}"
            if label == ligne["attendu"]:
                issue = "juste"
            elif label in FRANCHES:
                declaree = (ligne.get("erreur_connue") or "").strip()
                issue = "erreur franche déclarée" if declaree else "erreur franche"
            elif reponse.status_code == 200:
                issue = "abstention"
            else:
                issue = label
            bilan[issue] += 1
            score = corps.get("score", 0.0) if reponse.status_code == 200 else 0.0
            print(f"{issue:<24} {label!s:<12} {score:.2f}  attendu {ligne['attendu']:<9} {ligne['text'][:55]}")

    print(f"\nBilan sur {len(lignes)} avis : " + ", ".join(f"{k} {v}" for k, v in sorted(bilan.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
