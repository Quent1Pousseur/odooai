# Learning — Mobile Engineer (39) — PWA & Offline-First
## Date : 2026-03-20
## Duree : 4 heures

## Ce que j'ai appris

### PWA pour un SaaS comme OdooAI
- Une PWA (Progressive Web App) permet d'installer le chat OdooAI comme une app native
- Service Worker cache les assets statiques → chargement instantane
- Offline : on peut afficher les conversations passees meme sans internet
- Push notifications : alerter l'utilisateur quand une analyse est terminee

### Ce qui est installable en PWA vs ce qui necessite internet
| Feature | Offline possible ? | Comment |
|---------|-------------------|---------|
| Ouvrir l'app | Oui | Service Worker cache |
| Lire les conversations passees | Oui | IndexedDB local |
| Poser une question | Non | Necessite l'API |
| Voir les BA Profiles | Oui si pre-cache | Cache Strategy |
| Voir le landing page | Oui | Static assets |

### Audit responsive actuel
- Chat : ✅ responsive grace a Tailwind (flex, max-w)
- Formulaire connexion : ✅ modal responsive
- Landing page : ✅ grid responsive (md:grid-cols-3)
- Sidebar : ⚠️ pas de hamburger menu sur mobile — overlay seulement
- Chat input : ⚠️ petit sur iPhone SE (min-height needed)

### Lighthouse scores estimes (sans optimisation)
- Performance : ~70 (pas de lazy loading, pas de compression images)
- Accessibility : ~80 (pas de aria-labels sur les boutons icon)
- Best Practices : ~85 (pas de CSP, pas de HTTPS en dev)
- SEO : ~60 (pas de meta tags, pas de sitemap)
- PWA : 0 (pas de manifest, pas de service worker)

## Comment ca s'applique a OdooAI

- La PWA est un quick win : manifest.json + service worker basique = installable sur mobile
- Le chat est deja responsive mais 2 fixes necessaires (sidebar + input)
- Lighthouse performance peut monter a 90+ avec lazy loading + image optimization
- L'accessibilite est critique pour les PME (dirigeants ages, dyslexie, etc.)

## Ce que je recommande

1. Sprint 5 : manifest.json + icons + meta tags (1h de travail)
2. Sprint 5 : Fix sidebar mobile (hamburger) + chat input height
3. Sprint 5 : Service Worker basique (cache assets statiques)
4. Sprint 6 : IndexedDB pour les conversations offline
5. Sprint 6 : Push notifications quand analyse terminee

## Sources
- web.dev/progressive-web-apps
- Next.js PWA avec next-pwa
- Lighthouse scoring documentation
