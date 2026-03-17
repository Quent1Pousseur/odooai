# OdooAI — Registre des Risques

## Responsable : Project Manager (04)
## Revue : Chaque sprint (2 semaines)

## Matrice de Risques

| ID | Risque | Probabilite | Impact | Score | Owner | Mitigation | Status |
|----|--------|-------------|--------|-------|-------|-----------|--------|
| R01 | Anthropic double ses prix LLM | Moyenne (2) | Critique (4) | 8 🟠 | CFO + Vendor Manager | Architecture LLM-agnostic, plan B OpenAI/Mistral | OUVERT |
| R02 | Odoo SA lance son propre assistant IA | Moyenne (2) | Critique (4) | 8 🟠 | Competitive Intel + CEO | Avance technique (Knowledge Graphs), relation ecosystem | OUVERT |
| R03 | Breach de donnees client | Faible (1) | Critique (4) | 4 🟡 | Security Architect + Auditor | 4 couches securite, audit regulier, anonymisation | OUVERT |
| R04 | L'IA donne un mauvais conseil comptable | Moyenne (2) | Haute (3) | 6 🟡 | AI Safety + Legal | Disclaimers, double validation, source citing | OUVERT |
| R05 | Scaling impossible au-dela de 1000 users | Faible (1) | Haute (3) | 3 🟢 | SRE + DBA | Architecture horizontale, load testing, capacity planning | OUVERT |
| R06 | Knowledge Graphs incomplets ou incorrects | Moyenne (2) | Haute (3) | 6 🟡 | Odoo Expert + Data Engineer | Validation humaine, evals automatisees | OUVERT |
| R07 | Churn eleve (> 10% mensuel) | Moyenne (2) | Haute (3) | 6 🟡 | Customer Success + CPO | Health scoring, anti-churn playbook, onboarding < 5 min | OUVERT |
| R08 | Reponses IA trop vagues — pas assez de valeur | Haute (3) | Critique (4) | 12 🔴 | Prompt Eng + AI Eng | Pivot buddy, few-shot, routing Haiku/Sonnet, eval 8+/10 | OUVERT |
| R09 | UI/UX pas assez pro pour convaincre | Haute (3) | Haute (3) | 9 🟠 | UX Designer + Frontend | Refonte UI faite, design tokens, iterer | OUVERT |
| R10 | Pas de staging deploye — tout en localhost | Haute (3) | Haute (3) | 9 🟠 | Infra + DevOps | VPS a commander, Dockerfile pret | OUVERT |
| R11 | 0 beta users — aucune validation terrain | Haute (3) | Critique (4) | 12 🔴 | Sales + Customer Success | Teaser integrateurs, 5 PME ciblees | OUVERT |
| R12 | Process non suivi (learnings oublies 5x) | Moyenne (2) | Haute (3) | 6 🟡 | HR Director + PM | Restructuration gouvernance (ce fix) | OUVERT |
| R13 | Single point of failure Anthropic API | Haute (3) | Haute (3) | 9 🟠 | Vendor Mgr + AI Eng | Fallback OpenAI prevu Sprint 6, retry deja en place | OUVERT |

## Scoring

```
Probabilite : Faible (1) | Moyenne (2) | Haute (3)
Impact :      Faible (1) | Moyen (2) | Haut (3) | Critique (4)

Score = Probabilite x Impact
  1-3  : 🟢 Acceptable
  4-6  : 🟡 A surveiller
  7-9  : 🟠 Plan de mitigation obligatoire
  10-12: 🔴 Action immediate requise
```

## Process

1. **N'importe qui** peut ajouter un risque a ce registre
2. Le **PM** assigne un owner et demande une mitigation
3. Le risque est **revu chaque sprint** — est-il toujours d'actualite ? La mitigation fonctionne ?
4. Un risque qui se materialise → devient un **incident** (voir `incidents/`)
5. Un risque resolu → Status passe a FERME avec date et raison
