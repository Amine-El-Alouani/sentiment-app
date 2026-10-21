#!/usr/bin/env python
"""Relève des dépôts des binômes : un tableau de vérification par TP, en une commande.

Usage, dans l'environnement virtuel du cours (activé) :
  python releve_binomes.py binomes.csv --tp 3
  python releve_binomes.py binomes.csv --tp 4 --tests
  python releve_binomes.py binomes.csv --tp 4 --tests --date-limite "2026-10-25 23:59"
  python releve_binomes.py binomes.csv --tp 5 --tests

binomes.csv : deux colonnes, binome et depot (l'adresse du dépôt GitHub).
Chaque dépôt est recloné à neuf dans releve/<binome>/. Avec --date-limite, la relève porte sur
le dernier commit avant cette date, et les commits plus tardifs sont comptés à part.
Avec --tests, le script rejoue les tests du dépôt : il exécute donc le code des étudiants,
dans l'environnement courant, comme le fait la CI.
Produit releve/releve-tpN.md (à lire) et releve/releve-tpN.csv (pour un tableur).
"""
import argparse
import csv
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ATTENDU = {1: "38 passed", 2: "42 passed", 3: "48 passed", 4: "aucun failed", 5: "aucun failed"}
INTERDITS = [r"(^|/)\.venv/", r"\.joblib$", r"(^|/)data/demo_reviews\.csv$", r"(^|/)\.env$"]
TESTS_DU_KIT = ["tests/test_environment.py", "tests/test_cadrage.py", "tests/test_git_history.py",
                "tests/test_model.py", "tests/test_api.py", "tests/test_jeu_or.py",
                "tests/test_client.py", "tests/test_interface.py"]
FICHES = ["cas1-pharmacie.md", "cas2-reglement.md", "cas3-avis-negatifs.md"]


