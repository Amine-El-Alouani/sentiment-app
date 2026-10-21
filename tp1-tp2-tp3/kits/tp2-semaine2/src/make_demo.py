#!/usr/bin/env python
"""Génère un jeu de démonstration d'avis en français, déterministe.

290 avis : 80 nettement positifs, 80 nettement négatifs, 100 mitigés
(le sentiment qui compte est celui qui conclut la phrase) et 30 neutres
rattachés à la classe la plus proche. Les avis mitigés sont volontaires :
ils font commettre au modèle quelques erreurs instructives.

Usage : python src/make_demo.py
Produit : data/demo_reviews.csv
"""
import csv
import random
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "data" / "demo_reviews.csv"
GRAINE = 42

POSITIFS = [
    "Service impeccable et livraison en avance",
    "Produit conforme à la description, très satisfait",
    "Excellent rapport qualité prix",
    "Emballage soigné et finitions propres",
    "Prise en main immédiate, notice claire",
    "Le vendeur a répondu en moins d'une heure",
    "Je recommande sans hésiter",
    "Solide, léger, exactement ce que je cherchais",
]
NEGATIFS = [
    "Produit cassé à l'arrivée",
    "Aucune réponse du service client",
    "Commande jamais reçue et remboursement en attente",
    "Se casse au bout de deux utilisations",
    "Notice incompréhensible et pièces manquantes",
    "Taille trop petite et retour payant",
    "Application qui plante à chaque ouverture",
    "Facture erronée, aucun geste commercial",
]
ATTENUATIONS = ["au début", "les premiers jours", "sur le papier", "à la livraison", "au déballage"]
RETOURNEMENTS = ["mais finalement", "sauf que ensuite", "puis rapidement", "avant que", "jusqu'à ce que"]
NEUTRES = [
    "Reçu dans les délais annoncés",
    "Conforme à la fiche produit",
    "Rien de particulier à signaler",
    "Usage standard, sans surprise",
    "Livré, monté, utilisé",
]


def phrases_nettes(modeles, etiquette, nombre, rng):
    suffixes = ["", ", vraiment", ", comme prévu", " pour ce prix", " cette fois"]
    return [(f"{rng.choice(modeles)}{rng.choice(suffixes)}.", etiquette) for _ in range(nombre)]


def phrases_mitigees(nombre, rng):
    """Deux moitiés opposées : l'étiquette suit la seconde, celle qui conclut."""
    lignes = []
    for i in range(nombre):
        if i % 2 == 0:
            debut, fin, etiquette = rng.choice(POSITIFS), rng.choice(NEGATIFS), "negative"
        else:
            debut, fin, etiquette = rng.choice(NEGATIFS), rng.choice(POSITIFS), "positive"
        lignes.append((f"{debut} {rng.choice(ATTENUATIONS)}, {rng.choice(RETOURNEMENTS)} {fin.lower()}.", etiquette))
    return lignes


def phrases_neutres(nombre, rng):
    lignes = []
    for i in range(nombre):
        base = rng.choice(NEUTRES)
        if i % 2 == 0:
            lignes.append((f"{base}, {rng.choice(POSITIFS).lower()}.", "positive"))
        else:
            lignes.append((f"{base}, {rng.choice(NEGATIFS).lower()}.", "negative"))
    return lignes


def main() -> int:
    rng = random.Random(GRAINE)
    lignes = (
        phrases_nettes(POSITIFS, "positive", 80, rng)
        + phrases_nettes(NEGATIFS, "negative", 80, rng)
        + phrases_mitigees(100, rng)
        + phrases_neutres(30, rng)
    )
    rng.shuffle(lignes)
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    with SORTIE.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["review", "label"])
        w.writerows(lignes)
    positifs = sum(1 for _, e in lignes if e == "positive")
    print(f"{len(lignes)} avis écrits dans {SORTIE.relative_to(RACINE)}")
    print(f"  {positifs} positifs, {len(lignes) - positifs} négatifs")
    print("  dont 100 avis mitigés et 30 neutres, volontairement difficiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
