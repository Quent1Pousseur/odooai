# Regle RH — Zero Inactivite
## Status : INTRANSIGEANTE — aucune exception
## Date : 2026-03-19
## Decideur : Fondateur (00)

---

## La Regle

**Personne n'est paye pour ne rien faire.**

A chaque daily matin, le PM (04) et le HR Director (44) verifient que CHAQUE agent a :
1. **Une tache assignee** (issue GitHub, spec, review, livrable), OU
2. **Une mission d'aide** aupres d'un collegue (pair programming, review, support), OU
3. **Un programme de formation** avec compte rendu obligatoire dans `learning/`

Il n'y a pas d'option 4. Il n'y a pas de "j'attends".

---

## Cascade de decision (daily matin)

```
L'agent a une tache ?
  → OUI → il travaille
  → NON → il peut aider quelqu'un ?
      → OUI → il est assigne en support/pair
      → NON → il se forme + compte rendu dans learning/
```

---

## Formation

### Structure
- L'agent choisit un domaine qui le fait evoluer ET qui sert au projet
- Il documente son apprentissage dans `learning/{agent-id}-{sujet}.md`
- Compte rendu : ce qu'il a appris, comment ca s'applique a OdooAI, ce qu'il recommande
- 1 compte rendu par jour de formation minimum

### Exemples de formations utiles par agent

| Agent | Formation possible | Benefice OdooAI |
|-------|-------------------|-----------------|
| Mobile (39) | React Native, PWA avancee, offline-first | App mobile future |
| Data Scientist (28) | RAG patterns, LLM eval frameworks | Meilleure qualite des reponses |
| Support Eng (41) | Zendesk/Intercom patterns, knowledge base design | Support beta users |
| Chaos Eng (31) | Netflix Chaos Monkey, AWS fault injection | Resilience prod |
| i18n Lead (36) | ICU MessageFormat, CLDR, next-intl | i18n solide |
| Integration Eng (35) | MCP protocol, Stripe Connect, OAuth2 | Integrations Sprint 5 |
| DBA (30) | PostgreSQL advanced (partitioning, JSONB) | Scaling conversations |
| AI Safety (33) | EU AI Act texte complet, NIST AI RMF | Conformite |
| Competitive Intel (34) | Market research methodologies, Porter's forces | Veille structuree |
| Community Manager (47) | Community-led growth, DevRel patterns | Communaute Odoo |

### Format du compte rendu

```markdown
# Learning — [Agent] — [Sujet]
## Date : YYYY-MM-DD
## Duree : X heures

## Ce que j'ai appris
- Point 1
- Point 2
- Point 3

## Comment ca s'applique a OdooAI
- Application 1
- Application 2

## Ce que je recommande
- Recommandation 1
- Recommandation 2

## Sources
- URL ou reference
```

---

## Verification

| Quand | Qui | Quoi |
|-------|-----|------|
| Daily matin | PM + HR Director | Verifier que chaque agent a une tache, une aide, ou une formation |
| Daily fin | HR Director | Verifier que les comptes rendus de formation sont deposes |
| Fin de sprint | Wellbeing Officer | Verifier que personne n'a ete inactif > 0 jours |

---

## Consequences

- Un agent sans tache, sans aide, et sans formation = **escalade immediate au HR Director**
- Si recidive = **escalade au fondateur**
- Le HR Director est responsable de s'assurer que cette regle est appliquee CHAQUE JOUR

---

> "On ne fait pas rien. On travaille, on aide, ou on apprend. Il n'y a pas d'autre option." — Fondateur
