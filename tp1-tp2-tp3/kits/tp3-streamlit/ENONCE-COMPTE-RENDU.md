# Compte rendu global des TP1, TP2 et TP3

**Module :** Développement et déploiement d'applications intelligentes
**Auteur :** A. Larhlimi
**Travail :** en binôme · **Rendu :** sur GitHub, dans votre dépôt `sentiment-app`

## Ce qui est demandé

Un document unique qui raconte les trois séances comme un seul projet : ce que vous avez construit, les décisions que vous avez prises, ce qui a échoué, et ce que vous feriez autrement.

Ce n'est pas un résumé des énoncés. L'enseignant les connaît. Ce qui est noté, c'est **votre analyse** : pourquoi telle approche, pourquoi ce seuil, pourquoi ce modèle se trompe là où il se trompe.

**Longueur :** quatre à six pages, soit environ 1 500 à 2 500 mots. Un compte rendu plus long n'est pas mieux noté ; un compte rendu de deux pages sera incomplet.

## Où le déposer

Dans votre dépôt, à l'emplacement exact suivant :

```text
sentiment-app/
└── docs/
    └── compte-rendu.md
```

Partez du modèle `docs/compte-rendu-TEMPLATE.md`, livré avec le kit du TP3 :

```bash
cp docs/compte-rendu-TEMPLATE.md docs/compte-rendu.md
```

Puis, une fois rédigé :

```bash
git add docs/compte-rendu.md
git commit -m "Compte rendu global des TP1 a TP3"
git push
git tag -a compte-rendu -m "Version remise le <date>"
git push origin compte-rendu
```

L'étiquette Git (`tag`) fige la version remise : les commits postérieurs ne seront pas pris en compte. C'est elle qui fait foi pour la date de rendu.

**Format :** Markdown, en français, dans le dépôt. Pas de PDF, pas de Word, pas de lien vers un document externe. Le compte rendu vit avec le code qu'il décrit, et se relit dans l'historique comme le reste.

**Figures :** si vous en ajoutez (matrice de confusion, copie d'écran de l'interface), placez-les dans `docs/images/` et référencez-les en Markdown. Trois images au maximum.

## Le plan attendu

| Section | Contenu | Longueur indicative |
| --- | --- | --- |
| 1. Le besoin et son cadrage | Le problème métier, l'approche retenue pour le cas 3 et sa justification par les critères (a) à (d) | 1/2 page |
| 2. L'architecture du dépôt | Ce que contient chaque dossier, ce qui est versionné et ce qui ne l'est pas, et pourquoi | 1/2 page |
| 3. Le modèle | Données, découpage, pipeline, résultats chiffrés sur les deux jeux, lecture de la matrice de confusion | 1 à 1 page et demie |
| 4. L'analyse des erreurs | Quelles erreurs, quel mécanisme les produit, ce qu'il faudrait pour les corriger | 1 page |
| 5. L'interface et le seuil d'incertitude | Le choix du seuil, son effet chiffré, l'arbitrage métier qu'il représente | 1/2 à 1 page |
| 6. Ce qui a échoué | Les blocages réels de vos séances et comment vous les avez résolus | 1/2 page |
| 7. Ce que vous feriez autrement | Avec le recul, et avec les moyens d'une vraie équipe | 1/4 page |
| 8. Répartition du travail | Qui a fait quoi, honnêtement | 3 lignes |

## Grille de notation (sur 20)

| Critère | Points | Ce qui est regardé |
| --- | --- | --- |
| Cadrage : l'approche est justifiée par les critères, pas affirmée | 3 | Les lettres (a) à (d) sont utilisées comme un raisonnement, pas comme une formalité |
| Architecture : la distinction versionné / non versionné est comprise | 3 | Vous savez dire pourquoi `metrics.json` est dans Git et pas `sentiment.joblib` |
| Modèle : chiffres exacts, méthode correcte | 4 | Vos F1 correspondent à votre `metrics.json` ; le découpage avant vectorisation est expliqué |
| Analyse des erreurs : mécanisme identifié | 4 | Les avis mitigés et l'absence d'ordre dans le sac de mots, avec un exemple tiré de vos données |
| Seuil d'incertitude : arbitrage argumenté et chiffré | 3 | Combien d'avis partent vers un agent, et pourquoi ce compromis |
| Honnêteté et clarté : échecs réels, répartition sincère, texte lisible | 3 | Un compte rendu sans aucun échec n'est pas crédible |

## Trois règles

**Vos chiffres, pas les miens.** Les valeurs du corrigé (0,879 ; 0,920 ; 7 erreurs sur 58) sont celles obtenues sur le kit de référence. Si les vôtres diffèrent, c'est les vôtres qu'il faut écrire, avec une phrase expliquant l'écart. Recopier des chiffres qui ne correspondent pas à votre `metrics.json` est la faute la plus facile à repérer.

**Un compte rendu par binôme**, avec les deux noms, et une section 8 qui dit sincèrement qui a fait quoi. Deux comptes rendus identiques entre deux binômes différents valent zéro aux deux.

**Si vous utilisez un assistant d'IA** pour rédiger, dites-le en fin de document, en une phrase : pour quoi faire, et ce que vous avez vérifié vous-même. C'est autorisé, le cacher ne l'est pas.

## Avant de pousser, vérifiez

- [ ] `docs/compte-rendu.md` existe et contient les huit sections
- [ ] Les chiffres cités correspondent à votre `models/metrics.json`
- [ ] Les deux noms et identifiants GitHub figurent en tête
- [ ] Au moins un exemple d'erreur est tiré de vos propres données
- [ ] Le compte rendu est poussé et l'étiquette `compte-rendu` créée
- [ ] `pytest -q` affiche toujours 45 passed
