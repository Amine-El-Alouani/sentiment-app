# Banque de mini-cas (TP1)

Douze sujets de rechange, en plus des trois cas imposés. Ils servent à remplacer un cas, à en cadrer un quatrième (`python scripts/new_cadrage.py <fiche> "Titre"`) ou à varier les sujets d'une promotion à l'autre. Mêmes règles, même fiche, mêmes tests.

## Besoins d'entreprise

| Fiche | Cas | Indices à discuter |
| --- | --- | --- |
| `ent1-factures-doublons` | Une PME veut bloquer les factures fournisseurs qui seraient payées deux fois | Les critères d'un doublon sont-ils connus (numéro, montant, fournisseur, date) ? Le contrôleur doit-il pouvoir expliquer le blocage ? Que coûte un double paiement ? |
| `ent2-ruptures-stock` | Une chaîne de supermarchés veut prévoir les ruptures de stock par magasin et par produit | Historique des ventes sur plusieurs années. Des milliers de prévisions par jour. Que coûte une rupture, que coûte un surstock ? |
| `ent3-reponses-avis` | Une marque veut rédiger des brouillons de réponse aux avis clients publiés en ligne | Existe-t-il une bonne réponse unique ? Qui relit avant publication ? Coût par avis, ton de la marque à respecter. |

## Besoins des citoyens

| Fiche | Cas | Indices à discuter |
| --- | --- | --- |
| `cit1-triage-urgences` | Un centre d'appels d'urgence veut classer les appels par gravité pour prioriser l'envoi des secours | Des protocoles de triage existent déjà. Que coûte un appel grave classé mineur ? Données de santé ; qui décide en dernier ? |
| `cit2-demarches-commune` | Une commune veut répondre aux questions des habitants sur les démarches (état civil, urbanisme, taxes) | Les guides et formulaires existent. La réponse doit-elle citer le texte officiel ? Les questions contiennent-elles des données personnelles ? |
| `cit3-chutes-domicile` | Une association veut détecter les chutes des personnes âgées à domicile à partir d'un bracelet capteur | Enregistrements étiquetés chute ou non chute, mais rares. Que coûte une chute manquée, une fausse alerte ? Qui appelle avant d'intervenir ? |

## Besoins de l'université

| Fiche | Cas | Indices à discuter |
| --- | --- | --- |
| `uni1-decrochage` | L'université veut repérer à mi-semestre les étudiants à risque d'abandon à partir de la plateforme de cours et des notes | Historique étiqueté (diplômé, abandon) sur plusieurs promotions. Risque de stigmatisation ? Qui contacte l'étudiant, et pour lui proposer quoi ? |
| `uni2-variantes-exercices` | Un enseignant veut produire des variantes d'exercices corrigés pour ses séances de TD | Pas de vérité unique. Que coûte un corrigé faux distribué ? Relecture avant diffusion, coût par exercice. |
| `uni3-tuteur-cours` | Un département veut un assistant qui répond aux questions des étudiants à partir des polycopiés et des diapositives du cours | Les supports existent. La réponse doit-elle renvoyer à la page du polycopié ? A-t-on des questions étiquetées ? Risque : une réponse inventée hors du cours. |

## Besoins étatiques

| Fiche | Cas | Indices à discuter |
| --- | --- | --- |
| `etat1-rendements-agricoles` | Le ministère de l'agriculture veut prévoir les rendements céréaliers par province avant la récolte | Rendements passés par saison et par province, météo, images satellites. Quelques prévisions par an. Que coûte une erreur pour la planification des importations ? |
| `etat2-suivi-chantiers` | Un ministère veut répondre aux questions des citoyens sur l'avancement des chantiers publics à partir des rapports d'étape | Les rapports existent et sont mis à jour chaque mois. La réponse doit-elle citer le rapport et sa date ? Coût par question ? |
| `etat3-alerte-epidemie` | Le ministère de la santé veut déclencher des alertes à partir des déclarations hebdomadaires des centres de santé | Des seuils d'alerte sont définis par les protocoles de surveillance. Que coûte une alerte tardive, une fausse alerte ? Les épidémiologistes doivent-ils pouvoir vérifier le déclenchement ? |
