# ODAI-AGENT-001 — Orchestrator + BA Agent + Chat CLI

## Status
DONE (spec redigee apres implementation — erreur de processus)

## Auteur
Backend Architect (08) + AI Engineer (09)

## Reviewers
CTO (02), Security Architect (07), Prompt Engineer (25)

## Date
2026-03-17

## Contexte
Les BA Profiles existent. Il faut un Orchestrator pour router les questions vers le bon BA Profile et un Chat CLI pour que le fondateur puisse tester.

## Objectif
1. Orchestrator : detecte le domaine d'une question, charge le BA Profile, appelle le BA Agent
2. BA Agent : construit le prompt avec le BA Profile en contexte, appelle le LLM, retourne une reponse structuree
3. Chat CLI : `odooai chat` — boucle interactive question/reponse

## Definition of Done
- [x] Orchestrator avec detection de domaine par keywords (9 domaines)
- [x] BA Agent avec system prompt (disclaimer, sources, structure)
- [x] Chat CLI interactif
- [x] Domain detection affichee
- [x] Tokens et sources affiches apres chaque reponse
- [x] Error handling sanitise (pas de leak API key)
- [x] Review interne : API key leak fix + domain_id validation
- [x] mypy --strict clean

## Design

### Flow
```
User question
  → Orchestrator.detect_domain(question) → domain_id
  → Orchestrator.load_ba_profile(domain_id) → BAProfile
  → BA Agent.ask(question, profile) → LLM call → AgentResponse
  → Display answer + sources + tokens
```

### Domain Detection (Sprint 1)
Simple keyword matching. Sprint 2 : classification LLM (Haiku).

### System Prompt BA Agent
- Reponds en francais
- Cite toujours la source (module, modele, champ)
- Ne donne JAMAIS de conseil juridique/fiscal/comptable
- Actions concretes avec niveau de complexite
- Disclaimer en fin de chaque reponse

## Fichiers
| Fichier | Action |
|---------|--------|
| `odooai/agents/__init__.py` | Cree |
| `odooai/agents/orchestrator.py` | Cree |
| `odooai/agents/ba_agent.py` | Cree |
| `odooai/cli.py` | Modifie — ajout chat |

## Securite
- API key jamais dans les messages d'erreur (sanitized)
- domain_id valide contre DOMAIN_NAMES avant construction de path
- System prompt inclut disclaimer obligatoire
- Review : Security Architect (07)

## NOTE PROCESSUS
**Cette spec a ete redigee APRES l'implementation.** Violation de la regle d'or. Ne plus reproduire.

## Estimation
M (1-3 jours) — realise en 1 session
