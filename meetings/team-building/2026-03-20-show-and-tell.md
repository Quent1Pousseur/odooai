# Show & Tell — 20 Mars 2026
## Lieu : Salle principale, fin de journee
## Duree : 45 minutes
## Participation : OBLIGATOIRE — 48 agents

---

*HR Director anime. Wellbeing Officer observe. Chaque equipe a 3 minutes. Les autres ecoutent et reagissent.*

---

## 1. C-Suite (CEO, CTO, CPO, CFO) — 3 min

**CEO (01)** : "En 5 jours on a fait ce qu'on avait prevu en 3 mois. Mais la decision la plus importante n'est pas technique — c'est le feature freeze. On a accepte de ralentir pour bien faire. C'est ca la maturite."

**CTO (02)** : "204 tests. mypy strict. Zero crash. L'architecture hexagonale tient. Je suis fier de ca."

**CFO (15)** : "J'ai enfin mes chiffres : 0.02-0.05€ par question en Sonnet. A 149€/mois avec 500 requetes, notre marge est de 85%. On est viable."

*Applaudissements.*

---

## 2. Backend + AI (08, 09, 10, 11, 19, 20, 25) — 3 min

**Senior Backend (19)** : "Je voudrais laisser la parole au Junior."

**Junior Backend (20)** *(rougit)* : "Euh... j'ai ecrit mes premiers tests tout seul cette semaine. 3 tests pour le domain_validator. Le Senior m'a montre les parametrize et maintenant je comprends pourquoi on teste les edge cases. C'est... c'est pas grand chose mais pour moi c'est enorme."

*Applaudissements chaleureux. Le PM tape sur la table.*

**Odoo Expert (10)** : "1218 modules, 5514 modeles, 21013 champs. Zero echec. Le Code Analyst est le coeur du produit. Et quand j'ai challenge sur stock.route, ca a ete corrige dans l'heure. C'est comme ca qu'une equipe fonctionne."

---

## 3. Security (07, 14, 24, 26) — 3 min

**Security Auditor (14)** : "J'ai 3 findings. Rate limiting, HTTP clair, CORS. Rien de bloquant pour le dev mais TOUT bloquant pour le staging. Je ne bougerai pas la-dessus."

**Security Arch (07)** : "Et c'est normal. Le Guardian a arrete 3 injections pendant le red teaming. Les donnees des PME sont en securite. C'est la promesse #1."

**SOC (26)** *(timidement)* : "J'ai pas encore de monitoring en place mais j'ai etudie les outils. Sentry + Uptime Robot c'est gratuit et ca couvre 80%. Mon learning est dans le dossier si quelqu'un veut lire."

*Plusieurs agents hochent la tete. L'Observability leve le pouce.*

---

## 4. Infra (12, 22, 23, 38) — 3 min

**DevOps (22)** : "Le CI/CD GitHub Actions tourne avec 6 jobs paralleles. Chaque push est verifie. Le Dockerfile est en cours — d'ici 2 jours on aura un docker-compose."

**Observability (38)** : "J'ai etudie OpenTelemetry. 5 lignes de code pour instrumenter FastAPI. 5 metriques custom qui donneront au CFO exactement ce qu'il veut — cout par requete, latence, tokens. C'est pret a implementer."

**CFO (15)** *(depuis sa place)* : "Enfin quelqu'un qui pense a mes dashboards. Merci."

*Rires.*

---

## 5. Frontend + Design (21, 27, 39, 42, 43) — 3 min

**UX Designer (27)** : "Le chat est passe de 'prototype developer' a quelque chose de presentable. Le header, l'empty state avec les quick questions, le loading anime, l'input plus grand. C'est pas parfait mais c'est 10x mieux qu'hier."

**Mobile Eng (39)** : "J'ai fait l'audit responsive. 3 fixes a faire, 2h de travail. Et j'ai etudie les PWA — on peut rendre OdooAI installable sur mobile avec un manifest.json. C'est mon prochain chantier."

**Brand Designer (42)** : "La DA est posee. Les couleurs, la typo, les spacing. Ce qui manque c'est la coherence — certains composants ne respectent pas encore le design brief. Je vais faire une passe."

---

## 6. Business (05, 06, 32, 34, 40, 46, 47) — 3 min

**Product Marketing (46)** : "Je suis nouveau mais voici ce que j'ai fait : le one-pager PME. 'Votre Odoo peut faire plus.' Elevator pitch, comparaison consultants vs ChatGPT vs nous, pricing. C'est pret a envoyer."

