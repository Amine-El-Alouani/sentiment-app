# Grille de décision : quelle approche pour quel besoin ?

Feuille de rappel pour la partie A du TP1. À garder ouverte pendant que vous remplissez les fiches.

## Les quatre critères

| Lettre | Critère | La question à se poser |
| --- | --- | --- |
| (a) | Données étiquetées | A-t-on des exemples déjà annotés, ou peut-on en produire à faible coût ? |
| (b) | Vérifiabilité | La réponse doit-elle pouvoir être tracée jusqu'à une source ou une règle ? |
| (c) | Coût par requête | Combien d'appels par jour, et que coûte chacun ? |
| (d) | Conséquence d'une erreur | Que se passe-t-il concrètement quand le système se trompe ? |

Votre justification doit citer au moins deux de ces lettres, écrites telles quelles : `(a)`, `(b)`, `(c)`, `(d)`.

## L'arbre de choix

Parcourez les questions dans l'ordre. La première réponse « oui » donne l'approche.

1. La logique est-elle connue, stable, et doit-elle rester explicable ? → **règles métier**
2. Dispose-t-on de données étiquetées pour une tâche répétitive ? → **machine learning**
3. La réponse doit-elle être tirée de documents existants et citée ? → **RAG**
4. Sinon, et seulement sinon → **modèle génératif seul**

On ne saute jamais directement à la dernière ligne : c'est l'option la plus coûteuse et la moins vérifiable.

## Les quatre approches, en une ligne chacune

| Approche | Quand | Coût par requête | Vérifiabilité |
| --- | --- | --- | --- |
| Règles métier | logique connue et stable | quasi nul | totale, la règle est lisible |
| Machine learning | données étiquetées, tâche répétitive | très faible | moyenne, on explique par les exemples |
| RAG | réponse à tirer de documents | moyen | bonne, la source est citée |
| Génératif seul | texte libre, pas de vérité unique | élevé | faible, d'où la relecture humaine |

## Deux réflexes attendus dans chaque fiche

**La métrique.** Un seuil chiffré sur un jeu de test défini : « rappel d'au moins 0,90 sur la classe négative », pas « de bons résultats ».

**La validation humaine.** Dès que l'erreur a une conséquence réelle, une personne doit pouvoir contredire le système avant que l'action ne parte. Écrivez qui, et à quel moment.

## Rappel éthique

Aucune donnée personnelle réelle dans ce cours, du TP1 au projet : uniquement des données publiques, fictives ou anonymisées (RGPD, loi 09-08). Un avis client peut contenir un nom, un numéro de commande ou une adresse.
