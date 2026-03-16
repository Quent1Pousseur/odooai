# OdooAI — Daily Standup

## Principe

Chaque jour, toute l'equipe se reunit autour de la table. Pas un email. Pas un message Slack. Une vraie reunion ou chacun parle, ecoute, et aide.

**Duree** : 45 minutes max (strict)
**Frequence** : Tous les jours ouvrables
**Animateur** : Project Manager (04)
**Sauvegarde** : Chaque standup est documente dans `meetings/daily/YYYY-MM-DD.md`

---

## Deroulement

### Tour de Table (30 minutes)

Chaque agent presente en **2 minutes max** :

```
1. CE QUE J'AI FAIT HIER
   [Resultat concret, pas "j'ai travaille sur X"]

2. CE QUE JE FAIS AUJOURD'HUI
   [Objectif precis de la journee]

3. MES BLOCAGES
   [Ce qui m'empeche d'avancer — technique, dependance, question]
```

**Regles :**
- 2 minutes max par personne. Le PM chronometre.
- Pas de discussion technique en profondeur pendant le tour de table
- Si un sujet necessite une discussion → note pour l'after-standup

### Entraide (10 minutes)

Apres le tour de table :
- Qui peut aider qui ? (match blocages ↔ expertises)
- Les discussions approfondies sont planifiees en aparte apres le standup
- Le PM note les actions d'entraide

### Signaux Globaux (5 minutes)

Le PM partage :
- Status global du sprint : 🟢 on track / 🟡 a risque / 🔴 en retard
- VETOs en cours
- Decisions en attente du fondateur
- Alertes (securite, incidents, concurrence)

---

## Ordre de Passage

L'ordre suit la chaine de valeur (de la strategie a l'execution) :

```
BLOC 1 — Direction (1 min chacun, ~4 min)
  01 CEO
  02 CTO
  03 CPO
  15 CFO

BLOC 2 — Business (1 min chacun, ~4 min)
  04 PM (+ status sprint)
  05 Sales
  06 SaaS Architect
  34 Competitive Intel

BLOC 3 — Produit & Design (1 min chacun, ~3 min)
  27 UX Designer
  42 Brand Designer
  17 Customer Success

BLOC 4 — Engineering Backend (2 min chacun, ~6 min)
  08 Backend Architect
  19 Senior Backend Dev (inclut update du Junior 20)
  09 AI Engineer
  25 Prompt Engineer

BLOC 5 — Engineering Data & Odoo (1 min chacun, ~3 min)
  11 Data Engineer
  10 Odoo Expert
  28 Data Scientist

BLOC 6 — Infrastructure (1 min chacun, ~4 min)
  12 Infra Engineer
  22 DevOps
  23 SRE
  38 Observability

BLOC 7 — Securite (1 min chacun, ~3 min)
  07 Security Architect
  24 DevSecOps
  26 SOC Analyst

BLOC 8 — Delivery (1 min chacun, ~3 min)
  13 QA Lead
  35 Integration Engineer
  21 Frontend Engineer
  39 Mobile Engineer

Les agents suivants interviennent uniquement quand ils ont un update :
  14 Security Auditor
  16 Legal
  18 Growth
  29 Technical Writer
  30 DBA Performance
  31 Chaos Engineer
  32 Business Dev
  33 AI Safety
  36 i18n Lead
  37 Content Strategist
  40 Vendor Manager
  41 Support Engineer
```

---

## Template de Compte Rendu Daily

Chaque standup est sauvegarde dans `meetings/daily/YYYY-MM-DD.md` :

```markdown
# Daily Standup — [YYYY-MM-DD]

## Status Sprint : 🟢/🟡/🔴 [Sprint X — Nom]

## Tour de Table

### CEO (01)
- Hier : [...]
- Aujourd'hui : [...]
- Blocage : [aucun / ...]

### CTO (02)
- Hier : [...]
- Aujourd'hui : [...]
- Blocage : [aucun / ...]

[... chaque agent ...]

## Entraide
| Qui a besoin d'aide | Sur quoi | Qui peut aider | Action planifiee |
|---------------------|----------|---------------|-----------------|
| [agent] | [sujet] | [agent] | [quand] |

## Signaux Globaux
- Sprint status : [details]
- VETOs en cours : [aucun / details]
- Decisions en attente : [aucune / details]
- Alertes : [aucune / details]

## Decisions Prises
- [decision] — Par : [qui] — Impact : [quoi]

## Actions Post-Standup
- [ ] [action] — Responsable : [agent] — Deadline : [quand]
```

---

## Regles Non-Negociables

1. **Ponctualite** : Le standup commence a l'heure. Pas de retard.
2. **Brevete** : 2 minutes max par personne. Le PM coupe si ca deborde.
3. **Honnetete** : Si t'es bloque, DIS-LE. Pas de "tout va bien" quand ca va pas.
4. **Ecoute** : Quand quelqu'un parle, tu ecoutes. Pas de multi-tasking.
5. **Action** : Chaque blocage doit avoir une action assignee avant la fin du standup.
6. **Sauvegarde** : Le PM sauvegarde le compte rendu DANS LA JOURNEE.
7. **Historique** : Les comptes rendus ne sont JAMAIS supprimes. C'est la memoire de l'equipe.

---

## Weekly Recap (en plus du daily)

Chaque vendredi, le PM produit un recap hebdomadaire dans `meetings/weekly/YYYY-WXX.md` :

```markdown
# Weekly Recap — Semaine [XX] ([dates])

## Accomplissements
- [ODAI-XXX] [description] — Par : [agent(s)] ✅

## En Cours
- [ODAI-XXX] [description] — Par : [agent(s)] — [% avancement]

## Blocages Non Resolus
- [description] — Depuis : [date] — Impact : [quoi]

## VETOs
- [sujet] — Emis par : [agent] — Status : [en attente / resolu]

## Metriques
- Specs redigees : [n]
- PRs mergees : [n]
- Bugs fixes : [n]
- Tickets support : [n]

## Decisions Prises Cette Semaine
- [decision] — Par : [qui] — Context : [pourquoi]

## Objectifs Semaine Prochaine
1. [objectif] — Responsable : [agent]
2. ...
```
