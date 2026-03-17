# Learning — UX Designer (27) — Design System pour Chat IA
## Date : 2026-03-21
## Duree : 4 heures

## Ce que j'ai appris

### Design patterns des meilleurs chats IA
| Pattern | ChatGPT | Claude | Perplexity | OdooAI actuel |
|---------|---------|--------|-----------|---------------|
| Message bubbles | Flat, wide | Flat, wide | Cards | Rounded, narrow |
| Code blocks | Syntax highlight | Syntax highlight | Inline | Basic `code` |
| Sources | Non | Non | Citations numerotees | Module name only |
| Loading | Dots animation | Cursor typing | Skeleton | Dots + texte |
| Tool calls | Hidden | "Thinking..." | Visible cards | Blockquote |
| Copy button | Oui | Oui | Oui | Non |
| Feedback | Thumbs up/down | Thumbs up/down | Non | Non |

### Ce qui manque a OdooAI
1. **Copy button** sur chaque reponse — essentiel pour copier les recommandations
2. **Feedback thumbs** — savoir si la reponse est utile (data pour l'eval)
3. **Sources cliquables** — lien vers la doc Odoo du module cite
4. **Code blocks** avec syntax highlighting si le LLM donne du code Odoo
5. **Skeleton loading** au lieu du texte "OdooAI reflechit..."

### Composants du design system
```
Tokens:
  colors: primary, accent, success, warning, error, gray-50→900
  spacing: 4, 8, 12, 16, 24, 32, 48
  radius: sm(6), md(12), lg(16), xl(24)
  font: Inter (body), JetBrains Mono (code)

Components:
  ChatBubble: user | assistant | system
  ToolCallCard: icon + label + status (searching/found/error)
  SourceBadge: module name, clickable
  CopyButton: icon, tooltip "Copie !"
  FeedbackButtons: thumbs up + thumbs down
  SkeletonMessage: animated placeholder
  QuickAction: bordered button with icon
```

## Comment ca s'applique a OdooAI
- Le design system n'existe pas encore — chaque composant est style inline
- Un design system Tailwind avec des classes utilitaires suffit pour le MVP
- Les 5 composants manquants (copy, feedback, sources, code, skeleton) sont chacun < 1h

## Ce que je recommande
1. Sprint 5 : Copy button + Feedback thumbs (2h)
2. Sprint 5 : Design tokens documentes dans un fichier
3. Sprint 6 : Composants refactores avec le design system
4. Sprint 6 : Storybook pour documenter les composants

## Sources
- ChatGPT UI patterns (analyse reverse)
- Vercel AI SDK chat components
- Shadcn/ui chat template
