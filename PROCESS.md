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

**Cascade — dans cet ordre :**

```
1. Tache directe ?     → OUI → travailler dessus
                       → NON ↓
2. Aider un collegue ? → OUI → pair programming, review, support
                       → NON ↓
3. Projet R&D ?        → OUI → avancer le projet (docs/rnd/NN-projet.md)
                       → NON ↓
4. Se former           → Choisir un sujet utile au projet
                         Produire un CR (docs/learning/sprintN/NN-sujet.md)
                         Presenter au partage learning en fin de session
```

**R&D passe AVANT la formation.** Un agent avec un projet R&D actif n'a pas besoin de faire de learning.

**Exemples de projets R&D :** prototyper une feature, tester un outil, benchmarker une technologie, creer un POC.

**Exemples de formation :** etudier un pattern, lire une doc, analyser un concurrent, apprendre un framework.

**Regle** : a la fin de chaque session, l'agent a produit soit du code, soit une review, soit un avancement R&D, soit un CR de formation. JAMAIS rien.

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
