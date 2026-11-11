"""La commande « sentiment » (TP6) : le paquet s'utilise sans connaître ses fichiers.

  sentiment --version
  sentiment predict "Livraison rapide, très satisfait"
  sentiment serve [--host 127.0.0.1] [--port 8000]
  sentiment ui
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from sentiment_app import __version__


def _predire(args: argparse.Namespace) -> int:
    """Même raccord que l'API (api/model.py) : le seuil d'abstention s'applique aussi ici."""
    from api.model import load_model

    try:
        classifieur = load_model()
    except FileNotFoundError as erreur:
        print(erreur, file=sys.stderr)
        return 1
    print(json.dumps(classifieur.predict(" ".join(args.texte)), ensure_ascii=False))
    return 0


def _servir(args: argparse.Namespace) -> int:
    import uvicorn

    uvicorn.run("api.main:app", host=args.host, port=args.port)
    return 0


def _interface(args: argparse.Namespace) -> int:
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print('Streamlit absent : pip install "sentiment-app[ui]"', file=sys.stderr)
        return 1
    page = Path(__file__).resolve().parents[1] / "ui" / "app.py"
    return subprocess.call([sys.executable, "-m", "streamlit", "run", str(page)])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sentiment", description="Analyse de sentiment d'avis clients.")
    parser.add_argument("--version", action="version", version=f"sentiment-app {__version__}")
    commandes = parser.add_subparsers(dest="commande", required=True)

    predire = commandes.add_parser("predict", help="classe un avis, sans serveur")
    predire.add_argument("texte", nargs="+", help="l'avis à analyser")
    predire.set_defaults(fonction=_predire)

    servir = commandes.add_parser("serve", help="lance l'API")
    servir.add_argument("--host", default="127.0.0.1")
    servir.add_argument("--port", type=int, default=8000)
    servir.set_defaults(fonction=_servir)

    interface = commandes.add_parser("ui", help="lance la page Streamlit (l'API doit tourner)")
    interface.set_defaults(fonction=_interface)

    args = parser.parse_args(argv)
    return int(args.fonction(args))
