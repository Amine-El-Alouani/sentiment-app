# TP4 (semaine 4) : tests approfondis et qualité de l'API

## Contexte et objectifs

Le TP4 n'ajoute presque rien à l'API : il cherche ses défauts, les corrige et installe les garde-fous qui empêcheront leur retour.

**Module** : Développement et déploiement d'applications intelligentes · **Auteur** : A. Larhlimi · **Public** : binômes · **Durée** : une séance de 2 h, jeu d'or préparé avant, compte rendu terminé après

À la fin du TP3, l'API répond et ses six tests passent. Aucun test ne dit pourtant ce qu'elle répond à un texte fait d'espaces, à un texte dont aucun mot n'est connu du modèle, ou quand le modèle plante en pleine requête. Le seul changement visible de la semaine est un troisième verdict, `INDETERMINE`, que l'interface du TP5 affichera.

**La question de la séance** : que peut-on garantir sur cette API, et comment le prouver à chaque commit ?

À la fin de la séance, le binôme sait :

1. écrire des tests aux limites du contrat et des tests de propriété (hypothesis) qui trouvent des cas auxquels personne n'a pensé ;
2. faire dire « je ne sais pas » au modèle, avec un seuil mesuré puis vérifié sur un jeu d'or écrit à la main ;
3. tester l'API comme elle tourne vraiment (démarrage, modèle absent, modèle en panne) et lire un rapport de couverture ligne par ligne ;
4. faire vérifier le code par ruff et mypy, et dire ce que ces outils voient et ne voient pas ;
5. rendre tout cela automatique : crochet pre-commit en local, CI qui refuse un commit qui régresse.

**Hors périmètre** : Docker et Compose arrivent au TP8, le suivi des expériences au TP7. Les tests de charge et Kubernetes ne font pas partie du cours.

## Prérequis et installation

Le TP4 part du dépôt `sentiment-app` dans l'état exact de fin de TP3, CI verte.

- `api/` contient `model.py`, `schemas.py` et `main.py` (TP3) ; `src/predict.py` expose `predict()` et `charger_modele()` (TP2).
- `pytest -q` affiche `48 passed`, le compte de référence de fin de TP3.
- L'API démarre avec `uvicorn api.main:app --reload`, et `http://localhost:8000/docs` s'ouvre.

