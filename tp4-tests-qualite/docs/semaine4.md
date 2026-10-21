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

- Deux ou trois points de la courbe (`python src/courbe_seuil.py`) : …
- Seuil retenu : … ; part des avis envoyés à un humain : … ; justification : …

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) : justes …, abstentions …, erreurs franches déclarées …
- Ce que ces chiffres disent du modèle : …

## 5. Outils statiques

- Remarques au départ : ruff …, mypy …
- Parmi les défauts de la partie 2, combien ruff et mypy avaient-ils signalés ? Qu'en concluez-vous ?
