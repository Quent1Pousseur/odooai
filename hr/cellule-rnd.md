# Cellule R&D — OdooAI Innovation Lab
## Date : 2026-03-21
## Decideur : Fondateur (00)
## Responsable : CTO (02) + HR Director (44)

---

## Principe

Chaque agent qui n'a pas de tache directe peut travailler sur un **projet perso** lie a OdooAI. C'est pas du temps perdu — c'est de l'innovation. Les meilleurs projets R&D deviennent des features du produit.

## Cascade (mise a jour)

```
L'agent a une tache ?
  → OUI → il travaille
  → NON → il peut aider quelqu'un ?
      → OUI → il aide (pair/support)
      → NON → il a un projet R&D en cours ?
          → OUI → il avance son projet R&D
          → NON → il se forme (learning CR)
```

**R&D passe AVANT la formation.** Un agent qui a un projet R&D ne fait pas de learning — il innove.

## Regles R&D

### Qui peut faire de la R&D ?
Tout agent sans tache directe. Pas besoin d'approbation pour demarrer — juste informer le CTO.

### Quoi ?
Un projet perso qui :
- Est lie a OdooAI (pas un side project sans rapport)
- A un objectif clair (pas "explorer vaguement")
- Peut devenir une feature, un outil, ou une amelioration
- Est documentable et partageable

### Comment ?
1. Creer un fichier `rnd/[agent-id]-[nom-projet].md` avec : objectif, plan, avancement
2. Travailler dessus quand pas de tache directe
3. Presenter l'avancement au Show & Tell (chaque sprint)
4. Si le projet est mur → proposer en spec pour le sprint suivant

### Exemples de projets R&D

| Agent | Projet possible | Impact potentiel |
|-------|----------------|-----------------|
| Data Scientist (28) | Eval automatique LLM avec scoring ML | Qualite reponses automatisee |
| Odoo Expert (10) | Parseur de workflows/state machines | KG enrichis avec les transitions |
| Chat Eng (43) | Mode vocal (speech-to-text → chat) | Accessibilite, mobile |
| Mobile Eng (39) | App React Native MVP | Marche mobile |
| Integration Eng (35) | MCP server prototype | Ecosysteme Claude Desktop |
| DBA (30) | Cache intelligent avec embeddings | Reponses instantanees |
| UX Designer (27) | Dashboard KPIs avec charts | Valeur visible au premier regard |
| Brand Designer (42) | Animations Framer Motion | UX premium |
| i18n Lead (36) | Traduction automatique BA Profiles | Marche international |
| SOC (26) | Honeypot de detection d'attaques | Securite proactive |
| Growth (18) | Chatbot de qualification leads | Acquisition automatisee |
| Content Strat (37) | Generateur d'articles SEO depuis les KG | Acquisition organique |
| Chaos Eng (31) | Framework de resilience testing | Antifragilite |
| Community Mgr (47) | Bot Discord pour les beta users | Engagement communaute |
| Support Eng (41) | Chatbot support basé sur la KB | Self-service |

### Format du fichier R&D

```markdown
# R&D — [Agent] — [Nom du projet]
## Date debut : YYYY-MM-DD
## Status : En cours / Pause / Termine / Propose en spec

## Objectif
[1-2 phrases]

## Plan
1. [Etape 1]
2. [Etape 2]
3. [Etape 3]

## Avancement
### Session X (date)
- Ce que j'ai fait
- Ce que j'ai decouvert
- Prochaine etape

## Resultat
[Quand termine — ce que ca donne, demo/prototype/doc]
```

### Evaluation

A chaque retro, le CTO et le fondateur evaluent les projets R&D :
- **Adopt** → le projet devient une spec pour le prochain sprint
- **Continue** → le projet avance, on attend plus de maturite
- **Pause** → le projet est en attente (priorite autre)
- **Kill** → le projet n'a pas d'avenir, on arrete

### Budget R&D

Les projets R&D qui necessitent des couts (tokens LLM, API externe) doivent etre approuves par le CFO. Budget max : $50/sprint pour la R&D.

---

> "L'innovation ne vient pas des meetings — elle vient des gens qui ont le temps de penser." — Fondateur
