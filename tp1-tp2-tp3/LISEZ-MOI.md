# Entrepôt TP1, TP2, TP3

Tout ce qu'il faut pour les trois premières séances du module, sur un seul dépôt étudiant.

## Contenu

| Dossier | Fichier | Pour qui | Quand |
| --- | --- | --- | --- |
| | `tp1-tp2-tp3.md` | Tous | La démarche complète, dix-sept contrôles |
| | `tp1-tp2-tp3-detaille.tex`, `.pdf` | Tous | **La version détaillée**, 22 pages : chaque commande expliquée, architecture, tests, CI et MLOps |
| | `tp1-tp2-tp3.tex`, `.pdf` | Tous | La version courte, 8 pages, convertie du Markdown |
| | `TP3-colab-streamlit.ipynb` | Étudiants | L'interface sur Colab, avec tunnel |
| `kits/` | `sentiment-app.zip` | Étudiants | Avant le TP1 |
| `kits/` | `tp2-semaine2-kit.zip` | Étudiants | Avant le TP2 |
| `kits/` | `tp3-streamlit-kit.zip` | Étudiants | Avant le TP3 |
| `compte-rendu/` | `ENONCE-COMPTE-RENDU.md` | Étudiants | Distribué au TP3 |
| `compte-rendu/` | `compte-rendu-TEMPLATE.md` | Étudiants | Squelette à remplir |
| `diapositives/` | `tp1-tp2-tp3-beamer.pdf` et `.tex` | Projection | **Vue d'ensemble des trois TP** : objectif, kits, Streamlit, démarche, CI et MLOps (34 diapositives) |
| `diapositives/` | trois autres PDF | Projection | TP1 détaillé (44), TP1 démarche (19), TP2 (13) |
| `enseignant/` | `corrige-cadrage/`, QCM, guide | **Enseignant seulement** | Ne pas distribuer |

## L'ordre des opérations

1. **Avant le TP1 :** diffusez `sentiment-app.zip` et les prérequis (Python 3.11, Git, compte GitHub).
2. **TP1 :** les binômes créent leur dépôt `sentiment-app`. Fin de séance : 38 tests verts.
3. **TP2 :** diffusez `tp2-semaine2-kit.zip`, installé par `python appliquer_tp2.py ../sentiment-app`. Fin : 42 tests.
4. **TP3 :** diffusez `tp3-streamlit-kit.zip`, même mécanique. Fin : 45 tests, et une interface qui tourne.
5. **Après le TP3 :** le compte rendu global, déposé dans `docs/compte-rendu.md` et figé par une étiquette Git.

Aucun kit n'écrase le travail du précédent.

## Les comptes de tests

| Moment | `pytest -q` | Sur Colab |
| --- | --- | --- |
| Kit TP1 décompressé, fiches vides, pas de dépôt | 3 failed, 31 passed, 4 skipped | idem, sans `test_virtualenv_active` |
| Fin du TP1 | 38 passed | 37 passed |
| Kit TP2 installé, avant entraînement | 2 failed, 38 passed, 2 skipped | idem |
| Fin du TP2 | 42 passed | 41 passed |
| Fin du TP3 | 45 passed | 44 passed |

Chiffres obtenus en rejouant la chaîne complète depuis les trois zips de ce dossier.

## Google Colab

Les trois kits contiennent leur notebook, dans `notebooks/`. Le TP3 a besoin d'un tunnel pour que
Streamlit soit joignable depuis votre navigateur : le notebook lance `localtunnel`, affiche un mot
de passe (l'IP publique de la machine) et une adresse `loca.lt`. Cette adresse est publique et
temporaire : aucune donnée réelle ne doit y transiter.

## Note sur la numérotation

Dans le plan du module, la semaine 3 est consacrée à l'API et Streamlit arrive en semaine 5.
Ce paquet enchaîne cadrage, modèle, puis interface, pour donner un résultat visible dès la troisième
séance. Si vous suivez le plan d'origine, le kit `tp3-streamlit` devient celui de la semaine 5 sans
aucune modification : il ne dépend que de `src/predict.py`, produit au TP2.
