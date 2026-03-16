# OdooAI — Todo

## Phase 1 — Foundation (Mois 1-3)

### Sprint 0 : Setup (termine)
- [x] Governance framework (42 agents, workflows, specs)
- [x] Git init + CLAUDE.md projet
- [x] Scaffold technique (pyproject.toml, structure odooai/)
- [x] Kick-off meeting (16 mars 2026)
- [x] ODAI-CORE-001 : Architecture hexagonale (DONE)
- [x] ODAI-CORE-002 : OdooClient dual-protocole (DONE)
- [x] Retro Sprint 0 (DONE)

### Sprint 1 : Infrastructure (17-30 mars 2026)

#### En cours
- [ ] ODAI-INFRA-001 : Pipeline CI/CD GitHub Actions — DevOps (22)
- [ ] ODAI-CORE-003 : Config validation fail-fast + structlog + exceptions — Backend Arch (08)

#### A faire
- [ ] ODAI-SEC-001 : Security Guardian (pipeline complet) — Security Arch (07) + Backend Arch (08)
- [ ] ODAI-DATA-001 : Knowledge Graph format et pipeline — AI Eng (09) + Data Eng (11)

#### Parallele (toute la duree)
- [ ] Board GitHub Projects — PM (04)
- [ ] Modele financier v1 — CFO (15)
- [ ] Matrice concurrentielle — Competitive Intel (34)
- [ ] Liste PME cibles pour interviews — Sales (05)
- [ ] Personas + user stories finalisees — CPO (03)

### Stubs actifs (dette technique a combler)

| Stub | Localisation | Spec qui le remplit | Deadline |
|------|-------------|-------------------|----------|
| AnthropicProvider | infrastructure/llm/anthropic_provider.py | ODAI-AGENT-XXX | Sprint 2 |
| Database engine | infrastructure/db/database.py | ODAI-CORE-003 | Sprint 1 |
| RedisClient (vrai Redis) | infrastructure/cache/redis_client.py | Quand necessaire | Sprint 2 |
| Guardian pipeline complet | security/guardian.py | ODAI-SEC-001 | Sprint 1 |
| Audit persistence | security/audit.py | ODAI-SEC-001 | Sprint 1 |
