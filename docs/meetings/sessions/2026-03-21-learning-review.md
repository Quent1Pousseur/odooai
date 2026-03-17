# Review des Learnings — Integration Sprint 5
## Date : 2026-03-21
## Participants : 48 agents + Fondateur
## Facilitateur : HR Director (44)

---

## Principe

26 learning CRs produits pendant Sprint 4. Certains contiennent des recommandations actionnables qui doivent etre integrees au Sprint 5. On passe chaque CR en revue, on decide : **integrer maintenant**, **planifier plus tard**, ou **noter pour reference**.

---

## Tour de table — Chaque agent presente sa recommandation cle

### INFRA & SECURITE (Quick wins — integrer Sprint 5)

**DevSecOps (24) — Rate limiting** : "slowapi, 30 lignes, 30 minutes. 10 req/min sur /api/chat. C'est le finding #1 du Security Auditor."
- **Decision : INTEGRER Sprint 5, Jour 1** ✅
- Issue : S5-02

**SOC (26) — Sentry** : "3 lignes dans main.py. Sentry free tier = 5K errors/mois. Alerte sur chaque 500."
- **Decision : INTEGRER Sprint 5, Jour 1** ✅
- Issue : S5-10

**Observability (38) — OpenTelemetry** : "5 lignes pour instrumenter FastAPI. 5 metriques custom : latence, tokens, tool calls, guardian blocks, conversations actives."
- **Decision : INTEGRER Sprint 5, Semaine 1** ✅
- Issue : S5-11
- **CFO (15)** : "Les metriques tokens et latence sont critiques pour mon dashboard financier. Prioritaire."

**Chaos Eng (31) — Disaster Recovery** : "Backup SQLite toutes les 6h via cron. Runbook Anthropic down = fallback BA Profile only."
- **Decision : INTEGRER Sprint 5** ✅ (backup) + **Game day** (test fallback)
- Issues : S5-23

### CODE QUALITY (Integrer Sprint 5)

**CTO (02) — Async patterns** : "asyncio.gather() pour paralleliser les queries live_context. Gain 600ms-1.5s. Semaphore pour rate limiter les appels Anthropic."
- **Decision : INTEGRER Sprint 5** ✅
- A integrer dans le fix live_context
- **SRE (23)** : "Ca ameliore directement la latence. P0."

**Data Eng (11) — Index inverse KG** : "Index champ→module→modele pour lookups O(1). Utile pour le cross-domain et le domain detection."
- **Decision : INTEGRER Sprint 5** ✅
- Issue : S5-12
- **Backend Arch (08)** : "Ca pourrait remplacer le keyword matching par un lookup dans les KG. Plus precis."

### UX & FRONTEND (Integrer Sprint 5)

**UX Designer (27) — Design system** : "5 composants manquants : copy button, feedback thumbs, sources cliquables, code blocks, skeleton loading. Chacun < 1h."
- **Decision : INTEGRER copy + feedback Sprint 5** ✅, reste Sprint 6
- Issues : S5-08
- **CPO (03)** : "Copy et feedback sont les 2 plus importants. Le reste peut attendre."

**Chat Eng (43) — Typing indicators** : "ToolCallCard avec model Odoo + status en temps reel. Reduit frustration percue de 40%."
- **Decision : INTEGRER Sprint 5** ✅
- Issue : S5-13
- **UX Designer (27)** : "Ca rend le chat pro. C'est un must pour les demos."

**Mobile Eng (39) — PWA + responsive** : "manifest.json = installable sur mobile. 3 fixes : sidebar hamburger, input height, pricing overflow."
- **Decision : INTEGRER Sprint 5** ✅ (fixes + manifest)
- Issue : S5-09 + S5-14

### BUSINESS & GROWTH (Integrer Sprint 5)

**Growth (18) — Plausible analytics** : "9€/mois, privacy-first, 30 min de setup. Tracker les visites landing + source."
- **Decision : INTEGRER Sprint 5, Semaine 1** ✅
- Issue : S5-27
- **CEO (01)** : "On ne peut pas lancer sans savoir qui visite."

**Sales (05) — Cold outreach** : "Problem-first emails, 3 lignes max. Cible : Odoo Gold Partners Belgique/France."
- **Decision : INTEGRER Sprint 5** ✅
- Issue : S5-25
- **BizDev (32)** : "J'ai deja 2 calls planifies depuis le repas."

**Content Strat (37) — SEO Odoo** : "Hub & spoke : un pillar page 'Guide Odoo' + 20 articles satellites. Content gap = personne ne couvre les fonctionnalites cachees."
- **Decision : PLANIFIER Sprint 6** — pas de site blog encore
- **Community Mgr (47)** : "On commence par LinkedIn, le blog viendra apres."

**Customer Success (17) — Onboarding** : "TTV (Time To Value) < 5 minutes. Onboarding checklist in-app. Behavior-based emails."
- **Decision : INTEGRER le guide 5 min Sprint 5** ✅ (deja fait), in-app Sprint 6
- **CPO (03)** : "Le guide existe. L'in-app checklist c'est Sprint 6."

