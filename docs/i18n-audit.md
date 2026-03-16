# Audit i18n — Strings hardcodees dans le frontend
## i18n Lead (36)
## Date : 2026-03-21

## Fichiers audites

### page.tsx (chat principal) — 8 strings
1. "OdooAI"
2. "Business Analyst intelligent"
3. "Comment puis-je vous aider ?"
4. "Posez une question sur votre Odoo — configuration, fonctionnalites cachees, optimisations."
5. "Quelles fonctionnalites je n'utilise pas ?"
6. "Comment optimiser mes stocks ?"
7. "Mes relances sont-elles automatisees ?"
8. "OdooAI ne fournit pas de conseil juridique, fiscal ou comptable."
9. "Erreur de connexion au serveur."
10. "OdooAI reflechit..."
11. "Recherche en cours"

### chat-input.tsx — 2 strings
1. "Posez votre question sur Odoo..."
2. "Envoyer"

### odoo-connect.tsx — 10 strings
1. "Connecte"
2. "Deconnecter"
3. "Connecter Odoo"
4. "Connexion a votre Odoo"
5. "URL instance"
6. "Base de donnees"
7. "Login"
8. "Cle API"
9. "Annuler"
10. "Connecter"
11. "Vos identifiants ne sont pas stockes — session uniquement."
12. Tous les placeholders (4)

### landing/page.tsx — 20+ strings
- Hero, stats, features, pricing, email capture, footer
- Tout le contenu marketing

### chat-message.tsx — 2 strings
1. "tokens"
2. Separateur "·"

### layout.tsx — 2 strings
1. "OdooAI — Votre Odoo peut faire plus"
2. Description meta

## Total : ~58 strings a extraire

## Structure recommandee (next-intl)

```
frontend/
  messages/
    fr.json     # { "chat.title": "OdooAI", "chat.subtitle": "Business Analyst intelligent", ... }
    en.json     # { "chat.title": "OdooAI", "chat.subtitle": "Intelligent Business Analyst", ... }
  i18n.ts       # Configuration next-intl
  middleware.ts  # Detection locale navigateur
```

## Priorite d'extraction

| Priorite | Fichier | Strings | Effort |
|----------|---------|---------|--------|
| P1 | page.tsx | 11 | 30 min |
| P2 | odoo-connect.tsx | 14 | 30 min |
| P3 | chat-input.tsx | 2 | 10 min |
| P4 | landing/page.tsx | 20+ | 1h |
| P5 | layout.tsx | 2 | 5 min |

**Total : ~2h30 pour tout extraire.**

## A faire en Sprint 5
1. `npm install next-intl`
2. Creer `messages/fr.json` et `messages/en.json`
3. Extraire les strings par priorite (P1-P5)
4. Middleware de detection de langue
