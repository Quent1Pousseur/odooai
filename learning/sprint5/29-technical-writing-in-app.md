# Learning — Tech Writer (29) — In-App Help Patterns (Tooltips, Guided Tours, Contextual Help)
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **Les tooltips contextuels ont le meilleur ROI** : un petit icone "?" a cote de chaque champ complexe avec une explication de 1-2 phrases reduit les tickets support de 30-40%. Pour OdooAI, chaque concept non-evident (connexion Odoo, Knowledge Graph, tokens) doit avoir un tooltip.

2. **Les guided tours (onboarding) augmentent l'activation de 70%** : des outils comme Shepherd.js ou React Joyride permettent de creer des tours interactifs en 5-7 etapes. Le tour ideal pour OdooAI : (1) Bienvenue, (2) Connecter Odoo, (3) Poser une premiere question, (4) Comprendre la reponse, (5) Explorer les conversations.

3. **Le pattern "Empty State Education"** : quand une section est vide (pas de conversations, pas de connexion), afficher un message educatif avec un CTA clair au lieu d'un ecran blanc. Exemple : "Connectez votre instance Odoo pour commencer a analyser vos donnees" avec un bouton "Connecter".

4. **L'aide contextuelle doit etre progressive** : niveau 1 = tooltips inline, niveau 2 = panneau d'aide lateral (cmd+?), niveau 3 = documentation complete. Ne jamais forcer l'utilisateur a quitter l'application pour trouver de l'aide. Le panneau lateral peut utiliser le LLM pour repondre aux questions sur l'utilisation.

5. **Les micro-copy (textes UI) sont la premiere ligne d'aide** : les labels de boutons, les placeholders, les messages d'erreur sont plus lus que toute documentation. "Analyser mes ventes Q1" est meilleur que "Envoyer". "Connexion echouee : verifiez l'URL et les identifiants" est meilleur que "Erreur 401".

## Comment ca s'applique a OdooAI

1. **Le premier contact avec OdooAI doit etre guide** : l'utilisateur arrive, connecte son Odoo, et ne sait pas quoi demander. Un onboarding tour + des suggestions de questions ("Quels sont mes 10 meilleurs clients ?", "Montre-moi le workflow de vente") transforment un utilisateur perdu en utilisateur actif.

2. **Les empty states sont partout en early-stage** : pas de conversations, pas d'historique, pas de KG charge. Chaque empty state doit eduquer et orienter. Le composant React `EmptyState` doit etre reutilisable avec titre, description, illustration, et CTA.

3. **Les erreurs de connexion Odoo sont le premier point de friction** : les messages d'erreur doivent expliquer exactement quoi faire. "L'URL doit etre au format https://moninstance.odoo.com" au lieu de "URL invalide". "L'utilisateur n'a pas les droits XML-RPC, activez-les dans Configuration > Technique" au lieu de "Acces refuse".

## Ce que je recommande

1. **Sprint 6** : Ecrire le contenu des tooltips pour tous les champs du formulaire de connexion Odoo et les integrer dans les composants Shadcn/ui existants. Creer le composant `EmptyState` reutilisable.

2. **Sprint 7** : Implementer le guided tour d'onboarding avec React Joyride (3.5 kB gzipped, compatible Next.js). 5 etapes couvrant connexion > premiere question > reponse > historique. Stocker la completion dans localStorage.

3. **Sprint 8** : Ameliorer tous les messages d'erreur de l'API avec des `user_message` clairs et actionnables. Chaque exception dans `odooai/exceptions.py` doit avoir un message technique ET un message utilisateur comprehensible.

## Sources

1. Nielsen Norman Group — "Tooltip Guidelines" (2024) : https://www.nngroup.com/articles/tooltip-guidelines/
2. Appcues — "User Onboarding Best Practices" (2025) : https://www.appcues.com/blog/user-onboarding-best-practices
3. React Joyride — "Create guided tours in React apps" : https://github.com/gilbarbara/react-joyride
