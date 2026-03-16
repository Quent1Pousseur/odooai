# Sprint 4 — Execution Tracker
## Owner : PM (04)
## Superviseur : HR Director (44)
## Periode : 20-26 mars 2026
## Mise a jour : chaque daily matin

---

## REGLE : Ce fichier est la SEULE source de verite pour Sprint 4.
## Chaque agent met a jour son status ici. Le PM verifie chaque matin.

---

## Piste A — Stabilisation technique

| # | Tache | Responsable | Deadline | Status | Bloquant ? |
|---|-------|-------------|----------|--------|------------|
| A1 | 5 questions types repondues correctement | Prompt Eng (25) | 22 mars | ⬜ TODO | Oui (demo) |
| A2 | Zero crash sur parcours 10 questions | QA Lead (13) | 23 mars | ⬜ TODO | Oui (demo) |
| A3 | Reponses en < 15 secondes | SRE (23) | 23 mars | ⬜ TODO | Non |
| A4 | Fix domain_validator (edge cases) | Junior Backend (20) | 22 mars | ⬜ TODO | Non |
| A5 | Fix live_context pertinence | AI Eng (09) | 23 mars | ⬜ TODO | Oui (demo) |

## Piste B — Qualite & Securite

| # | Tache | Responsable | Deadline | Status | Bloquant ? |
|---|-------|-------------|----------|--------|------------|
| B1 | 10 tests d'integration minimum | QA Lead (13) | 24 mars | ⬜ TODO | Oui (staging) |
| B2 | Eval framework + 50 questions benchmark | Data Scientist (28) | 24 mars | ⬜ TODO | Non |
| B3 | Audit securite rapport | Security Auditor (14) | 25 mars | ⬜ TODO | Oui (staging) |
| B4 | Comparaison Haiku vs Sonnet (10 BA) | Data Scientist (28) + AI Eng (09) | 24 mars | ⬜ TODO | Non |

## Piste C — Business & Demo

| # | Tache | Responsable | Deadline | Status | Bloquant ? |
|---|-------|-------------|----------|--------|------------|
| C1 | Contact integrateur Bruxelles | BizDev (32) | 20 mars | ⬜ TODO | Oui (demo) |
| C2 | Instance Odoo demo (donnees realistes) | Odoo Expert (10) | 23 mars | ⬜ TODO | Oui (demo) |
| C3 | Run through demo complet | Sales (05) + CPO (03) | 24 mars | ⬜ TODO | Oui (demo) |
| C4 | Go/No-go demo | Prompt Eng (25) | 23 mars | ⬜ TODO | — |
| C5 | Cost forecasting (projection 100-10K users) | CFO (15) + Data Scientist (28) | 25 mars | ⬜ TODO | Non |

## Piste D — Personnes

| # | Tache | Responsable | Deadline | Status | Bloquant ? |
|---|-------|-------------|----------|--------|------------|
| D1 | Mentorat Senior → Junior : premier daily 1:1 | Senior Backend (19) | 20 mars | ⬜ TODO | Non |
| D2 | Mobile : rapport responsive | Mobile Eng (39) | 21 mars | ⬜ TODO | Non |
| D3 | Support : FAQ 20 questions | Support Eng (41) | 22 mars | ⬜ TODO | Non |
| D4 | Knowledge base v1 | Support Eng (41) + Customer Success (17) | 24 mars | ⬜ TODO | Non |
| D5 | Guide utilisateur "5 minutes" | Tech Writer (29) | 25 mars | ⬜ TODO | Non |
| D6 | Rapport competitive intel (prodooctivity) | Competitive Intel (34) | 21 mars | ⬜ TODO | Non |

## Piste E — Infra (preparation Sprint 5)

| # | Tache | Responsable | Deadline | Status | Bloquant ? |
|---|-------|-------------|----------|--------|------------|
| E1 | Dockerfile backend + frontend | DevOps (22) | 25 mars | ⬜ TODO | Non |
| E2 | docker-compose.yml (backend + frontend + db) | DevOps (22) + Infra (12) | 26 mars | ⬜ TODO | Non |
| E3 | Spec migration PostgreSQL | DBA (30) | 25 mars | ⬜ TODO | Non |

---

## CHEMIN CRITIQUE (demo du 24 mars)

```
20 mars : C1 (contact integrateur) ────────────────────────┐
21 mars : D2 (responsive), D6 (competitive intel)          |
22 mars : A1 (5 questions), A4 (domain fix), D3 (FAQ)      |
23 mars : A2 (zero crash), A5 (live_context), C2 (demo db) |
          C4 (go/no-go) ←──────────────────────────────────┤
24 mars : C3 (run through) → DEMO ──────────────────────→ ✅ ou ❌
```

**Si C4 (go/no-go) = NO-GO** → on reporte la demo de 3 jours et on itere.

---

## RITUELS DE SUIVI

| Rituel | Quand | Qui | Quoi |
|--------|-------|-----|------|
| Daily matin | 9h00 | PM + tous les agents actifs | Chaque agent dit : fait / en cours / bloque |
| Check tracker | 9h15 | PM | Met a jour ce fichier |
| Escalade | Immediate | PM → CTO ou CEO | Si un bloquant est rouge depuis > 1 jour |
| Check-in PM | 12h00 | HR Director → PM | "Ca va ? Charge ok ?" (2 min) |
| Point mi-sprint | 22 mars | CEO + CTO + PM | Vue d'ensemble, ajustements |
| Retro fin sprint | 26 mars | Toute l'equipe | Ce qui a marche / pas marche |
| Sondage wellbeing #002 | 26 mars | Wellbeing Officer | Mesurer l'evolution (cible 6.5/10) |

---

## ESCALADE

| Situation | Qui escalade | Vers qui | Delai max |
|-----------|-------------|----------|-----------|
| Tache en retard de 1 jour | PM | Responsable + son lead | 2h |
| Tache bloquante en retard de 2 jours | PM | CTO | Immediat |
| Agent surcharge (signal wellbeing) | Wellbeing Officer | HR Director + PM | 4h |
| VETO securite | Security Arch/Auditor | CTO + Fondateur | Immediat |
| Demo compromise | PM | CEO | Immediat |

---

## LEGENDES STATUS

- ⬜ TODO — pas commence
- 🔵 IN PROGRESS — en cours
- ✅ DONE — termine et verifie
- ❌ BLOCKED — bloque (raison dans la colonne Bloquant)
- 🟡 AT RISK — en retard ou risque de retard

---

> **Prochaine mise a jour** : 20 mars matin (daily)
> **Fondateur** : Vous n'avez qu'a ouvrir CE fichier pour savoir ou en est le sprint.
