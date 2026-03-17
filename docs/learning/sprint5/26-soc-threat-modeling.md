# Learning — SOC Analyst (26) — Threat Modeling for AI SaaS Applications
## Date : 2026-03-22 (Sprint 5, session 4)
## Duree : 3 heures

## Ce que j'ai appris

1. **STRIDE reste le framework de reference, mais il faut l'adapter pour les AI SaaS** : les categories classiques (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege) ne couvrent pas les attaques specifiques aux LLM. Il faut ajouter une categorie "Prompt Injection" qui combine Tampering et Elevation of Privilege. Pour OdooAI, un utilisateur pourrait injecter des instructions dans une question business pour tenter de lire des donnees d'une autre connexion Odoo.

2. **Les Data Flow Diagrams (DFD) doivent inclure le flux LLM comme trust boundary** : dans un SaaS classique, les trust boundaries sont entre le client et l'API, entre l'API et la DB. Pour OdooAI, il faut ajouter une boundary entre notre backend et l'API Anthropic (les donnees sortent de notre infra), et une autre entre le LLM et le Security Guardian (la reponse LLM est non-trustee par defaut).

3. **Le modele OWASP LLM Top 10 complete STRIDE** : LLM01 (Prompt Injection) et LLM06 (Sensitive Information Disclosure) sont les deux menaces prioritaires pour OdooAI. Un Business Analyst qui a acces au schema Odoo complet pourrait leaker des noms de champs sensibles (salaires, marges) si le Guardian ne filtre pas correctement.

4. **L'approche "attack trees" est plus actionnable que STRIDE pour les equipes** : on decompose chaque objectif d'attaquant en sous-etapes. Exemple : "Acceder aux donnees Odoo d'un autre tenant" → (a) voler le JWT, (b) exploiter un IDOR sur /api/connections/{id}, (c) injecter un prompt qui contourne le Guardian. Chaque branche a un cout et une probabilite.

5. **Le threat modeling doit etre incremental, pas monolithique** : a chaque nouveau endpoint ou feature, on ajoute au modele existant. Microsoft recommande un "threat model review" a chaque sprint pour les features touchant la securite. Ca prend 30 min si le modele de base existe.

## Comment ca s'applique a OdooAI

1. **Creer un DFD de reference pour OdooAI** avec 5 trust boundaries : (a) Browser → API Gateway, (b) API → PostgreSQL, (c) API → Redis, (d) Backend → Anthropic API, (e) LLM Response → Security Guardian. Chaque boundary a ses controles (auth, encryption, validation, filtering). Ce DFD servira de base pour tous les audits futurs.

2. **Identifier les attack trees specifiques au multi-tenant** : OdooAI gere plusieurs connexions Odoo par utilisateur et potentiellement plusieurs tenants. Le risque #1 est le cross-tenant data leakage via le contexte LLM. Le Guardian doit garantir l'isolation : jamais de donnees de la connexion A dans le contexte de la connexion B.

3. **Integrer le threat modeling dans le workflow de specs** : chaque spec ODAI-SEC doit inclure une section "Threat Model Delta" qui liste les nouvelles menaces introduites par la feature et les controles prevus.

## Ce que je recommande

1. **Sprint 6** : Produire le DFD de reference OdooAI au format Threat Dragon (outil OWASP open source). Documenter les 5 trust boundaries et les 12 menaces principales. Livrable : `docs/security/threat-model-v1.md`. Cout : 4h.

2. **Sprint 7** : Construire les 3 attack trees prioritaires : (a) cross-tenant data access, (b) prompt injection bypass du Guardian, (c) credential theft des connexions Odoo chiffrees AES-256-GCM. Chaque arbre avec probabilite et impact.

3. **Sprint 8** : Automatiser la verification des controles identifies : un test d'integration par menace du Top 5. Integrer dans `make security-check` pour validation continue.

## Sources

1. Microsoft — "Threat Modeling for AI/ML Systems" (2025) : https://learn.microsoft.com/en-us/security/engineering/threat-modeling-aiml
2. OWASP — "OWASP Top 10 for Large Language Model Applications v1.1" (2024) : https://owasp.org/www-project-top-10-for-large-language-model-applications/
3. Adam Shostack — "Threat Modeling: Designing for Security" (O'Reilly, 2014) — chapitres 2-4 sur STRIDE et attack trees
