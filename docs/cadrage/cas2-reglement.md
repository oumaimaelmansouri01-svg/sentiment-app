# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Permettre de consulter un règlement et d'obtenir des réponses fiables aux questions des utilisateurs.

## Utilisateur final (obligatoire)
Les étudiants et les membres de l'administration qui recherchent des informations dans le règlement.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
Je choisis le RAG parce que les réponses doivent provenir des documents officiels de l'établissement. Le critère (b) de vérifiabilité est essentiel, car les réponses doivent citer les articles du règlement. Le critère (a) est également pris en compte, car il n'est pas nécessaire de disposer d'un grand volume de questions-réponses étiquetées pour mettre en place cette approche.


## Données nécessaires et leur origine (obligatoire)
Les données nécessaires comprennent le règlement intérieur, les procédures administratives et les documents officiels de l'école. Elles seront fournies par l'administration de l'établissement sous forme de fichiers PDF ou de documents numériques régulièrement mis à jour.

## Métrique de succès et seuil d'acceptation (obligatoire)
L'application devra fournir au moins 90 % de réponses correctes sur un ensemble de 100 questions représentatives validées par l'administration. Au moins 95 % des réponses devront citer une source pertinente et vérifiable du règlement intérieur


## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une réponse incorrecte pourrait induire un étudiant en erreur concernant ses droits, ses obligations ou les procédures administratives. Les réponses ambiguës ou concernant des décisions importantes devront être vérifiées par le service administratif avant toute application.


## Risques éthiques ou de confidentialité (obligatoire)
L'application devra protéger les données personnelles éventuellement présentes dans les questions des utilisateurs et respecter le RGPD. Elle devra également limiter les risques d'hallucinations, éviter les réponses non fondées et signaler clairement lorsqu'aucune information fiable n'est disponible dans les documents.

## Approche écartée et pourquoi (facultatif)
Le modèle génératif seul est écarté, car il peut produire des réponses inventées ou obsolètes sans s'appuyer sur les documents officiels. Le RAG permet de rechercher les informations dans les sources de référence et de les citer pour améliorer la fiabilité des réponses.

