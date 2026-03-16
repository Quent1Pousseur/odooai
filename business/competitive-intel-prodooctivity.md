# Rapport Competitive Intelligence — Prodooctivity
## Agent : Competitive Intel (34)
## Date : 2026-03-20
## Classification : CONFIDENTIEL

---

## 1. Qu'est-ce que Prodooctivity ?

Un **gateway MCP securise** qui connecte les assistants IA (Claude, GPT, Gemini) a des instances Odoo. Ce n'est PAS un chat — c'est un middleware. L'IA questionne Odoo via des outils standardises MCP.

**Positionnement** : infrastructure pour developpeurs et integrateurs, pas pour les PME directement.

---

## 2. Stack technique

| Couche | Prodooctivity | OdooAI |
|--------|--------------|--------|
| Backend | Python 3.12, FastAPI, SQLAlchemy async | Python 3.11+, FastAPI, SQLAlchemy async |
| DB | PostgreSQL 16 + pgvector | SQLite (dev), PostgreSQL (prevu) |
| Cache | Redis 7 | Redis (prevu) |
| LLM | Anthropic Claude (via OpenAI SDK) | Anthropic Claude (SDK natif) |
| Frontend | Next.js 15, Tailwind v4, shadcn/ui | Next.js 14, Tailwind, shadcn/ui |
| Auth | OAuth 2.1 + PKCE, JWT | Aucune (a implementer) |
| Billing | Stripe integre | Aucun (spec en cours) |
| MCP | Complet (Streamable HTTP) | Aucun (spec en cours) |
| Monitoring | Prometheus, structlog | structlog seulement |
| Tests | pytest, mypy strict | pytest, mypy strict, 204 tests |

**Constat** : stacks quasi identiques. La difference est la maturite — ils sont en avance de ~3-4 mois sur l'infra.

---

## 3. Comment ils connectent Odoo

Double protocole :
- **JSON-RPC 2.0** pour Odoo 19+ (nouveau)
- **XML-RPC** pour Odoo 17/18 (legacy)

Abstrait derriere une interface unique `OdooClient`. Exactement comme nous.

---

## 4. Leur MCP Server

C'est leur produit principal :
- 5 outils : `odoo_schema`, `odoo_search`, `odoo_read`, `odoo_search_read`, `odoo_execute`
- 2 outils connexion : `odoo_list_connections`, `odoo_switch_connection`
- 1 outil fichier : `odoo_get_attachment`
- Transport SSE (Streamable HTTP)
- OAuth 2.1 complet avec PKCE

**Chaque appel passe par** : RBAC → Quota → OdooClient → Anonymisation → Audit

---

## 5. Ce qu'ils font mieux que nous

| Avantage | Detail | Impact |
|----------|--------|--------|
| **Multi-tenant** | Isolation complete par tenant, 16+ repositories | Pret pour les integrateurs |
| **RBAC 4 couches** | Default → Plan → Role → Account, field-level | Securite enterprise |
| **Stripe integre** | Webhooks, subscriptions, overage pricing | Revenus possibles |
| **OAuth 2.1** | Server OAuth complet avec PKCE | Standard MCP |
| **MCP natif** | Streamable HTTP, connection switching | Compatible Claude Desktop |
| **Dashboard** | Enterprise (equipe, RBAC, audit), Individual (usage) | Self-service |
| **Monitoring** | Prometheus + structlog | Observabilite prod |
| **~43K LOC** | Backend 26K + Frontend 15K | Produit mature |

---

## 6. Ce qu'on fait mieux qu'eux

| Avantage OdooAI | Detail | Impact |
|-----------------|--------|--------|
| **Knowledge Graphs** | 1218 modules parses, 5514 modeles, 21013 champs du CODE SOURCE | Ils n'ont pas ca |
| **BA Profiles** | Intelligence business generee par LLM sur 9 domaines | Recommandations proactives |
| **Code Analyst** | Parseur AST Python + XML du code Odoo | Comprend les workflows, pas juste les champs |
| **Reponses orientees business** | "Vous n'utilisez pas X, voici pourquoi l'activer" | Eux = data brute |
| **Chat web integre** | Interface utilisateur directe, pas juste un gateway | Accessible aux non-techniques |
| **Security Guardian** | Classification modeles, anonymisation, domain validator | Zero LLM dans la securite |

**Notre moat** : on comprend Odoo SEMANTIQUEMENT. Eux exposent les donnees, nous les interpretons.

---

## 7. Leurs faiblesses

1. **Pas d'intelligence metier** — ils exposent les donnees brutes via MCP. Aucune recommandation, aucun diagnostic. Le LLM doit tout comprendre seul.
2. **Schema SQL monolithique** — 40K+ LOC dans la migration initiale. Difficile a evoluer.
3. **Sur-ingenierie RBAC** — 4 couches de policies cascadees, couple au billing Stripe. Complexite enorme pour un gain marginal vs un simple role-based.
4. **Dependance Redis** — cache partout (policies, credentials, budgets). Si Redis tombe, beaucoup de choses cassent.
5. **OAuth server maison** — au lieu d'utiliser Auth0/Supabase. Maintenance lourde.
6. **Pas de Code Intelligence** — ils ne parsent pas le code source Odoo. Ils ne savent pas ce qu'un module PEUT faire, juste ce qu'il A.

---

## 8. Taille et maturite

| Metrique | Prodooctivity | OdooAI |
|----------|--------------|--------|
| LOC backend | ~26K | ~5K |
| LOC frontend | ~15K | ~2K |
| Total | ~43K | ~7K |
| Fichiers | ~240 | ~135 |
| Tests | Peu | 204 |
| Migrations DB | 5 | 1 |
| MCP tools | 8 | 0 |
| Stripe | Oui | Non |

Ils ont ~6x plus de code. Mais la majorite c'est de l'infra (billing, RBAC, OAuth) pas de l'intelligence metier.

---

## 9. Strategie recommandee

### Court terme (Sprint 4-6) — Ne PAS les copier
- Ne pas implementer MCP, OAuth, Stripe maintenant
- Concentrer sur la QUALITE des reponses (pertinence 8+/10)
- Ameliorer le chat web (notre interface directe vs leur gateway)
- Multi-tenant simple (1 Odoo par user)

### Moyen terme (Sprint 7-10) — Combler les gaps critiques
- Auth utilisateur (JWT simple, pas OAuth server)
- Stripe basique (3 plans, webhooks)
- MCP server (pour etre compatible Claude Desktop)
- Staging deploye

### Long terme — Notre avantage competitif
- **Knowledge Graphs + BA Profiles** = ce qu'ils n'auront jamais sans refaire leur architecture
- **Recommandations proactives** = "Vous devriez activer X" vs "Voici les donnees de X"
- **Chat direct** pour PME vs **Gateway technique** pour developpeurs
- **2 marches differents** : eux = infra pour devs, nous = IA pour business users

---

## 10. Verdict

**Prodooctivity est un concurrent serieux mais sur un marche different.**

Ils vendent un middleware technique aux developpeurs et integrateurs. Nous vendons un Business Analyst IA aux dirigeants de PME.

Si on les copie, on perd. Si on se concentre sur notre moat (intelligence du code source + recommandations business), on gagne.

> "Ils savent ce que votre Odoo A. Nous savons ce que votre Odoo PEUT faire." — Competitive Intel (34)
