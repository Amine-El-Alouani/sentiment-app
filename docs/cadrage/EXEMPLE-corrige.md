# Fiche de cadrage : Exemple corrigé (tri des courriels de support)

> Exemple fourni par l'enseignant pour montrer le niveau de détail attendu. Ne pas recopier.

## Besoin en une phrase (obligatoire)

Orienter automatiquement chaque courriel reçu par le support vers l'équipe compétente (facturation, technique, commercial).

## Utilisateur final (obligatoire)

Les agents du support, qui reçoivent une file déjà triée au lieu d'une boîte commune.

## Approche retenue (obligatoire)

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire)

(a) Deux ans de courriels déjà étiquetés par l'équipe qui les a traités : des données étiquetées existent. (c) Plusieurs milliers de courriels par jour : un classifieur coûte presque rien par requête, un LLM coûterait à chaque appel. (d) Une erreur de tri se corrige en un clic par l'agent, la conséquence est faible.

## Données nécessaires et leur origine (obligatoire)

Export anonymisé des tickets (texte, équipe assignée) depuis l'outil de support ; suppression des adresses, noms et numéros avant tout traitement.

## Métrique de succès et seuil d'acceptation (obligatoire)

F1 macro sur un jeu de test tenu à l'écart ; acceptation à partir de 0,85, avec un rappel d'au moins 0,90 sur la classe "technique" (la plus urgente).

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un courriel mal orienté est renvoyé à la bonne équipe par l'agent ; le bouton "réassigner" alimente les données de réentraînement.

## Risques éthiques ou de confidentialité (obligatoire)

Les courriels contiennent des données personnelles : anonymisation avant stockage, modèle hébergé en interne, pas d'envoi à un service tiers.

## Approche écartée et pourquoi (facultatif)

Règles par mots-clés : testées en interne, 60 % d'exactitude seulement, trop de formulations imprévues.
