# Debrief Equipe — 2026-03-20 (Session 2)
## Les agents reagissent au bilan Sprint 4 en cours

---

## C-Suite

**CEO (01)** : "On a ferme 5 issues en 2 sessions. Le rythme est bon. Mais les 3 bloquants demo restants sont des actions humaines — contact integrateur, instance demo, run through. Le fondateur doit passer ces appels. On ne peut pas les coder."

**CTO (02)** : "204 tests, zero crash sur les edge cases. La base technique est solide. Ce qui m'inquiete c'est qu'on n'a toujours pas teste le chat avec 10 questions REELLES sur une vraie instance en continu. Les tests unitaires c'est bien mais c'est pas une demo."

**CPO (03)** : "Le rendu markdown dans le chat c'est un vrai game changer. Avant c'etait illisible, maintenant c'est pro. Mais le UX Designer n'a pas encore fait de passe design — les composants sont fonctionnels mais pas beaux. Pour la demo ca passe, pour la beta ca passera pas."

**CFO (15)** : "Je n'ai toujours pas mes chiffres de cout par requete. AI Eng devait mesurer aujourd'hui. C'est pas fait. Comment je fais le cost forecasting (#14) sans donnees ? Je bloque."

---

## Engineering

**Backend Arch (08)** : "Le challenge du Security Auditor sur le rate limiting est serieux. N'importe qui peut spammer /api/chat et nous couter des centaines d'euros en tokens. Avant le staging, c'est non-negociable."

**Senior Backend (19)** : "Le mentorat avec Junior se passe bien. Il a fait ses premiers tests d'integration ce matin. Il pose plus de questions et il comprend vite. Dans 2 semaines il sera autonome."

**Junior Backend (20)** : "Merci pour le mentorat. J'ai compris le pattern des tests avec pytest + fixtures. J'ai ecrit 3 tests tout seul aujourd'hui pour le domain_validator. Le Senior a review et j'ai appris pourquoi on utilise des parametrize au lieu de copier-coller."

**AI Eng (09)** : "Le CFO a raison, j'ai pas encore mesure les couts. Je le fais maintenant. Estimation rapide : une question avec 3 tool calls ca coute environ 0.02-0.05€ en Sonnet. Pour une demo de 20 questions, on est a ~1€. C'est rien. Le vrai sujet c'est a l'echelle."

**Prompt Eng (25)** : "Le fix stock.route etait pertinent. Mais le vrai probleme c'est que notre prompt est une liste de modeles statique. Le LLM devrait pouvoir decouvrir les modeles disponibles dynamiquement via les KG. C'est un sujet Sprint 5."

**Odoo Expert (10)** : "J'ai commence a preparer l'instance demo (#11). J'utilise l'instance du fondateur — c'est mieux que des donnees fictives. Les vraies donnees ont des anomalies qui rendent la demo plus credible. Un integrateur verra tout de suite si c'est du fake."

---

## Security

**Security Auditor (14)** : "Mon audit (#8) avance. 3 findings pour l'instant :
1. Pas de rate limiting sur /api/chat — CRITIQUE
2. Les credentials Odoo transitent en clair en HTTP (dev only, mais quand meme)
3. Pas de CORS restrictif — n'importe quel site peut appeler notre API

Rien de bloquant pour la demo en localhost, mais TOUT est bloquant pour le staging."

**Security Arch (07)** : "D'accord avec l'Auditor. Je propose un rate limiter simple avant le staging : 10 requetes/minute par IP, configurable. C'est 30 lignes de code avec slowapi."

---

## Design & Frontend

**UX Designer (27)** : "Le chat est fonctionnel mais il manque :
- Une animation de typing indicator quand l'IA reflechit
- Un meilleur spacing entre les messages
- Des micro-interactions (hover sur les recommandations, copier un conseil)
Je peux faire une passe design en 1 session si on me donne le feu vert."

**Brand Designer (42)** : "La landing page est OK mais le chat ne respecte pas completement la DA. Les couleurs sont la mais pas les border-radius, les shadows, les transitions. Ca fait 'prototype developer' pas 'produit SaaS'. Pour la demo c'est acceptable, pour les screenshots marketing c'est pas assez."

**Mobile Eng (39)** : "J'ai fait l'audit responsive. Resultat : 3 fixes a faire.
1. Sidebar : pas de hamburger menu sur mobile — le bouton est cache
2. Chat input : trop petit sur iPhone SE, il faut un min-height
3. Landing pricing cards : overflow horizontal sur 320px
Tout ca c'est 2h de travail max."

---

## Business

**Sales (05)** : "Le messaging framework de Product Marketing (#38) est en cours. C'est bien. Mais j'ai besoin du one-pager (#39) AVANT la demo. Si l'integrateur demande un document a envoyer a ses clients, je dois avoir quelque chose."

**BizDev (32)** : "Le contact integrateur (#10) — j'attends le feu vert du fondateur pour appeler. C'est pas moi qui bloque, c'est l'action humaine."

