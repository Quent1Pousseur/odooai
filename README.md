# OdooAI

> AI-powered Business Analyst that has read every line of Odoo's source code.
> Replaces expensive consultants for SMBs worldwide.

## Quick Navigation

### Pour comprendre le projet
| Document | Contenu |
|----------|---------|
| **[PROJECT.md](PROJECT.md)** | **⭐ BIBLE DU PROJET — Lire en premier. Probleme, solution, architecture, securite, stack, business model** |
| [MANIFESTO.md](MANIFESTO.md) | Culture, valeurs, obligation de challenge |
| [GLOSSARY.md](GLOSSARY.md) | Definitions des termes utilises dans le projet |
| [roadmap/ROADMAP.md](roadmap/ROADMAP.md) | Vision timeline et phases |

### Pour travailler
| Document | Contenu |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Standards de code, conventions, lint |
| [WORKFLOW.md](WORKFLOW.md) | Specs, Git, PRs, reviews, tracking |
| [ONBOARDING.md](ONBOARDING.md) | Checklist d'onboarding pour un nouvel agent |

### Pour suivre le projet
| Document | Contenu |
|----------|---------|
| [agents/TEAM.md](agents/TEAM.md) | Equipe (42 agents), roles, matrices |
| [meetings/DAILY_STANDUP.md](meetings/DAILY_STANDUP.md) | Process du daily standup |
| [OKRs.md](OKRs.md) | Objectifs trimestriels mesurables |
| [ESCALATION.md](ESCALATION.md) | Qui appeler quand ca va mal |

### Historique et tracabilite
| Repertoire | Contenu |
|------------|---------|
| [specs/](specs/) | Toutes les specs (ODAI-XXX) |
| [decisions/](decisions/) | Architecture Decision Records (ADR) |
| [meetings/daily/](meetings/daily/) | Comptes rendus des standups |
| [meetings/weekly/](meetings/weekly/) | Recaps hebdomadaires |
| [meetings/retro/](meetings/retro/) | Retrospectives de sprint |
| [risks/](risks/) | Registre des risques |
| [incidents/](incidents/) | Post-mortems des incidents |
| [lessons/](lessons/) | Lecons apprises |
| [budget/](budget/) | Suivi budgetaire et couts |

## Structure du Repo

```
mcp/
  README.md               ← Tu es ici
  MANIFESTO.md            ← Culture et valeurs
  CONTRIBUTING.md         ← Standards de code
  WORKFLOW.md             ← Process de developpement
  ONBOARDING.md           ← Checklist nouvel agent
  GLOSSARY.md             ← Definitions
  OKRs.md                 ← Objectifs trimestriels
  ESCALATION.md           ← Matrice d'escalade

  agents/
    TEAM.md               ← Equipe complete (42 agents)
    prompts/              ← Profils detailles de chaque agent

  specs/                  ← Specifications (ODAI-XXX-description.md)
  decisions/              ← Architecture Decision Records (ADR-XXX.md)
  roadmap/                ← Vision et timeline
  risks/                  ← Registre des risques
  incidents/              ← Post-mortems
  lessons/                ← Lecons apprises
  budget/                 ← Suivi budgetaire

  meetings/
    DAILY_STANDUP.md      ← Process du daily
    daily/                ← Un fichier par jour
    weekly/               ← Recaps hebdomadaires
    retro/                ← Retrospectives de sprint

  odooai/                 ← Code source (quand on commence a coder)
  tests/                  ← Tests
```
