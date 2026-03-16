# Strategie i18n — OdooAI
## i18n Lead (36) + CPO (03)
## Date : 2026-03-21

## Principe : Anglais d'abord, francais en traduction

### Phase 1 — Sprint 5 (preparation)
- Installer `next-intl`
- Extraire les 58 strings hardcodees en `messages/fr.json`
- Creer `messages/en.json` (traduction anglaise)
- Middleware detection locale navigateur

### Phase 2 — Sprint 6 (activation)
- URL routing : `/fr/...` et `/en/...`
- Le chat detecte la langue de l'utilisateur
- Le prompt LLM s'adapte : "Reponds en [langue]"
- Landing page en 2 langues

### Phase 3 — Sprint 8+ (expansion)
- Langues supplementaires : NL, DE, ES, PT
- BA Profiles multilingues (prompt adapte)
- Crowdsourcing traductions (communaute)

### Framework : next-intl
- Meilleur support App Router + Server Components
- Type-safe
- Bundle size : 2kb
- ICU MessageFormat pour la pluralisation

### Impact sur les BA Profiles
Les BA Profiles sont generes en francais via le prompt. Pour le multilingue :
- Option A : regenerer les BA Profiles dans chaque langue (cout x N)
- Option B : garder les BA en francais, le LLM traduit a la volee (0 cout supplementaire)
- **Recommandation : Option B** — le LLM traduit bien, pas de surcout

### Estimation
- Sprint 5 : 1 jour (setup + extraction)
- Sprint 6 : 1 jour (activation + routing)
- Sprint 8 : 2 jours (3+ langues)