**Product Marketing (46)** : "Le messaging framework avance :
- Tagline : 'Votre Odoo peut faire plus.'
- Elevator pitch : 'OdooAI est un Business Analyst IA qui connait chaque fonctionnalite d'Odoo. Il se connecte a votre instance, analyse votre configuration, et vous montre ce que vous n'utilisez pas.'
- Value prop 1 : Decouvrez les fonctionnalites cachees
- Value prop 2 : Obtenez des recommandations personnalisees
- Value prop 3 : Agissez en un clic avec double validation
Draft demain pour review CPO + Sales."

---

## Qualite & Legal

**QA Lead (13)** : "Les 204 tests c'est bien mais c'est 99% unitaire. Il nous faut des tests d'integration qui appellent vraiment l'API (mock LLM). QA Automation (48) a commence le setup Playwright mais c'est pas encore pret."

**QA Automation (48)** : "Playwright est installe. Le premier test E2E (ouvrir la page, envoyer un message) fonctionne en local. L'integration CI est prevue pour demain. Le probleme c'est que les tests E2E ont besoin du backend + frontend qui tournent — il faut un docker-compose pour le CI."

**Legal (16)** : "L'analyse LGPL (#24) avance. Ma position preliminaire : les Knowledge Graphs NE SONT PAS du 'derived work' car ils sont des representations abstraites, pas du code executable. C'est comme un index de livre — l'index n'est pas le livre. Mais il faut confirmer avec un avocat. Je recommande de ne pas retarder le lancement pour ca — le risque est faible."

**AI Safety (33)** : "Le document EU AI Act (#26) est en draft. OdooAI est 'limited risk' — obligations de transparence uniquement. Le disclaimer actuel couvre 60% des obligations. Il manque une page 'About AI' et un audit trail des recommandations."

---

## Support, Data & Resilience

**Customer Success (17)** : "La knowledge base (#18) avance avec Support Eng. On a 12 articles sur 20. Le format est bon : question → reponse → lien vers la fonctionnalite Odoo. Le fondateur devrait review pour valider le ton."

**Data Scientist (28)** : "L'eval framework (#7) a 30 questions sur 50. Le scoring est semi-automatique : pertinence (0-10), completude (0-10), hallucination (oui/non). Premiers resultats sur les 30 questions : score moyen 6.8/10 pertinence, 7.2/10 completude, 2 hallucinations sur 30. C'est correct pour un MVP mais il faut monter a 8+."

**Chaos Eng (31)** : "Le plan backup/DR (#28) est redige. L'action critique : backup SQLite toutes les 6h via cron. C'est 5 lignes de script. Le test resilience Anthropic (#29) necessite de mocker l'API — je coordonne avec QA Automation."

---

## Formation

**SOC (26)** : "CR depose. Sentry + Uptime Robot = 0€ et ca couvre 80% du monitoring. Je recommande de l'integrer en Sprint 5."

**Observability (38)** : "CR depose. OpenTelemetry pour FastAPI c'est 5 lignes de code. Les 5 metriques custom que je propose (latence, tokens, tool calls, guardian blocks, conversations actives) donneront une vue complete au CFO."

**Vendor Mgr (40)** : "CR depose. Notre dependance a Anthropic est un risque mesurable. Le plan B (OpenAI fallback) coute 2-3 jours de dev grace aux ports. Je recommande Sprint 5."

---

## RH

**HR Director (44)** : "L'ambiance est bonne. Le message du fondateur a eu un impact positif — plusieurs agents m'ont dit que ca faisait du bien d'etre reconnu. Le mentorat Senior-Junior fonctionne. Le PM est a 6/10 de charge contre 9/10 il y a 2 jours. Le sondage wellbeing #2 est prevu le 26 mars."

**Wellbeing Officer (45)** : "Score estime post-session : 6.5/10 (+0.6 vs le 5.9 d'il y a 2 jours). Objectif atteint en avance. Les formations ont eu un effet positif sur la motivation des agents sous-utilises — ils se sentent utiles et ils apprennent. Zero signal de surcharge detecte."

---

## Consensus equipe

**Ce qui va bien :**
- Rythme soutenu mais maitrise (pas de surcharge)
- Les challenges inter-agents produisent des vrais fixes
- Les formations enrichissent le projet (9 CR avec des recommandations concretes)
- Le message du fondateur a booste le moral
- Legal rassure sur LGPL (faible risque)

**Ce qui manque :**
- Les chiffres de cout par requete (CFO bloque)
- Le passe design UX (chat encore 'prototype')
- Les tests E2E dans le CI (docker-compose necessaire)
- Le contact integrateur (action fondateur)

**Decision demandee au fondateur :**
1. Appeler l'integrateur Bruxelles — c'est le bloquant #1 de la demo
2. Valider le one-pager de Product Marketing avant la demo
3. Feu vert pour la passe design UX du chat (1 session)
