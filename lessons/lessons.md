# OdooAI — Lessons Learned (centralise)
## Mis a jour : chaque retro + quand une lecon est apprise
## Source : tasks/lessons.md + retros Sprint 0-5

---

## Format
| ID | Date | Lecon | Impact | Action prise |

---

## Lessons

| ID | Date | Lecon | Impact | Action prise |
|----|------|-------|--------|-------------|
| L01 | 2026-03-16 | Split > Monolithe — max 200 lignes/fichier | Code maintainable | Regle dans CLAUDE.md |
| L02 | 2026-03-16 | Reference ≠ Copie — toujours ameliorer | Qualite code | Review pattern |
| L03 | 2026-03-16 | mypy --strict des le jour 1 | Zero dette typage | CI bloquant |
| L04 | 2026-03-16 | Review AVANT commit, pas apres (SEC-001 : 5 failles) | Securite | Subagent review obligatoire |
| L05 | 2026-03-16 | Agents en veille doivent parler — silence interdit | Qualite decisions | Daily v2 avec challenges |
| L06 | 2026-03-16 | Business en parallele du technique — pas 100% code | Validation marche | Objectifs business chaque sprint |
| L07 | 2026-03-16 | Kick-off obligatoire a chaque sprint | Cadrage equipe | WORKFLOW.md mis a jour |
| L08 | 2026-03-17 | Meetings NON optionnels — rappele 3 fois | Process | Regle intransigeante CLAUDE.md |
| L09 | 2026-03-17 | Specs AVANT code — zero exception (2 violations) | Tracabilite | Reviews dans reviews/, pas subagent |
| L10 | 2026-03-19 | PM en surcharge (9/10) — feature freeze necessaire | Wellbeing | Reset PM + GitHub Issues |
| L11 | 2026-03-19 | Agents sous-utilises = talent gaspille (7 agents a 1-3/10) | Productivite | Assignation + formation obligatoire |
| L12 | 2026-03-19 | Zero inactivite — rappele 5 fois par le fondateur | Process | Regle #1 MANIFESTO + CLAUDE.md |
| L13 | 2026-03-21 | Learnings oublies systematiquement | Formation | Template daily bloquant (ce fix) |
| L14 | 2026-03-21 | KPIs jamais definis — pas de mesure = pas de progres | Performance | hr/kpis-individuels.md (ce fix) |
| L15 | 2026-03-21 | Dossiers gouvernance vides — crees mais pas utilises | Structure | Restructuration (ce fix) |
| L16 | 2026-03-21 | Pivot buddy — on construisait un consultant au lieu d'un collegue | Vision produit | Prompt reecrit, UI refaite |

---

## Patterns recurrents

**Pattern A — Oubli de process** (L08, L12, L13)
Les regles existent mais sont oubliees. Fix : les mettre dans CLAUDE.md (lu a chaque session) ET dans le template daily (verification bloquante).

**Pattern B — Dispersion** (L06, L10, L15)
On avance trop vite sans structure. Fix : feature freeze quand necessaire, weekly recap, budget tracker.

**Pattern C — Silence = danger** (L05, L11)
Les agents qui ne parlent pas cachent des problemes. Fix : challenges obligatoires, zero inactivite, KPIs mesurables.
