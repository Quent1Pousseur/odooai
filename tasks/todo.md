# OdooAI — Todo

## Phase 1 — Foundation (Mois 1-3)

### Sprint 0 : Setup (termine)
- [x] Governance framework (42 agents, workflows, specs)
- [x] ODAI-CORE-001 : Architecture hexagonale (DONE)
- [x] ODAI-CORE-002 : OdooClient dual-protocole (DONE)
- [x] ODAI-INFRA-001 : CI/CD GitHub Actions (DONE)
- [x] ODAI-CORE-003 : Config fail-fast + structlog (DONE)
- [x] ODAI-SEC-001 : Security Guardian + hardening (DONE)
- [x] Kick-off + daily + retro (DONE)

### Sprint 1 : Infrastructure + Business (17-30 mars 2026)

> 7 pistes paralleles. Chaque agent a un livrable.

#### PISTE 1 — DATA-001 : Knowledge Graphs (chemin critique technique)
- [ ] Schemas Pydantic KG — AI Eng (09) + Data Eng (11) — Lun 17
- [ ] Validation schemas — Odoo Expert (10) — Lun 17
- [ ] manifest_parser.py — Backend Arch (08) — Mar 18
- [ ] Fixtures test (vrais modules) — QA Lead (13) + Odoo Expert (10) — Mar 18
- [ ] python_parser.py (AST) — Backend Arch (08) — Mer 19
- [ ] xml_parser.py — Backend Arch (08) — Jeu 20
- [ ] analyzer.py + storage.py + tests — Backend Arch (08) + QA (13) — Ven 21
- [ ] Review interne DATA-001 — Security Arch (07) + Odoo Expert (10) — Ven 21

#### PISTE 2 — CORE-002 update
- [ ] Ajouter read_group + name_search — Backend Arch (08) — Lun 17
- [ ] Review independante — Senior Dev (19) — Lun 17

#### PISTE 3 — Infra
- [ ] Repo GitHub private + premier push — DevOps (22) — Lun 17
- [ ] CI/CD passe sur GitHub — DevOps (22) — Mar 18

#### PISTE 4 — Validation marche
- [ ] Pitch 10 mots — Sales (05) + CEO (01) — Lun 17
- [ ] 3 personas finalisees — CPO (03) — Lun 17
- [ ] Mockup chat Figma — UX Designer (27) — Mar 18
- [ ] 10 PME cibles identifiees — Sales (05) + BizDev (32) — Mar 18
- [ ] One-pager OdooAI — Brand Designer (42) — Mer 19
- [ ] Script interview — CPO (03) + Customer Success (17) — Mer 19
- [ ] Premiers contacts PME (3-5) — Sales (05) — Jeu 20-Ven 21

#### PISTE 5 — Finance & Legal
- [ ] Estimations tokens par requete — AI Eng (09) — Lun 17
- [ ] Modele de cout LLM v1 — CFO (15) — Mar 18
- [ ] Question juridique LGPL — Legal (16) — Mer 19
- [ ] Disclaimer systeme AI — AI Safety (33) + Legal (16) — Mer 19

#### PISTE 6 — Strategie
- [ ] Matrice concurrentielle — Competitive Intel (34) — Ven 21
- [ ] Definir aha moment — SaaS Arch (06) + CPO (03) — Mer 19
- [ ] SLOs cibles — SRE (23) — Ven 21

#### PISTE 7 — Qualite
- [ ] Review CORE-001 + CORE-002 — Security Arch (07) — Lun 17
- [ ] Criteres eval BA Profiles — Prompt Eng (25) + Odoo Expert (10) — Ven 21
- [ ] Plan red teaming Sprint 2 — Security Auditor (14) — Ven 21

### Stubs actifs (dette technique)

| Stub | Localisation | Remplit par | Deadline |
|------|-------------|------------|----------|
| AnthropicProvider | infrastructure/llm/ | ODAI-AGENT-XXX | Sprint 2 |
| Database engine | infrastructure/db/ | Quand necessaire | Sprint 2 |
| RedisClient (vrai Redis) | infrastructure/cache/ | Quand necessaire | Sprint 2 |
| Guardian pas wire | security/guardian.py | ODAI-AGENT-XXX (Orchestrator) | Sprint 2 |

### VETOs en attente

| Agent | Sujet | Impact | Status |
|-------|-------|--------|--------|
| Legal (16) | LGPL extraction code Odoo | Peut impacter distribution | En cours |
| Odoo Expert (10) | _inherits + related dans KG | KG incomplet si absent | A integrer DATA-001 |
