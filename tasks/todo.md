# OdooAI — Todo

## Phase 1 — Foundation (Mois 1-3)

### Sprint 1 Semaine 1 (termine — 7/7 pistes)
- [x] ODAI-CORE-001 : Architecture hexagonale
- [x] ODAI-CORE-002 : OdooClient dual-protocole + read_group + name_search
- [x] ODAI-INFRA-001 : CI/CD GitHub Actions
- [x] ODAI-CORE-003 : Config fail-fast + structlog
- [x] ODAI-SEC-001 : Security Guardian + hardening (22 issues, 11 corrigees)
- [x] ODAI-DATA-001 : Knowledge Graphs + Code Analyst (1218 modules, 0 echecs)
- [x] ODAI-API-001 : CLI (odooai analyze, check-kg, serve)
- [x] ODAI-BIZ-001 : Pitch, personas, cost model, LGPL, matrice concurrentielle
- [x] Repo GitHub private + CI/CD operationnel

### Sprint 1 Semaine 2 (24-28 mars 2026)

#### PISTE A — KG Quality + BA Profiles (chemin critique)
- [ ] KG quality check : sale.order vs realite — Odoo Expert (10) — Lun
- [ ] Schema BA Profile (Pydantic) — AI Eng (09) + Prompt Eng (25) — Lun
- [ ] Prompt BA Factory + tests — AI Eng (09) + Prompt Eng (25) — Mar
- [ ] Criteres d'eval BA Profiles — Prompt Eng (25) + Odoo Expert (10) — Mar
- [ ] BA Profile Generator — AI Eng (09) + Backend Arch (08) — Mer
- [ ] Generer BA Profile `sale` — AI Eng (09) — Mer
- [ ] Validation BA Profile par Odoo Expert — Odoo Expert (10) — Jeu
- [ ] Review interne — Security Arch (07) — Ven

#### PISTE B — Orchestrator + Chat CLI
- [ ] Spec ODAI-AGENT-001 Orchestrator — Backend Arch (08) + CTO (02) — Mer
- [ ] Orchestrator implementation — Backend Arch (08) — Jeu
- [ ] Wire Guardian dans pipeline — Backend Arch (08) — Jeu
- [ ] Chat CLI (`odooai chat`) — Senior Dev (19) — Ven
- [ ] **Fondateur teste** — Ven

#### PISTE C — Business (action fondateur)
- [ ] Envoyer 5+ messages LinkedIn PME — Fondateur — Lun-Ven
- [ ] RDV avocat LGPL — Fondateur — Lun
- [ ] README Getting Started — Technical Writer (29) — Mer

#### PISTE D — Qualite
- [ ] Sanitizer strings KG avant prompt — Security Arch (07) — Lun
- [ ] Plan red teaming Sprint 2 — Security Auditor (14) — Ven
- [ ] Instrumenter tokens LLM — AI Eng (09) — Ven

### Stubs actifs (dette technique)

| Stub | Localisation | Remplit par | Deadline |
|------|-------------|------------|----------|
| AnthropicProvider | infrastructure/llm/ | PISTE A (BA Factory) | Semaine 2 |
| Database engine | infrastructure/db/ | Quand necessaire | Sprint 2 |
| RedisClient (vrai Redis) | infrastructure/cache/ | Quand necessaire | Sprint 2 |
| Guardian pas wire | security/guardian.py | PISTE B (Orchestrator) | Semaine 2 |

### VETOs en attente

| Agent | Sujet | Impact | Status |
|-------|-------|--------|--------|
| Legal (16) | LGPL extraction code Odoo | Peut impacter distribution | Fondateur doit consulter avocat |
