#!/usr/bin/env python
"""Installe le kit TP6 (le paquet installable) dans un dépôt sentiment-app en fin de TP5.

Usage, depuis ce dossier :
  python appliquer_tp6.py ../sentiment-app --simulation   # voir ce qui sera fait, sans rien écrire
  python appliquer_tp6.py ../sentiment-app

Le script copie le paquet sentiment_app/ (version, commande), les tests du paquet, le journal des
versions et les documents du TP, sans rien écraser. Il complète pyproject.toml (métadonnées du paquet),
requirements-dev.txt (build), pytest.ini (src/ dans le chemin des tests), .gitignore (dist/, build/)
et la CI (une étape qui construit la roue et l'installe hors du dépôt).
Le déplacement de predict.py dans le paquet reste au binôme : c'est le cœur du TP.
"""
import argparse
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
A_COPIER = [
    "sentiment_app/__init__.py", "sentiment_app/__main__.py", "sentiment_app/cli.py",
    "tests/test_packaging.py", "CHANGELOG.md", "docs/semaine6.md",
    "TP6-ENONCE.md", "MARCHE-A-SUIVRE-TP6.md",
]
LIGNES_GITIGNORE = ["dist/", "build/", "*.egg-info/"]
OUTIL = "build==1.2.2.post1"


def lire(chemin: Path) -> str:
    return chemin.read_text(encoding="utf-8") if chemin.exists() else ""


def ecrire(chemin: Path, texte: str, simulation: bool) -> None:
    if not simulation:
        chemin.write_text(texte, encoding="utf-8")


def completer_pyproject(depot: Path, simulation: bool) -> None:
    fichier = depot / "pyproject.toml"
    texte = lire(fichier)
    if "[project]" in texte:
        print("  déjà là        pyproject.toml : [project]")
        return
    print("  complète       pyproject.toml : [build-system], [project], la commande sentiment")
    bloc = (KIT / "extraits" / "pyproject-tp6.toml").read_text(encoding="utf-8")
    ecrire(fichier, texte.rstrip() + "\n" + bloc, simulation)


def completer_dev(depot: Path, simulation: bool) -> None:
    fichier = depot / "requirements-dev.txt"
    texte = lire(fichier)
    if any(ligne.startswith("build") for ligne in texte.splitlines()):
        print("  déjà là        requirements-dev.txt : build")
        return
    print(f"  complète       requirements-dev.txt : {OUTIL}")
    ecrire(fichier, texte.rstrip() + f"\n# TP6 : construire la roue\n{OUTIL}\n", simulation)


def completer_pytest(depot: Path, simulation: bool) -> None:
    fichier = depot / "pytest.ini"
    lignes = lire(fichier).splitlines()
    for i, ligne in enumerate(lignes):
        if ligne.replace(" ", "").startswith("pythonpath="):
            if "src" in ligne.split("=", 1)[1].split():
                print("  déjà là        pytest.ini : pythonpath avec src")
                return
            lignes[i] = ligne.rstrip() + " src"
            print("  complète       pytest.ini : pythonpath = . src (pour « import predict » dans les tests)")
            ecrire(fichier, "\n".join(lignes) + "\n", simulation)
            return
    print("  ATTENTION      pytest.ini sans pythonpath : ajoutez « pythonpath = . src » sous [pytest]")


def completer_gitignore(depot: Path, simulation: bool) -> None:
    fichier = depot / ".gitignore"
    texte = lire(fichier)
    manquantes = [ligne for ligne in LIGNES_GITIGNORE if ligne not in texte.splitlines()]
    if not manquantes:
        print("  déjà là        .gitignore : dist/, build/")
        return
    print(f"  complète       .gitignore : {', '.join(manquantes)}")
    ecrire(fichier, texte.rstrip() + "\n\n# TP6\n" + "\n".join(manquantes) + "\n", simulation)


def adapter_ci(depot: Path, simulation: bool) -> None:
    fichier = depot / ".github" / "workflows" / "ci.yml"
    texte = lire(fichier)
    if not texte:
        print("  ATTENTION      ci.yml introuvable : ajoutez à la main l'étape de extraits/ci-tp6.yml")
        return
    # 1. La CI doit entraîner avec la version de scikit-learn que le paquet déclare : sinon la roue
    #    ne sait pas relire le modèle (AttributeError au chargement).
    lignes = texte.splitlines()
    for i, ligne in enumerate(lignes):
        if "pip install" in ligne and " scikit-learn " in f" {ligne} " and "scikit-learn==" not in ligne:
            lignes[i] = f" {ligne} ".replace(" scikit-learn ", ' "scikit-learn==1.5.*" ')[1:-1]
            print("  complète       .github/workflows/ci.yml : scikit-learn épinglé en 1.5, comme dans le paquet")
            texte = "\n".join(lignes) + "\n"
            break
    else:
        print("  déjà là        .github/workflows/ci.yml : scikit-learn épinglé")
    # 2. L'étape qui construit la roue, l'installe dans un environnement neuf et l'essaie hors du dépôt
    if "Roue installée hors du dépôt" in texte:
        print("  déjà là        .github/workflows/ci.yml : étape de la roue")
    else:
        print("  complète       .github/workflows/ci.yml : la roue construite, installée et essayée hors du dépôt")
        texte = texte.rstrip() + "\n" + (KIT / "extraits" / "ci-tp6.yml").read_text(encoding="utf-8")
    ecrire(fichier, texte, simulation)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("depot", help="chemin du dépôt sentiment-app")
    parser.add_argument("--simulation", action="store_true", help="n'écrit rien, affiche seulement")
    args = parser.parse_args()

    depot = Path(args.depot).expanduser().resolve()
    if not (depot / "README.md").is_file() or not (depot / "tests").is_dir():
        print(f"ERREUR : {depot} ne ressemble pas au dépôt du cours (README.md et tests/ attendus)")
        return 1
    if not (depot / "api" / "main.py").is_file() or not (depot / "src" / "predict.py").exists() and not (depot / "sentiment_app" / "predict.py").exists():
        print("ERREUR : api/main.py ou src/predict.py absent. Le TP6 se pose sur le dépôt en fin de TP5.")
        return 1
    if not (depot / "ui" / "client.py").is_file():
        print("ATTENTION : ui/client.py absent, le TP5 n'est pas installé : le paquet n'aura pas d'interface.")
    print(f"Dépôt cible : {depot}")

    for chemin in A_COPIER:
        src, dst = KIT / chemin, depot / chemin
        if not src.exists():
            print(f"  ABSENT DU KIT  {chemin}")
        elif dst.exists():
            print(f"  conservé       {chemin} (déjà présent, non écrasé)")
        else:
            print(f"  ajoute         {chemin}")
            if not args.simulation:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    completer_pyproject(depot, args.simulation)
    completer_dev(depot, args.simulation)
    completer_pytest(depot, args.simulation)
    completer_gitignore(depot, args.simulation)
    adapter_ci(depot, args.simulation)

    print("\nSimulation : rien n'a été écrit." if args.simulation else
          "\nKit installé. Suite, dans le dépôt : pip install -r requirements-dev.txt, puis python -m pytest -q"
          " (contrôle T35 de MARCHE-A-SUIVRE-TP6.md).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
