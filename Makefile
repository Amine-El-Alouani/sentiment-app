# Raccourcis du TP1. Linux, macOS et Git Bash ; sous Windows, lancez les
# commandes directement ou utilisez scripts\setup.ps1.

.PHONY: help setup check test test-cadrage test-env test-git verif clean exemple-ml exemple-ui

help:
	@echo "Cibles disponibles :"
	@echo "  make setup        installe le venv et les dependances, puis diagnostique"
	@echo "  make check        lance le diagnostic lisible"
	@echo "  make test         lance les 38 tests"
	@echo "  make test-cadrage lance les 12 tests des fiches (partie A)"
	@echo "  make test-env     lance les 23 tests d'environnement"
	@echo "  make test-git     lance les 3 tests d'historique Git"
	@echo "  make verif URL=<url>  rejoue le test de l'enseignant sur un clone frais"
	@echo "  make exemple-ml   entraine le modele d'exemple (semaine 2)"
	@echo "  make exemple-ui   lance l'interface Streamlit (semaine 5)"
	@echo "  make clean        supprime les caches (garde le venv)"

setup:
	bash scripts/setup.sh

check:
	.venv/bin/python scripts/check_setup.py

test:
	.venv/bin/python -m pytest -q

test-cadrage:
	.venv/bin/python -m pytest tests/test_cadrage.py -q

test-env:
	.venv/bin/python -m pytest tests/test_environment.py -q

test-git:
	.venv/bin/python -m pytest tests/test_git_history.py -q

verif:
	@test -n "$(URL)" || (echo "Usage : make verif URL=https://github.com/<org>/sentiment-app.git"; exit 2)
	bash scripts/verif_clone.sh $(URL)

exemple-ml:
	.venv/bin/python exemples/train_sentiment.py

exemple-ui:
	.venv/bin/streamlit run exemples/app_streamlit.py

clean:
	rm -rf .pytest_cache
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
