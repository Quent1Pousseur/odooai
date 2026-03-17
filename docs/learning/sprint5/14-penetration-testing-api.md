# Learning — Security Auditor (14) — API Penetration Testing Methodologies (OWASP API Top 10)
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **OWASP API Top 10 2023 reorganise les priorites** : API1 (Broken Object Level Authorization) reste #1. Pour OdooAI, ca signifie que chaque endpoint qui retourne des donnees Odoo doit verifier que le user a acces a CETTE connexion specifique, pas juste qu'il est authentifie. API2 (Broken Authentication) couvre les tokens JWT mal valides.

2. **API3 (Broken Object Property Level Authorization)** est critique pour nous : quand le Business Analyst retourne des donnees Odoo, il ne doit jamais exposer des champs auxquels le role de l'utilisateur n'a pas acces. Le Security Guardian doit filtrer les proprietes AVANT la reponse LLM, pas apres.

3. **API5 (Broken Function Level Authorization)** s'applique aux endpoints admin : `/api/connections` pour creer/modifier des connexions Odoo doit etre restreint au owner. Les endpoints de l'agent doivent etre separes des endpoints d'administration. Principe du moindre privilege.

4. **Les outils de pentest API modernes** : Burp Suite Pro pour l'interception, OWASP ZAP pour le scan automatise, Postman/Newman pour les tests de regression securite. Nuclei avec des templates custom est le plus efficace pour CI : on ecrit des templates YAML specifiques a nos endpoints.

5. **Rate limiting et abuse prevention** : API4 (Unrestricted Resource Consumption) est critique pour un SaaS avec LLM. Sans rate limit, un attaquant peut bruler notre budget Anthropic. Il faut limiter par user, par connexion, par endpoint, avec des budgets token journaliers.

## Comment ca s'applique a OdooAI

1. **Le Security Guardian (ZERO LLM) doit couvrir API1 et API3** : chaque requete passe par le Guardian qui verifie (a) l'ownership de la connexion, (b) les champs autorises pour ce role. C'est de la logique pure, pas de LLM, exactement comme specifie dans l'architecture.

2. **Rate limiting multi-couche pour proteger le budget LLM** : implementer un middleware FastAPI qui limite les requetes par user (100/h), par connexion (50/h), et les tokens LLM par jour (100k tokens/user free tier). Redis est deja dans la stack pour ca.

3. **Pipeline de tests securite en CI** : Nuclei templates custom pour chaque endpoint OdooAI, executes a chaque PR. Ca complete les tests unitaires avec des tests d'intrusion automatises.

## Ce que je recommande

1. **Sprint 6** : Ecrire les Nuclei templates pour les endpoints existants (`/health`, `/api/connections`). Les integrer dans le Makefile : `make security-scan`. Cout : 3h.

2. **Sprint 7** : Implementer le rate limiting middleware dans `odooai/api/middleware.py` avec Redis backend. Trois niveaux : request/min, request/hour, tokens/day par user.

3. **Sprint 8** : Audit complet OWASP API Top 10 sur tous les endpoints agent. Rapport formel avec findings, severity, remediation. Gate de validation avant la beta publique.

## Sources

1. OWASP — "API Security Top 10 2023" : https://owasp.org/API-Security/editions/2023/en/0x11-t10/
2. ProjectDiscovery — "Nuclei Templates for API Testing" (2025) : https://github.com/projectdiscovery/nuclei-templates
3. Trail of Bits — "Building Secure APIs" (2024) : https://blog.trailofbits.com/category/security-reviews/
