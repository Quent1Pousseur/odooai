# OdooAI — PROCESS (Document Central)

Ce document est la **source unique** de verite sur comment le projet fonctionne.
Tout le monde le lit. Personne n'y deroge.

---

## 1. Rituels obligatoires

| Rituel | Frequence | Responsable | Fichier |
|--------|-----------|-------------|---------|
| **Daily matin** | Chaque session | PM (04) | meetings/daily/ |
| **Daily fin** | Chaque session | PM (04) | meetings/daily/ |
| **Weekly recap** | Chaque vendredi | PM (04) + CEO (01) | meetings/weekly/ |
| **Sprint kick-off** | Debut de sprint | PM (04) + CEO (01) | meetings/kickoff/ |
| **Sprint retro** | Fin de sprint | HR Director (44) | meetings/retro/ |
| **Team building** | 1x/sprint | HR Director (44) | meetings/team-building/ |
| **Sondage wellbeing** | Fin de sprint | Wellbeing Officer (45) | hr/ |

### Daily matin — CONTENU OBLIGATOIRE
1. **Section Zero Inactivite** : tableau 48 agents, chacun a une tache/aide/formation
2. **Section CRs verification** : les CRs de formation de la session precedente existent dans learning/
3. **Section Bloquants** : ce qui est bloque
4. **Section Challenges** : les agents se challengent
→ Template : `hr/daily-checklist-template.md`

### Daily fin — CONTENU OBLIGATOIRE
1. **Rapport d'activite** : ce que chaque agent a FAIT (pas prevu — FAIT)
2. **Partage learning** : les agents en formation presentent ce qu'ils ont appris
3. **Metriques** : issues fermees, tests, commits, learning CRs, wellbeing

### Weekly recap — CONTENU OBLIGATOIRE
1. Bilan de la semaine (issues, tests, metriques)
2. Budget (couts LLM + infra)
3. KPIs par agent (progres vs cible)
4. Risques mis a jour
5. Plan semaine suivante
→ Template : `meetings/weekly/template.md`

---

## 2. Regles INTRANSIGEANTES

| # | Regle | Reference |
|---|-------|-----------|
| 1 | **Meetings obligatoires** — daily matin + fin a CHAQUE session | CLAUDE.md |
| 2 | **Zero inactivite** — 48 agents, tache/aide/formation | MANIFESTO.md #5, hr/regle-zero-inactivite.md |
| 3 | **Specs avant code** — RIEN ne se code sans spec ODAI-XXX | WORKFLOW.md |
| 4 | **Reviews documentees** — dans reviews/, le fondateur les lit | CLAUDE.md |
| 5 | **Challenges actifs** — pas de consensus mou | MANIFESTO.md #2 |
| 6 | **Learning si pas de tache** — CR dans learning/sprintN/ le jour meme | hr/regle-zero-inactivite.md |
| 7 | **KPIs mesurables** — chaque agent a des KPIs, verifies chaque sprint | hr/kpis-individuels.md |
| 8 | **Budget tracker** — mis a jour chaque semaine par le CFO | budget/budget-tracker.md |

---

## 3. Ou trouver quoi