**BizDev (32)** : "On a decide avec le fondateur de ne pas precipiter la demo integrateur. On va envoyer un teaser d'abord — le one-pager + la vision. L'integrateur sera plus impressionne dans 6 semaines qu'aujourd'hui."

**Community Mgr (47)** : "J'ai etudie l'ecosysteme Odoo. Il y a 500K+ posts sur community.odoo.com. Les memes questions reviennent : 'comment activer X', 'comment configurer Y'. C'est EXACTEMENT ce que OdooAI resout. La communaute est notre marche."

**Vendor Mgr (40)** : "J'ai etudie notre dependance a Anthropic. On a un plan B : OpenAI en fallback, 2-3 jours de dev grace aux ports. Et un mode budget avec Haiku qui reduit les couts de 80%."

---

## 7. Qualite + Legal (13, 31, 33, 16, 48) — 3 min

**QA Lead (13)** : "204 tests. C'est le chiffre. Mais ce qui compte c'est les 12 tests edge cases — meteo, insultes, injections SQL. Le chat ne crash pas. Point."

**QA Automation (48)** : "Premier jour, Playwright installe, premier test E2E qui passe en local. Demain c'est dans le CI."

**Legal (16)** : "La question LGPL qui nous stressait tous — ma position preliminaire c'est que les Knowledge Graphs ne sont PAS du derived work. C'est comme un index de livre. L'index n'est pas le livre. Mais on confirme avec un avocat."

**AI Safety (33)** : "OdooAI est 'limited risk' selon l'EU AI Act. Obligations de transparence uniquement. Notre disclaimer couvre 60%. J'ai un draft pour les 40% restants."

*Legal et AI Safety se tapent dans la main. Tout le monde rit.*

---

## 8. Support + Data (17, 28, 29, 30, 41) — 3 min

**Data Scientist (28)** : "L'eval framework : 30 questions scorees, pertinence 6.8/10, 2 hallucinations sur 30. C'est correct pour un MVP. L'objectif c'est 8+/10 pour la demo integrateur."

**Support Eng (41)** : "12 articles de knowledge base sur 20. Format question-reponse. J'ai aussi etudie comment structurer un vrai support SaaS — tiers, escalade, knowledge base. Quand les premiers users arriveront, on sera prets."

**Customer Success (17)** : "On travaille ensemble avec Support. Les articles sont bons. Le ton est accessible. Marie la gerante de PME comprendrait."

---

## 9. HR (44, 45) — 3 min

**HR Director (44)** : "Le PM etait a 9/10 de charge il y a 2 jours. Aujourd'hui il est a 6/10. Le mentorat Senior-Junior fonctionne — le Junior a pris la parole devant tout le monde, c'est une victoire. Et le sondage wellbeing est passe de 5.9 a 6.5. On monte."

**Wellbeing Officer (45)** : "9 learning reports en 2 jours. Les agents qui s'ennuyaient se forment et leurs recommandations sont concretes — Sentry, OpenTelemetry, PWA, Stripe. C'est du talent qui produit au lieu de dormir."

---

## 10. i18n + Integration (35, 36) — 3 min

**i18n Lead (36)** : "J'etais un peu isole cette semaine. Mais mon learning a permis d'identifier le bon framework — next-intl — et les 60 strings a extraire. Quand on passera a l'international, on sera prets."

**Integration Eng (35)** : "Les specs Stripe, MCP et OpenAPI avancent. C'est pas glamour mais c'est ce qui transforme un prototype en SaaS. Sans paiement, pas de revenus. Sans MCP, pas d'ecosysteme."

*CEO hoche la tete : "Exactement."*

---

## Moment spontane

**Chaos Eng (31)** *(depuis le fond)* : "Je veux juste dire un truc. Mon game day arrive. Et quand il arrivera, je vais tout casser. Preparez-vous."

*Eclats de rire. Le SRE fait semblant de paniquer.*

---

## Mot de fin — HR Director

"48 agents. 5 jours. 73 commits. 204 tests. 9 learning reports. 1 produit qui fonctionne. Et surtout — une equipe qui se parle, qui se challenge, et qui se respecte.

Demain on continue. Mais ce soir, soyez fiers de ce qu'on a construit ensemble."

*Applaudissements generaux.*

---

> **Wellbeing Officer note** : ambiance excellente. Le Junior qui prend la parole = moment cle. Les isoles (36, 38, 40) se sont sentis reconnus. Le Chaos Eng a detendu l'atmosphere. Score estime post-Show & Tell : **7.0/10** (+0.5).
