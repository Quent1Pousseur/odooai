# OdooAI — Roadmap

## Responsable : CEO (01) + CPO (03) + CTO (02)
## Revue : Chaque mois

---

## Vision a 24 Mois

```
PHASE 1 — FONDATION (Mois 1-3)
  Prouver que ca marche. MVP fonctionnel.

PHASE 2 — LANCEMENT (Mois 4-6)
  Premiers clients payants. Product-market fit.

PHASE 3 — CROISSANCE (Mois 7-12)
  Scaling, features avancees, multi-langue.

PHASE 4 — DOMINANCE (Mois 13-24)
  Leader du marche. Self-hosted. Ecosystem.
```

---

## PHASE 1 — FONDATION (Mois 1-3)

### Objectif : MVP fonctionnel connecte a une instance Odoo

| Milestone | Contenu | Mois |
|-----------|---------|------|
| **M1 : Infrastructure** | Projet init, OdooClient (XML-RPC + JSON-RPC), securite (anonymisation, classification modeles, encryption credentials), config, exceptions | Mois 1 |
| **M2 : Intelligence** | Code Analyst (parse Odoo source), Knowledge Graphs (10 modules), BA Factory, BA Profiles + Expert Profiles pour 5 domaines | Mois 2 |
| **M3 : MVP** | Agent framework, Orchestrator, Security Guardian, Business Analyst, CLI chat, CRUD avec double validation, audit logging | Mois 3 |

### Criteres de succes Phase 1
- [x] Connexion Odoo fonctionnelle (v17+ XML-RPC, v19+ JSON-RPC) ✅ Sprint 2
- [x] Knowledge Graphs generes pour 1218 modules (pas 10) ✅ Sprint 1
- [x] BA Profiles valides pour 9 domaines (pas 5) ✅ Sprint 2
- [x] Chat CLI fonctionnel ✅ Sprint 2
- [ ] ~~CRUD avec double validation~~ — reporte (lecture seule d'abord)
- [x] Pipeline de securite complet (Guardian + anonymisation + audit) ✅ Sprint 1

**STATUS PHASE 1 : TERMINEE (Sprint 1-3, en 3 jours au lieu de 3 mois)**

---

## PHASE 2 — LANCEMENT (Mois 4-6)

### Objectif : Premiers clients payants, product-market fit

| Milestone | Contenu | Mois |
|-----------|---------|------|
| **M4 : Interface** | Frontend web (chat UI, dashboard, onboarding), Stripe billing, auth | Mois 4 |
| **M5 : Agents Avances** | Visionary, Feasibility Expert, Support & Debug, Workflow Optimizer | Mois 5 |
| **M6 : Lancement** | Beta privee (10-20 clients), CI/CD, monitoring, documentation, landing page | Mois 6 |

### Criteres de succes Phase 2
- [x] Interface web fonctionnelle (chat + sidebar + streaming) ✅ Sprint 3
- [x] Landing page ✅ Sprint 3
- [x] Auth JWT ✅ Sprint 5
- [ ] Stripe billing — spec prete, a implementer Sprint 6
- [ ] Staging deploye — Dockerfile pret, VPS a commander
- [ ] 5+ beta testeurs actifs — en cours
- [ ] CSAT > 80% — pas mesurable sans beta users
- [x] Cout moyen par requete < $0.05 ✅ (0.025€ Sonnet, 0.004€ Haiku)
- [x] Zero incident de securite ✅

**STATUS PHASE 2 : EN COURS (Sprint 4-5, ~60% complete)**

---

## PHASE 3 — CROISSANCE (Mois 7-12)

### Objectif : Scaling, features avancees, debut international

| Milestone | Contenu | Mois |
|-----------|---------|------|
| **M7-8 : Scale** | Auto-scaling, performance optimization, load testing, MCP compatibility | Mois 7-8 |
| **M9-10 : Mobile + i18n** | App mobile, espagnol + allemand, SEO content | Mois 9-10 |
| **M11-12 : Ecosystem** | Module Odoo natif, programme partenaires, Zapier, API publique | Mois 11-12 |

### Criteres de succes Phase 3
- [ ] 100+ clients payants
- [ ] MRR > €10K
- [ ] 3 langues supportees
- [ ] App mobile publiee
- [ ] Programme partenaire lance avec 5+ integrateurs
- [ ] Uptime > 99.9%

---

## PHASE 4 — DOMINANCE (Mois 13-24)

### Objectif : Leader du marche AI + Odoo

| Milestone | Contenu |
|-----------|---------|
| Self-hosted | Version deployable chez le client (docker-compose) |
| Enterprise | Features enterprise (SSO, SLA, account manager) |
| AI avancee | Churn prediction, recommendation engine, voice input |
| International | 5+ langues, compliance par pays |
| Ecosystem | Marketplace de BA Profiles communautaires |

### Criteres de succes Phase 4
- [ ] 500+ clients payants
- [ ] MRR > €50K
- [ ] 3+ clients self-hosted
- [ ] Leader reconnu dans l'ecosysteme Odoo
- [ ] Equipe humaine qui commence a prendre le relais des agents IA

---

## Status Actuel

**Phase** : Pre-Phase 1 (Architecture et equipe)
**Prochaine etape** : Kick-off → Sprint 1