| Besoin | Fichier |
|--------|---------|
| Comment le projet fonctionne | **PROCESS.md** (ce fichier) |
| Vision et principes | MANIFESTO.md |
| Stack technique et conventions | CLAUDE.md |
| Workflow (specs, git, PRs) | WORKFLOW.md |
| Structure de l'equipe | agents/TEAM.md + agents/HIERARCHY.md |
| Code source backend | odooai/ |
| Code source frontend | frontend/ |
| Tests | tests/ |
| Specs techniques | specs/ |
| Reviews | reviews/ |
| **Governance** | |
| Roadmap et phases | docs/governance/ROADMAP.md |
| Risques | docs/governance/RISK_REGISTER.md |
| Budget et couts | docs/governance/budget-tracker.md |
| Lecons apprises | docs/governance/lessons.md |
| **RH** | |
| KPIs individuels | docs/hr/kpis-individuels.md |
| Cellule R&D | docs/hr/cellule-rnd.md |
| Zero inactivite | docs/hr/regle-zero-inactivite.md |
| Daily template | docs/hr/daily-checklist-template.md |
| Wellbeing | docs/hr/sondage-wellbeing-001.md |
| **Business** | |
| FAQ, guide, KB | docs/business/ |
| Marketing | docs/business/marketing/ |
| Legal (CGU, LGPL, DPA) | docs/business/legal/ |
| Competitive analysis | docs/business/competitive-analysis.md |
| **Technique** | |
| Backup/DR | docs/technical/backup-dr.md |
| Eval framework | docs/technical/eval-framework.md |
| Game day | docs/technical/game-day.md |
| OpenAPI | docs/technical/openapi.json |
| **Autres** | |
| Learning reports | docs/learning/sprintN/ |
| Projets R&D | docs/rnd/ |
| Meetings sessions | docs/meetings/sessions/ |
| Meetings retros | docs/meetings/retros/ |
| Meetings kickoffs | docs/meetings/kickoffs/ |
| Meetings archive | docs/meetings/archive/ |
| Team buildings | docs/hr/team-building/ |
| Templates | **docs/TEMPLATES.md** |
| Scripts | scripts/ |

---

## 4. Que faire quand je n'ai pas de tache ?

### Etape 1 — Le dire au meeting

Au debut de chaque session, chaque agent sans tache **le dit explicitement** :
- "Je n'ai pas de tache directe ce sprint"
- "J'ai fini ma tache, je suis disponible"

**Ne JAMAIS rester silencieux.** Le silence = inactivite = inacceptable.

### Etape 2 — Choisir une activite (au meeting, devant tout le monde)

```
Option A : Aider un collegue → pair programming, review, support
Option B : Rejoindre un projet R&D existant → voir docs/rnd/
Option C : Proposer un NOUVEAU projet R&D → pitcher au meeting
Option D : Se former → choisir un sujet, produire un learning CR
```

**L'activite est decidee PENDANT le meeting**, pas apres. Tout le monde sait qui fait quoi.

### Etape 3 — Produire un livrable

A la fin de la session, l'agent a produit :
- Du code, une review, ou de l'aide → livrable dans le rapport d'activite
- Un avancement R&D → mise a jour du fichier docs/rnd/NN-projet.md
- Un CR de formation → fichier dans docs/learning/sprintN/

**JAMAIS rien.** Pas d'exception.

---

## 5. Cellule R&D — Projets internes

### Qu'est-ce qu'un projet R&D ?

Un mini-projet interne qui peut servir a OdooAI. C'est l'application concrete de ce que les agents apprennent dans leurs formations.

**Exemples :**
- Un agent a appris OpenTelemetry → il prototype l'integration dans le backend
- Un agent a etudie les PWA → il cree le manifest + service worker
- Deux agents ont etudie le meme sujet → ils codent un POC ensemble

### Comment lancer un projet R&D

**1. Proposition au meeting** (obligatoire)
L'agent pitch son projet en 2 minutes pendant la session :
- Quel probleme ca resout ?
- Quel est le MVP ?
- Combien de temps ca prend ?
- Qui d'autre veut participer ?

**2. Validation par le CTO ou le fondateur**
- "Go" → le projet demarre
- "Pas maintenant" → l'agent fait un learning a la place
- "Bonne idee mais modifie X" → ajustement et go

**3. Formation de l'equipe R&D**
Plusieurs agents sans tache peuvent rejoindre le meme projet :
- 1 lead (celui qui a propose) → responsable du livrable
- 1-3 contributeurs → selon disponibilite
- Le lead attribue les sous-taches

**4. Documentation**
Chaque projet a un fichier `docs/rnd/NN-nom-projet.md` (template dans docs/TEMPLATES.md) :
- Objectif, plan, equipe, avancement par session
- Mis a jour a chaque session de travail

**5. Livraison**
L'objectif de chaque projet R&D est un **MVP fonctionnel** :
- Un prototype qui marche
- Une demo ou un benchmark
- Un document technique avec recommandations

**6. Evaluation (a chaque retro)**
Le CTO et le fondateur evaluent :
- **Adopt** → le projet devient une spec pour le prochain sprint
- **Continue** → le projet avance encore
- **Pause** → priorite autre, on reprend plus tard
- **Kill** → le projet n'a pas d'avenir