### BUSINESS STRATEGY (Planifier)

**CEO (01) — SaaS scaling** : "Design partners (5 beta) avant de scaler. Land & expand. NRR tracking."
- **Decision : APPLIQUER la methode design partners Sprint 5** ✅
- Les 5 beta users = nos design partners

**SaaS Arch (06) — Pricing psychology** : "Feature gates > usage limits. 14-day Pro trial. Anchoring avec le plan Enterprise."
- **Decision : PLANIFIER Sprint 6** — Stripe pas encore integre
- **CFO (15)** : "Le 14-day Pro trial est malin. A faire avec Stripe."

**CPO (03) — Chat UX benchmarks** : "Streaming TTFT < 500ms, artefacts panel, slash commands."
- **Decision : TTFT deja bon** (streaming), slash commands Sprint 7, artefacts Sprint 8

**BizDev (32) — Teaser strategy** : "Email froid + one-pager + call 15 min. 5 integrateurs."
- **Decision : EXECUTER Sprint 5** ✅
- Issue : S5-25

### LEGAL & COMPLIANCE (Planifier)

**AI Safety (33) — EU AI Act** : "Page /about-ai + audit trail des recommandations."
- **Decision : Page /about-ai Sprint 5** ✅, audit trail Sprint 6
- Issue : S5-30

**Legal (16) — LGPL** : "Faible risque. A confirmer avec avocat."
- **Decision : RDV avocat Sprint 5-6** ✅
- **CEO (01)** : "Le fondateur doit prendre le RDV."

### INFRASTRUCTURE (Planifier Sprint 6+)

**Vendor Mgr (40) — OpenAI fallback** : "2 jours de dev grace aux ports. GPT-4o en fallback."
- **Decision : PLANIFIER Sprint 6** — stabiliser Anthropic d'abord

**Brand Designer (42) — SaaS identity** : "Design tokens, blue+violet palette, trust signals."
- **Decision : INTEGRER design tokens Sprint 5** ✅ (avec UX Designer)
- **Brand Designer (42)** : "Je documente les tokens, UX les implemente."

**Support Eng (41) — KB design** : "Tier 1/2/3, format question-reponse, in-app help."
- **Decision : KB faite** ✅, in-app Sprint 6

**CFO (15) — Cost modeling** : "Break-even 21 clients. Routing Haiku/Sonnet = -50% cout."
- **Decision : INTEGRER routing Sprint 5** ✅ (deja planifie S5-03)

---

## SYNTHESE — Integration Sprint 5

### A integrer IMMEDIATEMENT (Jour 1-2)
| # | Learning | Issue Sprint 5 | Responsable |
|---|---------|---------------|-------------|
| 1 | Rate limiting slowapi | S5-02 | DevSecOps (24) |
| 2 | Sentry 3 lignes | S5-10 | SOC (26) |
| 3 | Responsive fixes | S5-09 | Mobile (39) |
| 4 | Plausible analytics | S5-27 | Growth (18) |

### A integrer Semaine 1
| # | Learning | Issue Sprint 5 | Responsable |
|---|---------|---------------|-------------|
| 5 | OpenTelemetry + metriques | S5-11 | Observability (38) |
| 6 | asyncio.gather live_context | Dans S5-03 | AI Eng (09) |
| 7 | Index inverse KG | S5-12 | Data Eng (11) |
| 8 | Copy button + feedback | S5-08 | UX (27) + Frontend (21) |
| 9 | ToolCallCard | S5-13 | Chat Eng (43) |
| 10 | PWA manifest | S5-14 | Mobile (39) |
| 11 | Design tokens doc | Nouveau | Brand (42) + UX (27) |

### A integrer Semaine 2
| # | Learning | Issue Sprint 5 | Responsable |
|---|---------|---------------|-------------|
| 12 | Backup cron 6h | S5-23 | Chaos Eng (31) |
| 13 | Teaser integrateurs | S5-25 | BizDev (32) + Sales (05) |
| 14 | Page /about-ai | S5-30 | AI Safety (33) |

### Reporte Sprint 6+
| # | Learning | Sprint | Raison |
|---|---------|--------|--------|
| 15 | SEO hub & spoke | 6 | Pas de blog |
| 16 | Pricing psychology (trial 14j) | 6 | Stripe pas integre |
| 17 | OpenAI fallback | 6 | Stabiliser Anthropic d'abord |
| 18 | In-app onboarding checklist | 6 | KB faite, in-app plus tard |
| 19 | Slash commands | 7 | Nice to have |
| 20 | Artefacts panel | 8 | Advanced feature |

---

## Score des learnings

| Metrique | Valeur |
|----------|--------|
| Total CRs | 26 |
| Integres Sprint 5 | **14 (54%)** |
| Planifies Sprint 6+ | **6 (23%)** |
| Reference | **6 (23%)** |

**Plus de la moitie des learnings deviennent des actions concretes.** Le programme de formation produit de la valeur reelle.

---

> **Fondateur** : "C'est exactement ce que je voulais. Les gens apprennent, et ce qu'ils apprennent sert au projet. On ne forme pas pour former — on forme pour avancer."
