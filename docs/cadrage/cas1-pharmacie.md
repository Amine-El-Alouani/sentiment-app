# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Signaler au pharmacien toute ordonnance à laquelle il manque un champ obligatoire, avant la délivrance des médicaments.

## Utilisateur final (obligatoire)

Le pharmacien de garde, qui reçoit une alerte au moment de la saisie au lieu de relire chaque ordonnance ligne par ligne.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Aucune base d'ordonnances étiquetées complètes ou incomplètes n'existe au départ, et en constituer une demanderait des mois. (b) Le pharmacien doit pouvoir expliquer au patient quel champ manque : une règle se montre, un modèle statistique non. (d) Une ordonnance validée à tort a une conséquence grave sur la santé, ce qui interdit une approche dont on ne peut pas justifier chaque décision.

## Données nécessaires et leur origine (obligatoire)

La liste réglementaire des champs obligatoires d'une ordonnance (prescripteur, date, posologie, durée, signature), fournie par le service pharmacie. Pour les tests, uniquement des ordonnances fictives rédigées par l'équipe : aucune ordonnance réelle n'entre dans le projet.

## Métrique de succès et seuil d'acceptation (obligatoire)

Taux de champs obligatoires manquants effectivement détectés, mesuré sur un jeu de 50 ordonnances fictives dont la moitié est incomplète. Acceptation à 100 pour cent de détection, avec moins de 10 pour cent de fausses alertes.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une alerte manquée peut conduire à délivrer un médicament sur une ordonnance non conforme. Le système ne bloque donc rien seul : il affiche le champ suspect, et le pharmacien valide chaque ordonnance, signalée ou non, avant la délivrance.

## Risques éthiques ou de confidentialité (obligatoire)

Les ordonnances sont des données de santé, protégées par la loi 09-08 au Maroc et par le RGPD en Europe. Aucune ordonnance réelle, aucun nom de patient et aucun identifiant ne sont utilisés dans ce cours, et rien n'est envoyé à un service externe.

## Approche écartée et pourquoi (facultatif)

Le machine learning : il faudrait d'abord constituer un jeu étiqueté de plusieurs milliers d'ordonnances, pour un gain nul sur une règle dont la liste des champs est déjà écrite dans le texte réglementaire.
