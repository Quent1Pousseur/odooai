# Learning — i18n Lead (36) — Internationalisation Next.js
## Date : 2026-03-20
## Duree : 3 heures

## Ce que j'ai appris

### Comparaison des frameworks i18n pour Next.js 14+

| Critere | next-intl | react-i18next | next-translate |
|---------|-----------|---------------|----------------|
| App Router support | Excellent | Bon | Moyen |
| Server Components | Natif | Plugin | Non |
| Bundle size | 2kb | 8kb | 3kb |
| ICU MessageFormat | Oui | Oui | Non |
| Pluralisation | Oui | Oui | Basique |
| Type safety | Excellent | Moyen | Non |

**Recommandation : next-intl** — meilleur support App Router + Server Components + type safety.

### Strategie "anglais d'abord"
- Les strings UI doivent etre en anglais par defaut (code source)
- Le francais devient une traduction comme les autres
- Avantage : le marche mondial est accessible nativement
- Les BA Profiles et les reponses LLM sont deja en francais via le prompt — ca ne change pas

### Structure recommandee
```
frontend/
  messages/
    en.json    # Strings UI en anglais (defaut)
    fr.json    # Traduction francaise
  middleware.ts  # Detection locale navigateur
  i18n.ts       # Configuration next-intl
```

### Strings hardcodees identifiees dans le frontend actuel
- `page.tsx` : "OdooAI", "Votre Odoo peut faire plus." (header)
- `chat-input.tsx` : placeholder "Posez votre question..."
- `odoo-connect.tsx` : tous les labels du formulaire
- `landing/page.tsx` : tout le contenu marketing
- Total estime : ~60 strings a extraire

## Comment ca s'applique a OdooAI

- Le frontend est 100% francais — pas deployable a l'international en l'etat
- 60 strings a extraire, effort estime : 1 jour
- Le prompt LLM doit detecter la langue de l'utilisateur et repondre en consequence
- Les BA Profiles sont en francais — il faudra un prompt multilingue plus tard

## Ce que je recommande

1. Sprint 5 : installer next-intl + extraire les 60 strings
2. Sprint 5 : ajouter `en.json` et `fr.json`
3. Sprint 6 : detection automatique de la langue navigateur
4. Plus tard : prompt multilingue pour les reponses LLM

## Sources
- next-intl documentation (next-intl.dev)
- Next.js 14 Internationalization guide
- ICU MessageFormat specification
