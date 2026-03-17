# OdooAI — Etat du Projet (mis a jour chaque fin de session)

> **Ce fichier est lu EN PREMIER a chaque nouvelle session.**
> Il donne le contexte complet en 2 minutes.

## Derniere mise a jour : 2026-03-22

## Sprint actuel : Sprint 5 — Decollage

## Ou on en est

### Produit
- **Chat web** fonctionnel avec streaming (Next.js + FastAPI)
- **CLI** : odooai analyze, generate-ba, chat, serve
- **Connexion Odoo** : XML-RPC (17/18) + JSON-RPC (19+)
- **9 BA Profiles** : 3 regeneres avec pipeline enrichi, 6 a faire
- **Security Guardian** : classification, anonymisation, domain validation
- **Auth JWT** : signup, login, middleware
- **225 tests**, mypy --strict, ruff, bandit

### Pipeline reverse engineering (PIECE MAITRESSE)
```
Code Odoo → AST (Python parser)
  → KG enrichi (selection constants resolues, action flows)
    → Business Extractor (0 tokens : workflows, relations, Q&A auto)
      → BA Profile (LLM enrichissement final)
        → Chat (buddy mode, data-first)
```

### Vision produit
- OdooAI est un **BUDDY de travail**, pas un consultant
- 4 roles : Reporting, Guide, Explorateur, Challenger
- Reponses directes avec donnees — pas des diagnostics generiques

### Structure
```
odooai/     frontend/     tests/     scripts/     rnd/
docs/ (team, specs, reviews, governance, hr, business, technical,
       meetings, learning, rnd)
```

## Issues Sprint 5 restantes

| Issue | Titre | Bloqueur |
|-------|-------|----------|
| #55 | Playwright E2E | Attend staging |
| #62 | Staging VPS | **Action fondateur** |
| #63-66 | HTTPS, PostgreSQL, CI/CD | Depend VPS |
| #70 | Quality gates CI | Depend E2E |
| #72 | 5 beta users | **Action fondateur** |

## Projets R&D actifs

| Projet | Lead | Status | Dossier |
|--------|------|--------|---------|
| SEO Content Generator | Content Strat (37) | MVP — 5 articles | rnd/seo-content-generator/ |
| OTel Dashboard | Observability (38) | MVP — 11 metriques | rnd/otel-dashboard/ |

## Prochaines priorites

1. **Regenerer les 6 BA restants** avec le pipeline enrichi
2. **Re-analyser les modules cles** (stock, account, hr) avec le nouveau parseur
3. **Iterer sur les reponses** — encore "pas assez precis" selon le fondateur
4. **VPS staging** — action fondateur pour debloquer le deploiement
5. **Les 20 agents en attente** doivent lancer des R&D ou approfondir des learnings

## Regles a ne JAMAIS oublier

1. **Meetings** : session debut + session fin a CHAQUE session
2. **Zero inactivite** : 48 agents, tache/aide/R&D/formation
3. **Learning CRs** : verifier Section 0 AVANT tout
4. **R&D doit produire du code** — pas juste des README
5. **Specs avant code**
6. **OdooAI = buddy** — pas consultant
7. **Subagents** pour paralleliser R&D + learnings + code

## Chiffres

| Metrique | Valeur |
|----------|--------|
| Commits | 130+ |
| Tests | 225 |
| Learning CRs | 61 |
| Specs | 21 |
| Reviews | 14 |
| Agents | 48 |
| R&D projets | 2 actifs |
| KG modules | 1218 |
| BA Profiles | 9 (3 enrichis) |