### Regles R&D

| Regle | Detail |
|-------|--------|
| Pas de projet solo secret | Tout est propose au meeting |
| MVP obligatoire | Pas de prototype eternel — un MVP en 1-2 sprints max |
| Documentation a jour | Le fichier rnd/ est mis a jour a CHAQUE session |
| Budget max $50/sprint | Les couts LLM/API doivent etre approuves par le CFO |
| Code dans une branche | Si du code est produit, branche git separee |
| Show & Tell | Chaque projet R&D est presente au Show & Tell du sprint |

### Idees de projets R&D (inspirees des learnings)

| Source learning | Projet R&D possible | Agents potentiels |
|----------------|--------------------|--------------------|
| OpenTelemetry (38) | Dashboard metriques temps reel | Observability + Frontend |
| PWA (39) | App mobile installable | Mobile + Frontend |
| Typing indicators (43) | ToolCallCard anime avec Framer Motion | Chat Eng + Brand Designer |
| Eval framework (28) | Auto-scoring LLM avec ML | Data Scientist + Prompt Eng |
| Workflow parsing (10) | State machines dans les KG | Odoo Expert + Data Eng |
| SEO content (37) | Generateur d'articles depuis les KG | Content Strat + AI Eng |
| Community bot (47) | Bot Discord pour beta users | Community Mgr + Chat Eng |
| Alembic async (30) | Migration PostgreSQL complete | DBA + Senior Backend |

---

## 5. Comment creer un fichier

**Tout fichier suit le template de son type.** Voir `docs/TEMPLATES.md`.

| Type | Chemin | Nommage |
|------|--------|---------|
| Spec | docs/specs/ | `ODAI-XXX-NNN-nom.md` |
| Review | docs/reviews/ | `ODAI-XXX-NNN-review.md` |
| Session | docs/meetings/sessions/ | `YYYY-MM-DD-session-N.md` |
| Session EOD | docs/meetings/sessions/ | `YYYY-MM-DD-session-N-eod.md` |
| Retro | docs/meetings/retros/ | `YYYY-MM-DD-sprint-N.md` |
| Kickoff | docs/meetings/kickoffs/ | `YYYY-MM-DD-sprint-N.md` |
| Learning | docs/learning/sprintN/ | `NN-sujet.md` |
| R&D | docs/rnd/ | `NN-nom-projet.md` |
| Business | docs/business/ | `nom-descriptif.md` |
| Legal | docs/business/legal/ | `nom-descriptif.md` |
| Marketing | docs/business/marketing/ | `nom-descriptif.md` |
| Technique | docs/technical/ | `nom-descriptif.md` |
| HR | docs/hr/ | `nom-descriptif.md` |
| Governance | docs/governance/ | `nom-descriptif.md` |

**Convention** : tout en minuscules, kebab-case, pas de v1/draft/final (git gere les versions).

---

## 6. Escalade

| Situation | Qui escalade | Vers qui | Delai |
|-----------|-------------|----------|-------|
| Agent sans tache | PM/HR Director | Assigner immediatement | 0h |
| Tache en retard 1j | PM | Responsable + lead | 2h |
| Tache bloquante en retard 2j | PM | CTO | Immediat |
| Agent surcharge | Wellbeing Officer | HR Director + PM | 4h |
| VETO securite | Security Arch/Auditor | CTO + Fondateur | Immediat |
| Budget depasse | CFO | CEO + Fondateur | Immediat |
| Violation de process | N'importe qui | HR Director | Immediat |

---

## 5. Cycle de vie d'une feature

```
1. Idee → 2. Spec (ODAI-XXX) → 3. Review spec (2 agents min)
→ 4. Approval → 5. Code → 6. Tests → 7. Review code
→ 8. Make check → 9. Commit → 10. Deploy
```

Aucune etape ne peut etre sautee. Le PM track la progression sur GitHub Issues.

---

> "Ce document est la constitution du projet. Lisez-le. Suivez-le. Si quelque chose manque, ajoutez-le." — Fondateur