def executer(dossier: Path, *commande: str) -> subprocess.CompletedProcess:
    return subprocess.run(list(commande), cwd=dossier, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def git(dossier: Path, *args: str) -> str:
    return executer(dossier, "git", *args).stdout.strip()


def supprimer(dossier: Path) -> None:
    """rmtree qui passe aussi sur les fichiers en lecture seule de .git (Windows)."""
    def deverrouiller(fonction, chemin, _):
        os.chmod(chemin, stat.S_IWRITE)
        fonction(chemin)
    if dossier.exists():
        shutil.rmtree(dossier, onerror=deverrouiller)


def livrables_manquants(d: Path, tp: int) -> list[str]:
    manque = []
    fiches = [f for f in FICHES if (d / "docs" / "cadrage" / f).is_file()]
    if len(fiches) < 3:
        manque.append(f"fiches {len(fiches)}/3")
    for f in fiches:
        if (d / "docs" / "cadrage" / f).read_text(encoding="utf-8", errors="replace").count("- [x]") != 1:
            manque.append(f"{f} : une seule case cochée attendue")
    if tp >= 2:
        if not (d / "models" / "metrics.json").is_file():
            manque.append("metrics.json")
        semaine2 = d / "docs" / "semaine2.md"
        if not semaine2.is_file() or len(semaine2.read_text(encoding="utf-8", errors="replace").strip()) < 80:
            manque.append("semaine2.md")
    if tp >= 3:
        if not (d / "api" / "main.py").is_file():
            manque.append("api/")
        semaine3 = d / "docs" / "semaine3.md"
        if not semaine3.is_file() or "…" in semaine3.read_text(encoding="utf-8", errors="replace"):
            manque.append("semaine3.md à compléter")
    if tp >= 4:
        jeu = d / "data" / "jeu_or.csv"
        lignes = list(csv.DictReader(jeu.open(encoding="utf-8"))) if jeu.is_file() else []
        lignes = [ligne for ligne in lignes if (ligne.get("text") or "").strip()]
        difficiles = [ligne for ligne in lignes if (ligne.get("difficulte") or "").strip()]
        if len(lignes) < 20 or len(difficiles) < 5:
            manque.append(f"jeu d'or {len(lignes)}/20 avis, {len(difficiles)}/5 difficiles")
        semaine4 = d / "docs" / "semaine4.md"
        if not semaine4.is_file() or "…" in semaine4.read_text(encoding="utf-8", errors="replace"):
            manque.append("semaine4.md à compléter")
        if not (d / ".pre-commit-config.yaml").is_file():
            manque.append("pre-commit")
    if tp >= 5:
        if not (d / "ui" / "app.py").is_file() or not (d / "ui" / "client.py").is_file():
            manque.append("ui/")
        semaine5 = d / "docs" / "semaine5.md"
        if not semaine5.is_file() or "…" in semaine5.read_text(encoding="utf-8", errors="replace"):
            manque.append("semaine5.md à compléter")
    return manque


def resume_pytest(sortie: str) -> str:
    lignes = [ligne for ligne in sortie.splitlines() if re.search(r"\d+ (passed|failed|error)", ligne)]
    return lignes[-1].strip("= ").split(" in ")[0] if lignes else "pytest n'a rien rendu"


def rejouer(d: Path, tp: int) -> dict[str, str]:
    py = sys.executable
    resultat: dict[str, str] = {}
    if tp >= 2:
        executer(d, py, "src/make_demo.py")
        entrainement = executer(d, py, "src/train.py")
        f1 = re.search(r"F1 macro[^0-9]*([0-9.]+)", entrainement.stdout)
        resultat["F1"] = f1.group(1) if f1 else "échec de l'entraînement"
    commande = [py, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
    if tp >= 4:
        commande += ["--cov=api", "--cov-report=term"]
    tests = executer(d, *commande)
    resultat["pytest"] = resume_pytest(tests.stdout + tests.stderr)
    if tp >= 4:
        total = re.search(r"^TOTAL\s.*?(\d+%)\s*$", tests.stdout, flags=re.M)
        resultat["couverture"] = total.group(1) if total else "?"
        ruff = executer(d, py, "-m", "ruff", "check", ".")
        resultat["ruff"] = "muet" if ruff.returncode == 0 else (re.findall(r"Found \d+ error", ruff.stdout) or ["erreurs"])[0]
        mypy = executer(d, py, "-m", "mypy", "api")
        resultat["mypy"] = "muet" if mypy.returncode == 0 else mypy.stdout.strip().splitlines()[-1][:60]
    return resultat


def relever(binome: str, url: str, args: argparse.Namespace, racine: Path) -> dict[str, str]:
    d = racine / re.sub(r"[^\w.-]", "_", binome)
    supprimer(d)
    clone = subprocess.run(["git", "clone", "-q", url, str(d)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
    ligne = {"binome": binome, "depot": url}
    if clone.returncode != 0:
        ligne["remarques"] = "clone impossible : " + (clone.stderr.strip().splitlines() or ["?"])[-1]
        return ligne

    cible = "HEAD"
    if args.date_limite:
        cible = git(d, "rev-list", "-1", f"--before={args.date_limite}", "HEAD")
        if not cible:
            ligne["remarques"] = "aucun commit avant la date limite"
            return ligne
        ligne["après la limite"] = git(d, "rev-list", "--count", f"{cible}..HEAD")
        git(d, "checkout", "-q", cible)
    ligne["commit"] = git(d, "log", "-1", "--format=%h %ad", "--date=format:%Y-%m-%d %H:%M")

    auteurs = [a.split("\t", 1)[1] for a in git(d, "shortlog", "-sn", "HEAD").splitlines() if "\t" in a]
    ligne["auteurs"] = f"{len(auteurs)} : {', '.join(auteurs)}"
    suivis = git(d, "ls-files").splitlines()
    interdits = [f for f in suivis if any(re.search(m, f) for m in INTERDITS)]
    ligne["fichiers interdits"] = ", ".join(sorted({f.split("/")[0] if f.startswith(".venv") else f for f in interdits})) or "aucun"
    ligne["livrables"] = "; ".join(livrables_manquants(d, args.tp)) or "complets"
    modifies = []
    for test in TESTS_DU_KIT:
        if test in suivis:
            n = len(git(d, "log", "--format=%h", "--", test).splitlines())
            if n > 1:
                modifies.append(f"{Path(test).name} ({n} commits)")
    ligne["tests du kit retouchés"] = ", ".join(modifies) or "non"
    if args.tests:
        ligne.update(rejouer(d, args.tp))
    if len(auteurs) < 2:
        ligne["remarques"] = (ligne.get("remarques", "") + " un seul auteur").strip()
    return ligne


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("liste", help="binomes.csv : colonnes binome et depot")
    parser.add_argument("--tp", type=int, choices=[1, 2, 3, 4, 5], required=True)
    parser.add_argument("--tests", action="store_true", help="rejouer les tests de chaque dépôt")
    parser.add_argument("--date-limite", help="ex. \"2026-10-25 23:59\"")
    parser.add_argument("--dossier", default="releve", help="où cloner (par défaut : releve/)")
    args = parser.parse_args()

    racine = Path(args.dossier).resolve()
    racine.mkdir(exist_ok=True)
    with open(args.liste, encoding="utf-8", newline="") as f:
        binomes = [(r["binome"].strip(), r["depot"].strip()) for r in csv.DictReader(f) if r.get("depot", "").strip()]
    lignes = []
    for binome, url in binomes:
        print(f"Relève de {binome}...", flush=True)
        lignes.append(relever(binome, url, args, racine))

    colonnes = ["binome", "commit", "après la limite", "auteurs", "fichiers interdits", "livrables",
                "tests du kit retouchés", "F1", "pytest", "couverture", "ruff", "mypy", "remarques"]
    colonnes = [c for c in colonnes if any(c in ligne for ligne in lignes)]
    sortie = racine / f"releve-tp{args.tp}"
    with open(f"{sortie}.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        w.writeheader()
        w.writerows(lignes)
    tableau = [f"# Relève du TP{args.tp} (attendu aux tests : {ATTENDU[args.tp]})", "",
               "| " + " | ".join(colonnes) + " |", "| " + " | ".join("---" for _ in colonnes) + " |"]
    tableau += ["| " + " | ".join(str(ligne.get(c, "")).replace("|", "/") for c in colonnes) + " |" for ligne in lignes]
    Path(f"{sortie}.md").write_text("\n".join(tableau) + "\n", encoding="utf-8")
    print("\n" + "\n".join(tableau))
    print(f"\nÉcrit : {sortie}.md et {sortie}.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
