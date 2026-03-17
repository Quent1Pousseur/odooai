# Review — ODAI-AGENT-001 (Orchestrator + BA Agent + Chat CLI)

## Reviewer : Security Architect (07)
## Date : 2026-03-17
## Status : DONE — 2 high fixes, 3 medium documentes

---

## Issues trouvees

### HIGH-1 : API Key exposure dans exception traceback (CORRIGE)
- **Fichier** : `cli.py` ligne 133
- **Probleme** : Exception raw echoed to stderr — si l'appel API echoue, le traceback peut contenir la cle
- **Fix applique** : Catch generique avec message sanitise, type d'erreur seulement
- **Status** : ✅ Corrige avant commit

### HIGH-2 : Domain ID non valide → path traversal (CORRIGE)
- **Fichier** : `orchestrator.py` ligne 103
- **Probleme** : `domain_id` utilise dans une construction de path sans validation
- **Fix applique** : Validation `domain_id in DOMAIN_NAMES` avant construction
- **Status** : ✅ Corrige avant commit

### MEDIUM-1 : Domain detection injection risk
- **Fichier** : `orchestrator.py` ligne 70
- **Probleme** : Question user passee directement au keyword matching sans sanitization
- **Risque** : Faible (keyword matching only), mais en Sprint 2 avec LLM classification, il faudra sanitizer
- **Status** : Documente pour Sprint 2

### MEDIUM-2 : BA Profile validation faible
- **Fichier** : `orchestrator.py` ligne 111
- **Probleme** : `model_validate()` en catch-all Exception, pas de ValidationError specifique
- **Status** : Documente pour prochaine iteration

### MEDIUM-3 : Single content block extraction
- **Fichier** : `ba_agent.py` ligne 89
- **Probleme** : Seul le premier TextBlock est extrait, les autres ignores
- **Risque** : Faible — Anthropic retourne generalement un seul TextBlock pour les completions simples
- **Status** : Acceptable Sprint 1

---

## Verdict
**Go** — les 2 issues high sont corrigees. Les 3 medium sont documentes et acceptables pour Sprint 1.
