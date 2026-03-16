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
- [ ] Connexion Odoo fonctionnelle (v17+ XML-RPC, v19+ JSON-RPC)
- [ ] Knowledge Graphs generes pour 10 modules
- [ ] BA + Expert Profiles valides pour 5 domaines
- [ ] Chat CLI fonctionnel : question business → reponse pertinente
- [ ] CRUD avec double validation et rollback
- [ ] Pipeline de securite complet (anonymisation + audit)

---

## PHASE 2 — LANCEMENT (Mois 4-6)

### Objectif : Premiers clients payants, product-market fit

| Milestone | Contenu | Mois |
|-----------|---------|------|
| **M4 : Interface** | Frontend web (chat UI, dashboard, onboarding), Stripe billing, auth | Mois 4 |
| **M5 : Agents Avances** | Visionary, Feasibility Expert, Support & Debug, Workflow Optimizer | Mois 5 |
| **M6 : Lancement** | Beta privee (10-20 clients), CI/CD, monitoring, documentation, landing page | Mois 6 |

### Criteres de succes Phase 2
- [ ] Interface web fonctionnelle et testee
- [ ] 3 plans d'abonnement actifs sur Stripe
- [ ] 10+ beta testeurs actifs
- [ ] CSAT > 80%
- [ ] Cout moyen par requete < $0.05
- [ ] Zero incident de securite

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
