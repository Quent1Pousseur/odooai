# Audit Responsive — Frontend OdooAI
## Mobile Engineer (39) + UX Designer (27)
## Date : 2026-03-21

## Resultats par page

### Chat (page.tsx)
| Element | Desktop | Tablet | Mobile (375px) | Mobile (320px) |
|---------|---------|--------|----------------|----------------|
| Header | ✅ | ✅ | ✅ | ✅ |
| Messages | ✅ | ✅ | ✅ | ✅ |
| Input | ✅ | ✅ | ⚠️ Petit | ⚠️ Petit |
| Sidebar toggle | ✅ | ✅ | ⚠️ Pas de hamburger | ⚠️ Pas de hamburger |
| Odoo Connect modal | ✅ | ✅ | ✅ | ⚠️ Padding serre |
| Quick questions | ✅ | ✅ | ✅ | ⚠️ Wrap ok |

### Landing (/landing)
| Element | Desktop | Tablet | Mobile (375px) | Mobile (320px) |
|---------|---------|--------|----------------|----------------|
| Hero | ✅ | ✅ | ✅ | ✅ |
| Stats grid | ✅ | ✅ | ✅ | ✅ |
| Features grid | ✅ | ✅ | ✅ (1 col) | ✅ |
| Pricing cards | ✅ | ✅ | ✅ (1 col) | ⚠️ Overflow horizontal |
| Email form | ✅ | ✅ | ✅ | ⚠️ Bouton serre |

## 3 Fixes identifies

### Fix 1 — Chat input min-height (FAIT dans la passe design)
- `min-h-[48px]` ajoute au chat-input.tsx ✅

### Fix 2 — Sidebar hamburger sur mobile
- Actuellement : bouton sidebar visible mais pas de hamburger icon
- Fix : ajouter un `Menu` icon de lucide-react sur mobile
- Effort : 30 min

### Fix 3 — Pricing cards overflow 320px
- Actuellement : les 3 cards debordent horizontalement sur iPhone SE
- Fix : `overflow-x-auto` ou `flex-wrap` sur le container
- Effort : 10 min

## Lighthouse scores estimes

| Metrique | Score estime | Cible |
|----------|-------------|-------|
| Performance | 70 | 85+ |
| Accessibility | 75 | 90+ |
| Best Practices | 80 | 90+ |
| SEO | 55 | 80+ |

## Actions Sprint 5
1. Fix sidebar hamburger (30 min)
2. Fix pricing overflow (10 min)
3. Ajouter meta tags SEO (20 min)
4. Ajouter aria-labels (30 min)
5. Lazy loading images si on en ajoute