Installation : décompressez `tp4-tests-qualite-kit.zip` à côté du dépôt, puis, environnement virtuel activé (sous Windows, `..\` au lieu de `../`) :

```bash
cd tp4-tests-qualite
python appliquer_tp4.py ../sentiment-app
cd ../sentiment-app
pip install -r requirements-dev.txt
python src/train.py
python -m pytest -q
```

Le script dépose le kit sans rien écraser et complète `pyproject.toml` et `.gitignore`. Le TP4 se fait avec le modèle du jeu de démonstration, celui que la CI entraîne : d'où `python src/train.py`. Juste après l'installation, `pytest -q` affiche `1 failed, 51 passed, 1 skipped` : le test qui échoue réclame le jeu d'or.

Le kit apporte la configuration des outils (`pyproject.toml`, `.pre-commit-config.yaml`, `requirements-dev.txt`), deux scripts (`src/courbe_seuil.py`, `src/bilan_jeu_or.py`), deux fichiers de tests à compléter (`tests/test_limites.py`, `tests/test_integration.py`), le test du jeu d'or (`tests/test_jeu_or.py`), l'en-tête de `data/jeu_or.csv` et le canevas de `docs/semaine4.md`.

**À préparer avant la séance** : vos 20 avis du jeu d'or (voir l'étape C). C'est le seul travail d'écriture du TP, et il prend du temps.

## Déroulé de la séance

Cinq étapes en 2 h, chacune close par un contrôle numéroté à la suite de ceux du TP3 (T14 à T20).

| Étape | Durée | Ce que vous faites | Contrôle |
| --- | --- | --- | --- |
| A. État des lieux | 15 min | Installer le kit ; mesurer tests, couverture, ruff et mypy avant toute correction | T21 : couverture de départ et lignes manquantes notées |
| B. Contrat d'entrée | 30 min | Test paramétré aux limites, deux propriétés hypothesis, correction du schéma | T22 : `{"text": "   "}` refusé par le schéma ; T23 : propriétés vertes |
| C. Abstention | 25 min | Texte inconnu du modèle, courbe du seuil, verdict `INDETERMINE`, jeu d'or | T24 : texte inconnu → `INDETERMINE` ; T25 : jeu d'or vert |
| D. Intégration | 25 min | Démarrage réel, modèle absent, modèle non chargé, modèle en panne ; couverture | T26 : panne → 500, couverture de `api/` à 95 % au moins |
| E. Qualité statique et CI | 25 min | Contrat typé, ruff et mypy muets, pre-commit, CI étendue | T27 : CI verte avec ruff, mypy et seuil de couverture |

Après la séance : terminer `docs/semaine4.md`, puis commit « Semaine 4 : tests approfondis et qualité » et push.

## Travail demandé

Chaque étape part d'une question et se termine par un contrôle ; chaque défaut trouvé va dans `docs/semaine4.md`, avec le test qui l'a révélé.

### A. État des lieux (15 min)

1. Mesurez la couverture de l'API avant d'écrire un seul test : `pytest --cov=api --cov-report=term-missing`.
2. Recopiez dans `docs/semaine4.md` le pourcentage et les lignes jamais exécutées. Pour chacune, une phrase : quel comportement de l'API aucun test ne vérifie-t-il ?
3. Lancez `ruff check .` puis `mypy api`, sans rien corriger. Notez le nombre de remarques de chacun : vous y reviendrez à l'étape E.

**T21** : la couverture de départ et ses lignes manquantes figurent dans `docs/semaine4.md`.

### B. Le contrat d'entrée (30 min)

`PredictRequest` promet un champ `text`, chaîne de 1 à 2000 caractères. Vérifiez cette promesse à ses frontières, puis au hasard.

1. Dans `tests/test_limites.py`, écrivez **un seul** test paramétré (`@pytest.mark.parametrize`) qui envoie au moins huit corps de requête, chacun avec son code attendu : texte vide, texte fait d'espaces, un seul caractère, exactement 2000 caractères, 2001 caractères, champ absent, champ d'un autre type (`42`), corps qui n'est pas du JSON.
2. Pour chaque 422, vérifiez aussi la forme de la réponse : `detail` doit être la liste d'erreurs standard de FastAPI (des objets avec `loc`, `msg` et `type`).
3. Un des cas reçoit le bon code, mais une réponse d'une autre forme. Lequel ? Quelle partie du code produit chacune des deux formes ? Pourquoi l'interface du TP5 préférera-t-elle n'en recevoir qu'une ?
4. Corrigez **le schéma**, pas le modèle : un `field_validator` refuse un texte vide une fois ses blancs retirés, avec la même règle que `predict()` du TP2 (`str.strip()`).
5. Ajoutez deux tests de propriété avec hypothesis. Tout texte de 1 à 2000 caractères contenant au moins un caractère non blanc reçoit 200, une étiquette du contrat et un score entre 0 et 1. Tout texte fait uniquement de blancs reçoit 422, sous la forme standard.
6. Si hypothesis trouve un contre-exemple, ajoutez-le comme cas explicite au test paramétré et expliquez-le.

**T22** : `{"text": "   "}` reçoit 422 sous la même forme que `{"text": ""}`.

**T23** : les deux propriétés passent, trois exécutions de suite.

### C. Un modèle qui sait dire « je ne sais pas » (25 min)

1. Envoyez à l'API un texte fait de mots inventés. Quelle étiquette reçoit-il, avec quelle confiance ? Expliquez ce chiffre : que devient la représentation TF-IDF d'un texte dont aucun mot n'est dans le vocabulaire, et que reste-t-il alors à la régression logistique ?
2. Lancez `python src/courbe_seuil.py` (`--allocine` pour le jeu Allociné). Pour chaque seuil de 0,50 à 0,95, il affiche, sur le jeu de test du TP2, la part des avis auxquels le modèle répond et l'exactitude sur ces seuls avis.
3. Choisissez un seuil (0,60 par défaut) et justifiez-le : combien d'avis partent vers un humain, combien d'erreurs sont évitées.
4. Dans `api/model.py`, sous le seuil, l'étiquette devient `INDETERMINE` et le score reste renvoyé. Le seuil est une constante nommée (`SEUIL_ABSTENTION`), jamais un nombre en dur dans une condition.
5. Mettez à jour la description du champ `label`, et les tests du TP3 qui supposaient deux étiquettes.
6. `tests/test_jeu_or.py` (fourni) crée un cas de test par ligne de `data/jeu_or.csv`. Un cas échoue si l'API se trompe franchement (`POSITIVE` au lieu de `NEGATIVE`, ou l'inverse) ; une abstention ne le fait pas échouer, mais elle est comptée par `src/bilan_jeu_or.py`.

Le jeu d'or, préparé avant la séance :

- 20 avis rédigés par le binôme, absents des données d'entraînement, chacun avec l'étiquette attendue (`POSITIVE` ou `NEGATIVE`) ;
- au moins 5 avis difficiles, signalés dans la colonne `difficulte` : négation, ironie, avis mitigé, avis d'un autre domaine que celui des données d'entraînement ;
- une erreur franche que vous ne savez pas corriger ne se retire pas du jeu : la colonne `erreur_connue` en donne la raison, et le test la marque `xfail(strict=True)`.

```csv
text,attendu,difficulte,erreur_connue
"Commande reçue en deux jours, emballage soigné",POSITIVE,,
"Pas déçu du tout, je recommande",POSITIVE,négation,
"Arrivé cassé, bravo le transporteur",NEGATIVE,ironie,
```

**T24** : un texte fait de mots inventés reçoit `INDETERMINE`.

**T25** : `pytest tests/test_jeu_or.py` est vert ; chaque erreur franche est corrigée ou déclarée avec sa raison.

### D. L'API telle qu'elle tourne (25 min)

Les tests du TP3 vérifient des réponses ; aucun ne vérifie le démarrage de l'API ni ses pannes. Écrivez-les dans `tests/test_integration.py`.

1. **Démarrage réel** : un client ouvert par `with TestClient(app) as client:` exécute le `lifespan`. Vérifiez que `/health` répond 200 et nomme le modèle servi.
2. **Modèle absent** : redirigez le chemin du modèle vers un fichier inexistant (`monkeypatch`), videz le cache de chargement (`charger_modele.cache_clear()`), et vérifiez que l'API refuse de démarrer (`FileNotFoundError`). C'est le contrôle T20 du TP3, devenu automatique.
3. **Modèle non chargé** : l'API démarrée, retirez le modèle de `app.state` ; `/health` et `/predict` doivent répondre 503.
4. **Modèle en panne** : remplacez le modèle par un objet dont `predict` lève une exception, d'abord `RuntimeError`, puis `ValueError("bug interne")`. Les deux doivent répondre 500, sans que le message interne apparaisse dans la réponse.
5. Que se passe-t-il avec `ValueError`, et pourquoi ? Corrigez `api/main.py` : depuis l'étape B, le schéma garantit un texte non vide, la conversion de `ValueError` en 422 n'a plus lieu d'être.
6. Relancez `pytest --cov=api --cov-report=term-missing`. Toute ligne exclue de la mesure (`# pragma: no cover`) est justifiée dans `docs/semaine4.md` ; seul le bloc `if __name__ == "__main__":` est un candidat évident.

**T26** : une panne du modèle répond 500, quelle que soit l'exception ; la couverture de `api/` atteint 95 % au moins.

### E. Qualité statique et automatisation (25 min)

1. **Contrat typé** : relancez `mypy api`. Il ne signale rien sur les étiquettes : pourquoi ? Regardez le type de retour de `predict()` au TP2 : d'un `dict` sans précision ne sortent que des `Any`, que mypy ne vérifie pas.
2. Donnez des types précis : un `TypedDict` pour le retour de `predict()` (TP2) et pour celui de `SentimentClassifier.predict`, l'étiquette limitée aux valeurs du contrat (`Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]`), le même type dans `PredictResponse`. Relancez mypy : que signale-t-il, et pourquoi `.upper()` ne suffit-il plus ?
3. Remplacez `.upper()` par une correspondance explicite entre les étiquettes du modèle et celles du contrat. Au démarrage, vérifiez que le modèle chargé n'a pas d'autres classes que celles de la correspondance, sinon l'API refuse de démarrer. Ajoutez le test.
4. Rendez `ruff check .` muet (`--fix` règle l'essentiel). Corrigez plutôt que de faire taire : un `# noqa` reste exceptionnel, avec le code de la règle et sa raison.
5. Installez le crochet (`pre-commit install`). Montrez qu'un commit contenant une erreur signalée par ruff est refusé, puis corrigez.
6. Dans `.github/workflows/ci.yml`, remplacez l'étape « Tests » par les quatre étapes suivantes, après l'étape « Modèle de démonstration » du TP3. Chacune active l'environnement virtuel, comme les étapes du TP1 (le fichier `ci-tp4.yml` du kit les contient).

```yaml
      - name: Outils de qualité (TP4)
        run: . .venv/bin/activate && pip install -r requirements-dev.txt
      - name: ruff
        run: . .venv/bin/activate && ruff check .
      - name: mypy
        run: . .venv/bin/activate && mypy api
      - name: Tests et couverture
        run: . .venv/bin/activate && pytest -q --cov=api --cov-report=term-missing --cov-fail-under=95
```

**T27** : `ruff check .` et `mypy api` sont muets en local ; la CI est verte avec ces trois vérifications.

## Le compte rendu `docs/semaine4.md`

Une à deux pages en cinq parties, avec uniquement des chiffres issus de vos propres exécutions.

1. **Couverture** : avant et après, les lignes manquantes au départ et le comportement que chacune représentait.
2. **Défauts trouvés** : pour chacun, le symptôme, le test qui l'a révélé et la correction.
3. **Seuil d'abstention** : deux ou trois points de la courbe, le seuil retenu, la part des avis envoyés à un humain, la justification.
4. **Jeu d'or** : réponses justes, abstentions, erreurs franches déclarées, et ce qu'elles disent du modèle.
5. **Outils statiques** : remarques de ruff et de mypy au départ ; parmi les défauts de la partie 2, combien avaient-ils signalés ? Qu'en concluez-vous ?

## Livrables

Tout est dans le dépôt du binôme, sur `main`, CI verte.

- [ ] `api/schemas.py` : texte vide après retrait des blancs refusé par le schéma ; `label` limité aux trois valeurs du contrat
- [ ] `api/model.py` : seuil d'abstention nommé, correspondance explicite des étiquettes, vérification des classes au démarrage
- [ ] `api/main.py` : une panne du modèle répond 500, jamais 422
- [ ] `tests/test_limites.py` : un test paramétré de huit cas au moins et deux propriétés hypothesis
- [ ] `tests/test_integration.py` : démarrage réel, modèle absent, modèle non chargé, modèle en panne, classes inattendues
- [ ] `data/jeu_or.csv` (20 avis, dont 5 difficiles au moins) et `tests/test_jeu_or.py` vert
- [ ] `ruff check .` et `mypy api` muets ; crochet pre-commit installé
- [ ] CI verte : ruff, mypy, puis pytest avec `--cov-fail-under=95`
- [ ] `docs/semaine4.md` complet
- [ ] Commit « Semaine 4 : tests approfondis et qualité » poussé

## Grille de notation (sur 10)

L'abstention pèse le plus lourd : c'est le seul changement que l'utilisateur verra.

| Critère | Contrôles | Points |
| --- | --- | --- |
| Contrat d'entrée : cas limites, propriétés, correction dans le schéma | T22, T23 | 2 |
| Abstention : seuil mesuré et justifié, jeu d'or honnête (cas difficiles gardés, erreurs déclarées) | T24, T25 | 2,5 |
| Intégration : démarrage, modèle absent, 503, 500 ; couverture de 95 % sans exclusion abusive | T26 | 2 |
| Qualité statique et automatisation : contrat typé, ruff et mypy muets, pre-commit, CI verte | T27 | 2 |
| `docs/semaine4.md` : chaque défaut relié au test qui l'a trouvé, chiffres issus de vos exécutions | T21 | 1,5 |
| **Total** |  | **10** |

## Pièges fréquents

La plupart viennent d'un état qui survit d'un test à l'autre.

| Piège | Conséquence | Correction |
| --- | --- | --- |
| `client = TestClient(app)` sans `with` | Le `lifespan` ne tourne pas : modèle jamais chargé, 503 partout | Ouvrir le client dans une fixture : `with TestClient(app) as client` |
| Fixture de portée `function` dans un test hypothesis | Hypothesis refuse de tourner (`FailedHealthCheck`, `function_scoped_fixture`) | Un client de portée `module` |
| Cache de `charger_modele` oublié | Le test « modèle absent » passe ou échoue selon l'ordre des tests | `charger_modele.cache_clear()` avant de démarrer l'API |
| `app.state` modifié à la main dans un test | Les tests suivants héritent d'un modèle retiré ou en panne | `monkeypatch.setattr`, qui restaure l'état à la fin du test |
| Deux définitions de « vide » (schéma, modèle) | Un texte passe l'une et pas l'autre ; hypothesis finit par le trouver | La même règle aux deux endroits : `str.strip()` |
| Avis retirés du jeu d'or parce que le modèle s'y trompe | Le jeu d'or ne protège plus rien | Garder l'avis, déclarer l'erreur : `xfail(strict=True)` |
| `xfail` réglés avec un autre modèle que celui de la CI | Un cas réussit en CI et `strict=True` en fait un échec | Évaluer le jeu d'or avec le modèle que la CI entraîne |
| `# pragma: no cover` pour atteindre 95 % | Une couverture flatteuse qui ne prouve rien | N'exclure que ce qui ne tourne pas sous pytest, et le justifier |
| mypy muet sur les étiquettes | Un `dict` sans type ne transporte que des `Any` | `TypedDict` et `Literal` sur tout le chemin de l'étiquette |
| `.hypothesis/` et `.coverage` commités | Dépôt pollué à chaque exécution | Les ajouter au `.gitignore` |

## Pour aller plus loin (facultatif)

Trois pistes pour les binômes en avance, sans effet sur la note.

- **Tests de données** (`tests/test_donnees.py`) : reproduisez le découpage de l'entraînement comme le fait `src/evaluate.py`. Aucun texte ne doit figurer à la fois dans l'entraînement et le test, aucun texte ne doit porter deux étiquettes. Mesurez sur le jeu de démonstration et sur Allociné ; si des textes contradictoires existent, calculez le plafond d'exactitude qu'ils imposent.
- **Une propriété d'invariance** : entourer un texte de blancs, sans dépasser 2000 caractères, ne change ni l'étiquette ni le score. Expliquez pourquoi c'est vrai pour un modèle TF-IDF.
- **Couverture des branches** : `pytest --cov=api --cov-branch`. Quelles branches restent sans test alors que toutes les lignes sont couvertes ?
