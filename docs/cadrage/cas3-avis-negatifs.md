# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Détecter automatiquement les avis négatifs afin d'identifier les insatisfactions des clients et faciliter leur traitement.

## Utilisateur final (obligatoire)
Les collaborateurs du service client et les responsables qualité chargés d'analyser les avis.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
Je choisis le machine learning parce que les avis clients peuvent être étiquetés pour entraîner un modèle de classification, ce qui correspond au critère (a). Le critère (c) est important, car le coût par prédiction doit rester faible pour traiter des milliers d'avis. Le critère (d) est également pris en compte, car les erreurs de classification peuvent être corrigées par une vérification humaine.


## Données nécessaires et leur origine (obligatoire)
Les données nécessaires comprennent les commentaires des clients, les notes attribuées aux produits, les dates de publication et les catégories de réclamations. Elles proviendront de l'historique des avis du site e-commerce et seront étiquetées selon leur sentiment et leur niveau de priorité pour constituer un jeu d'entraînement.

## Métrique de succès et seuil d'acceptation (obligatoire)
Le modèle devra atteindre un score F1 d'au moins 85 % pour la classification des avis négatifs sur un jeu de test indépendant. Le rappel des avis jugés urgents devra être supérieur ou égal à 95 % afin de limiter les réclamations prioritaires non détectées.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une erreur de classification pourrait conduire à ignorer une réclamation urgente ou à traiter en priorité un avis peu important. Les agents du service client devront pouvoir consulter et corriger les classifications proposées, et les avis présentant un niveau d'incertitude élevé seront soumis à une vérification humaine.

## Risques éthiques ou de confidentialité (obligatoire)
Les avis peuvent contenir des données personnelles telles que des noms, des coordonnées ou des informations sur les commandes. L'application devra respecter le RGPD, anonymiser les informations sensibles et limiter les risques de biais liés à la langue, au style d'écriture ou au profil des clients.

## Approche écartée et pourquoi (facultatif)
Le RAG est écarté, car l'objectif principal n'est pas de rechercher des informations dans des documents, mais de classer automatiquement des avis clients. Un modèle de machine learning supervisé est plus adapté à cette tâche répétitive et permet d'optimiser le traitement d'un grand volume de données.

