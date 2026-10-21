# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Classer automatiquement les avis clients en positifs et négatifs pour faire remonter les négatifs en tête de la file de traitement.

## Utilisateur final (obligatoire)

L'équipe relation client, qui répond d'abord aux clients mécontents au lieu de lire les avis dans leur ordre d'arrivée.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Les avis s'étiquettent à très faible coût à partir de la note en étoiles déjà saisie par le client. (c) Plusieurs milliers d'avis arrivent chaque jour : un classifieur coûte une fraction de milliseconde par avis, là où un appel à un modèle de langage se paierait à chaque fois. (d) Un avis mal classé est simplement traité plus tard, et l'agent le requalifie d'un clic.

## Données nécessaires et leur origine (obligatoire)

Un jeu public d'avis en français avec leur note pour l'entraînement, et un export anonymisé des avis du site pour l'évaluation. Les avis sont séparés en jeux d'entraînement, de validation et de test avant tout travail de modélisation.

## Métrique de succès et seuil d'acceptation (obligatoire)

Rappel sur la classe négative, mesuré sur un jeu de test tenu à l'écart : acceptation à partir de 0,90. Le rappel prime sur la précision, car manquer un client mécontent coûte plus cher que relire un avis positif.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif classé positif retarde la réponse de quelques heures, sans conséquence irréversible. L'agent peut requalifier n'importe quel avis, et chaque requalification alimente le jeu de réentraînement.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis peuvent citer un nom, un numéro de commande ou une adresse : anonymisation avant stockage. Il faut aussi surveiller le biais entre avis courts et avis détaillés, les premiers étant plus souvent mal classés.

## Approche écartée et pourquoi (facultatif)

Les règles par mots-clés : testées en interne, elles plafonnent autour de 60 pour cent d'exactitude parce que la négation et l'ironie leur échappent (« rien à redire » est compté comme négatif).
