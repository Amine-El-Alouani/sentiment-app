# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : … %, lignes jamais exécutées : …
- Pour chacune, le comportement qu'aucun test ne vérifiait : …
- Après (étape D) : … % ; lignes exclues de la mesure et pourquoi : …

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| … | … | … |

## 3. Seuil d'abstention

- Trois textes de mots inventés reçoivent tous `NEGATIVE` à `0,5162` sans abstention :
  sans mot connu, le vecteur TF-IDF est nul et il ne reste que l'ordonnée à l'origine.
- Courbe (`python src/courbe_seuil.py`) :
  - à `0,50` : 58 réponses, 100 % d'exactitude, 7 erreurs, 0 vers un humain ;
  - à `0,60` : 42 réponses, 95,2 % d'exactitude, 2 erreurs, 16 vers un humain ;
  - à `0,70` : 37 réponses, 100 % d'exactitude, 0 erreur, 21 vers un humain.
- Seuil retenu : `0,60` ; 28 % des avis du jeu de test sont envoyés à un humain.
  Ce seuil améliore nettement l'exactitude des réponses automatiques tout en conservant
  la majorité des avis traités automatiquement.
- Dans l'API, un score inférieur à `0,60` devient `INDETERMINE`, tandis que le score
  original reste renvoyé. T24 : un texte inventé reçoit donc `INDETERMINE` avec un
  score de `0,5162`.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) sur 20 avis : 7 justes, 9 abstentions et
  4 erreurs franches déclarées.
- `python -m pytest -q tests/test_jeu_or.py` : 17 tests passés et 4 erreurs déclarées
  en `xfail` ; aucun `failed`.
- Le modèle évite ainsi de transformer les cas incertains en erreurs franches, mais
  son seuil de `0,60` entraîne beaucoup d'abstentions sur ce petit jeu. Les erreurs
  restantes concernent notamment la négation, les avis mitigés et le vocabulaire
  ambigu ; elles sont conservées et documentées pour guider une amélioration future.

## 5. Outils statiques

- Remarques au départ : ruff …, mypy …
- Parmi les défauts de la partie 2, combien ruff et mypy avaient-ils signalés ? Qu'en concluez-vous ?
