# OdooAI — Templates de Fichiers

Chaque fichier cree DOIT suivre le template de son type.
Pas de derogation. Si le template ne convient pas, on le met a jour — on ne l'ignore pas.

---

## 1. Spec technique

**Chemin** : `docs/specs/ODAI-XXX-NNN-nom.md`

```markdown
# ODAI-[DOMAIN]-[NNN] — [Titre]

## Status
DRAFT | IN PROGRESS | DONE

## Auteur
[Agent(s) responsable(s)]

## Reviewers
[Agent(s) qui review]

## Date
YYYY-MM-DD

## Contexte
[Pourquoi cette spec ? Quel probleme resout-elle ?]

## Objectif
[Ce qu'on construit — clair et concis]

## Definition of Done
- [ ] [Critere 1]
- [ ] [Critere 2]
- [ ] [Tests passent]
- [ ] [Review dans docs/reviews/]

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| [path] | Creer / Modifier |

## Estimation
S (< 1 jour) | M (1-3 jours) | L (3+ jours)
```

---

## 2. Review

**Chemin** : `docs/reviews/ODAI-XXX-NNN-review.md`

```markdown
# Review — ODAI-[XXX]-[NNN] [Titre]

## Reviewer : [Agent(s)]
## Date : YYYY-MM-DD
## Status : APPROVED | CHANGES REQUESTED | VETO

## Points positifs
- [Ce qui est bien]

## Points d'attention
- [Ce qui pourrait etre ameliore]

## Decision
[Approuve / Changements demandes / VETO avec raison]
```

---

## 3. Session (ex-daily)

**Chemin** : `docs/meetings/sessions/YYYY-MM-DD-session-N.md`

```markdown
# Session — YYYY-MM-DD (Session N)

## SECTION 0 — Verification CRs / R&D
| Agent | Activite hier | Livrable depose ? | Fichier |
|-------|--------------|-------------------|---------|
| [agents en formation/R&D hier] | learning/R&D | oui/non | docs/learning/ ou docs/rnd/ |

## SECTION 1 — Zero Inactivite
| # | Agent | Activite | Type |
|---|-------|----------|------|
| 01-48 | ... | ... | tache / aide / R&D / formation |

## SECTION 2 — Agents sans tache — Attribution R&D / Learning
**Chaque agent sans tache le dit et choisit MAINTENANT :**

| Agent | Choix | Projet/Sujet | Equipe |
|-------|-------|-------------|--------|
| [agent] | R&D / Learning | [nom] | [solo ou avec qui] |

**Nouveaux projets R&D proposes :**
| Projet | Pitch (2 min) | Lead | Equipe | Validation CTO |
|--------|--------------|------|--------|----------------|

## SECTION 3 — Bloquants
[Ce qui bloque]

## SECTION 3 — Challenges inter-agents
[Les agents se challengent]

## SECTION 4 — Decisions
[Decisions prises]
```

---

## 4. Session fin (rapport d'activite)

**Chemin** : `docs/meetings/sessions/YYYY-MM-DD-session-N-eod.md`

```markdown
# Session EOD — YYYY-MM-DD (Session N)

## RAPPORT D'ACTIVITE
| # | Agent | Realise | Livrable |
|---|-------|---------|----------|
| 01-48 | ... | ... | fichier ou "en cours" |

## PARTAGE LEARNING
[Les agents en formation presentent]

## Metriques
| Metrique | Valeur |
|----------|--------|
| Issues fermees | X/Y |
| Tests | X |
| Learning CRs | X |
| Wellbeing | X/10 |
```

---

## 5. Retro sprint

**Chemin** : `docs/meetings/retros/YYYY-MM-DD-sprint-N.md`

```markdown
# Retrospective Sprint N

## Date : YYYY-MM-DD
## Participants : 48 agents + Fondateur

## Metriques Sprint
| Metrique | Objectif | Resultat |
|----------|---------|---------|

## Ce qui a BIEN fonctionne
[Avec preuves]

## Ce qui a MOINS BIEN fonctionne
[Avec actions correctives]

## Challenges des agents
[Les agents remontent des problemes]

## Lessons learned
[Ajoutees dans docs/governance/lessons.md]

## KPIs par agent (top/bottom)
[Top 3 + Bottom 3 avec actions]

## Score global : X/10
```

---

## 6. Kick-off sprint

**Chemin** : `docs/meetings/kickoffs/YYYY-MM-DD-sprint-N.md`

```markdown
# Kick-Off Sprint N

## Date : YYYY-MM-DD
## Objectifs Sprint

## SECTION 1 — Zero Inactivite (48 agents)
| # | Agent | Tache Sprint N | Type |
|---|-------|----------------|------|

## SECTION 2 — Issues
| Prio | Issue | Titre | Responsable | Deadline |
|------|-------|-------|-------------|----------|

## SECTION 3 — Challenges
[Les agents challengent le plan]

## Milestones
| Date | Milestone | Go/No-Go |
|------|-----------|----------|

## Metriques cibles
| Metrique | Sprint N-1 | Cible Sprint N |
|----------|-----------|----------------|
```

---

## 7. Learning CR

**Chemin** : `docs/learning/sprintN/NN-sujet.md`

```markdown
# Learning — [Agent Name] ([NN]) — [Sujet]
## Date : YYYY-MM-DD (Sprint N)
## Duree : X heures

## Ce que j'ai appris
- [Point 1]
- [Point 2]
- [Point 3]

## Comment ca s'applique a OdooAI
- [Application 1]
- [Application 2]

## Ce que je recommande
- [Recommandation 1 — Sprint X]
- [Recommandation 2 — Sprint X]

## Sources
- [Source 1]
- [Source 2]
```

---

## 8. Projet R&D

**Chemin** : `docs/rnd/NN-nom-projet.md`

```markdown
# R&D — [Agent Name] ([NN]) — [Nom du projet]
## Date debut : YYYY-MM-DD
## Status : En cours | Pause | Termine | Propose en spec

## Objectif
[1-2 phrases]

## Plan
1. [Etape 1]
2. [Etape 2]
3. [Etape 3]

## Avancement
### Session X (YYYY-MM-DD)
- Ce que j'ai fait
- Ce que j'ai decouvert
- Prochaine etape

## Resultat
[Quand termine — demo/prototype/doc]
```

---

> **Regle** : si un fichier ne suit pas son template, la review le rejette.
