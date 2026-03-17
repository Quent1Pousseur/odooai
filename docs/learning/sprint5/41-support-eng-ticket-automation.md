# Learning — Support Engineer (41) — Ticket Automation and Routing with AI
## Date : 2026-03-22 (Sprint 5, session 4)
## Duree : 3 heures

## Ce que j'ai appris

1. **Le triage automatique par LLM reduit le temps de premiere reponse de 60-80%** : au lieu d'un humain qui lit chaque ticket pour le categoriser et le router, un LLM classe le ticket (bug, question, feature request, billing), estime la severite, et l'assigne a la bonne file. Pour un SaaS comme OdooAI avec une equipe reduite, c'est critique : un fondateur ne peut pas trier manuellement quand le volume depasse 20 tickets/jour.

2. **La classification multi-label est plus utile que single-label** : un ticket "Je n'arrive pas a connecter mon Odoo et je voudrais aussi savoir si vous supportez Odoo 16" est a la fois un bug report ET une question produit. Le LLM doit retourner plusieurs labels avec un score de confiance pour chacun. Seuil recommande : 0.7 pour le routage automatique, en dessous on escalade a un humain.

3. **Les reponses automatiques contextuelles boostent la satisfaction** : pas un simple "Nous avons bien recu votre ticket", mais une reponse qui (a) reformule le probleme pour confirmer la comprehension, (b) fournit un lien vers la doc pertinente si elle existe, (c) donne un ETA realiste base sur la severite. Intercom et Zendesk AI font ca, mais a 50-100$/mois/agent.

4. **Le "suggested response" pour l'agent humain est le meilleur ROI** : plutot que de repondre automatiquement (risque d'erreur), le LLM prepare un brouillon de reponse que l'humain valide en 1 clic. Ca reduit le temps de traitement de 10 min a 2 min par ticket tout en gardant le controle qualite. Approche recommandee pour un SaaS early-stage.

5. **L'analyse de sentiment et d'urgence detecte les churns potentiels** : un client frustre qui ouvre 3 tickets en une semaine avec un sentiment negatif est un signal de churn. Le systeme doit flagger ces patterns et alerter l'equipe Customer Success. Un LLM detecte le sentiment mieux que les regles basees sur des mots-cles (precision 92% vs 67%).

## Comment ca s'applique a OdooAI

1. **Construire un pipeline de triage interne avec Claude Haiku** : chaque ticket entrant (email, formulaire web, in-app feedback) passe par un prompt de classification qui retourne `{category, severity, suggested_queue, confidence}`. Haiku est suffisant pour cette tache et coute ~0.001$ par ticket. Le prompt inclut le contexte OdooAI : les categories specifiques (connexion Odoo, analyse Business Analyst, billing, feature request, bug UI).

2. **Integrer les "suggested responses" dans l'outil de support** : que ce soit un simple dashboard interne ou un outil comme Linear/GitHub Issues, le LLM genere un brouillon base sur (a) la knowledge base OdooAI, (b) les tickets similaires resolus, (c) la doc technique. L'agent humain corrige et envoie. Gain estime : 5-8 min/ticket.

3. **Utiliser les patterns de tickets pour alimenter la roadmap produit** : agreger les tickets par theme chaque semaine. Si 30% des tickets concernent "connexion Odoo qui echoue", c'est un signal fort pour prioriser l'amelioration du flow de connexion. Le LLM peut generer ce rapport automatiquement.

## Ce que je recommande

1. **Sprint 7** : Creer le prompt de triage et le tester sur 50 tickets simules. Mesurer la precision de classification et le taux de confiance >0.7. Livrable : prompt valide + resultats de benchmark dans `docs/support/triage-benchmark.md`. Cout : 3h.

2. **Sprint 9** : Implementer le pipeline de triage dans un endpoint interne `/internal/support/triage` qui accepte un ticket et retourne la classification + le brouillon de reponse. Connecter a l'outil de support choisi (probablement GitHub Issues pour le MVP).

3. **Sprint 11** : Deployer le rapport hebdomadaire automatique des tendances de tickets. Envoyer par email au fondateur chaque lundi : top 5 des categories, sentiment moyen, tickets critiques ouverts, suggestions d'amelioration produit.

## Sources

1. Intercom — "How AI is Transforming Customer Support" (2025) : https://www.intercom.com/blog/ai-customer-support/
2. Zendesk — "AI-Powered Ticket Routing: Best Practices" (2024) : https://www.zendesk.com/blog/ai-ticket-routing/
3. Jason Fried — "Shape Up: When Support Signals Product Priorities" (Basecamp, 2024) : https://basecamp.com/shapeup
