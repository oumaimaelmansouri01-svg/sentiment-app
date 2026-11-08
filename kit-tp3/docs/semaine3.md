# Semaine 3 : l'API, notes du binôme

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

L'API a besoin du modèle pour effectuer les prédictions. Si le fichier sentiment.joblib est absent, elle ne peut pas assurer sa fonction principale. Il est donc préférable de bloquer son démarrage plutôt que de laisser fonctionner un service incapable de répondre correctement. Cela permet aussi de détecter immédiatement le problème et de le corriger avant d'utiliser l'API.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

Les deux vérifications peuvent sembler redondantes, mais elles interviennent à des niveaux différents. Pydantic vérifie les données reçues par l'API et renvoie une erreur 422 si le texte est vide. La fonction predict() effectue sa propre vérification pour éviter de traiter un texte invalide lorsqu'elle est appelée directement, sans passer par l'API. Ces deux contrôles sont donc complémentaires et rendent l'application plus fiable.
