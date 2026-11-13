# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Vérifier automatiquement qu'une ordonnance contient les informations obligatoires avant sa validation par le pharmacien.

## Utilisateur final (obligatoire)
Le pharmacien ou le préparateur en pharmacie responsable du contrôle des ordonnances.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

 Je choisis les règles métier parce que les champs obligatoires d'une ordonnance peuvent être définis par des règles connues. Le critère (b) de vérifiabilité est important, car chaque anomalie doit pouvoir être expliquée. Le critère (d) est également essentiel, car valider à tort une ordonnance incomplète peut avoir des conséquences graves pour le patient.


## Données nécessaires et leur origine (obligatoire)
Les données nécessaires comprennent les informations figurant sur les ordonnances (identité du patient, date, prescripteur, médicaments et posologie). Elles proviennent des ordonnances traitées par la pharmacie et des exigences réglementaires applicables, avec anonymisation des données utilisées pour les tests.


## Métrique de succès et seuil d'acceptation (obligatoire)
L'application devra détecter au moins 99 % des ordonnances présentant un champ obligatoire manquant sur un jeu de test représentatif. Le taux de fausses alertes devra rester inférieur à 5 %.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une erreur peut entraîner la non-détection d'une ordonnance incomplète ou le signalement injustifié d'une ordonnance correcte. Le pharmacien devra systématiquement vérifier les alertes et conserver la responsabilité de la validation finale avant toute délivrance.

## Risques éthiques ou de confidentialité (obligatoire)
Les ordonnances contiennent des données personnelles et médicales sensibles qui doivent être protégées conformément au RGPD. L'application devra limiter les accès aux personnes autorisées, sécuriser le stockage et éviter toute utilisation non nécessaire des informations de santé.

## Approche écartée et pourquoi (facultatif)
Le machine learning est écarté car il nécessiterait des données étiquetées et pourrait produire des décisions moins facilement explicables. Les règles métier sont plus adaptées à la vérification de champs obligatoires clairement définis.
