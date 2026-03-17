# Learning — Brand Designer (42) — SaaS Brand Identity Design
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

1. **Le "Trust Signal" visuel est critique pour un SaaS B2B early stage** — Les
   prospects B2B jugent la credibilite en 3 secondes. Les elements qui construisent
   la confiance : palette sobre (bleu/gris > rouge/jaune), typographie professionnelle
   (Inter, Plus Jakarta Sans), logos clients/partenaires, badges de securite.
   Linear, Vercel et Resend sont les references actuelles en design SaaS.

2. **Le systeme de design "token-based" accelere le developpement** — Definir des
   design tokens (couleurs, espacements, typographies, border-radius) dans un fichier
   central permet a l'equipe frontend de construire sans demander au designer.
   Tailwind CSS + CSS custom properties est le standard. Notre stack Tailwind + Shadcn
   est parfaitement alignee.

3. **L'identite visuelle doit refleter le positionnement** — OdooAI est un "Business
   Analyst IA" : l'identite doit communiquer intelligence + fiabilite + expertise.
   Pas un chatbot fun (comme Character.ai) ni un outil dev (comme GitHub).
   Reference : comment Notion communique "puissance + simplicite" visuellement.

4. **Le logo doit fonctionner en 4 contextes** — Favicon (16x16), sidebar (32x32),
   landing page (full), et dark mode. Un logomark (icone seule) + logotype (texte)
   modulaires couvrent tous les cas. Eviter les logos trop detailles qui deviennent
   illisibles en petit.

5. **La palette "AI-native" emerge comme tendance 2026** — Fond sombre avec accents
   lumineux (violet, bleu electrique, vert menthe) signale "produit IA" sans le dire.
   Claude utilise un orange chaud, ChatGPT un vert minimal. OdooAI doit trouver
   sa couleur signature qui evoque la fiabilite (bleu) + l'intelligence (violet).

## Comment ca s'applique a OdooAI

1. **Palette de marque OdooAI** : Proposer une palette primaire bleu profond (#1a365d)
   + accent violet intelligent (#6d28d9) + neutre slate (#64748b). Le bleu evoque
   la confiance B2B, le violet evoque l'IA/intelligence. Fond clair par defaut,
   dark mode avec fond #0f172a. Compatible avec Tailwind et Shadcn.

2. **Design tokens centralises** : Creer un fichier `tokens.css` qui definit toutes
   les variables de design. Integrer ces tokens dans `tailwind.config.ts` pour que
   chaque composant Shadcn utilise automatiquement la marque OdooAI. Eliminer
   toute couleur hardcodee dans les composants actuels.

3. **Logo modulaire** : Designer un logomark qui combine un symbole de "flux de
   donnees" (representant l'analyse) avec une forme geometrique stable (representant
   Odoo/ERP). Le logomark seul sert de favicon et d'icone sidebar. Le logotype
   "OdooAI" utilise Plus Jakarta Sans Bold.

## Ce que je recommande

1. **Sprint 8** : Livrer le brand guide V1 — palette, typographie, espacements,
   border-radius, shadows. Format : fichier `tokens.css` + `tailwind.config.ts`
   mis a jour + 1 page Figma de reference. Fichiers : `web/styles/tokens.css`.

2. **Sprint 8** : Designer 3 variations de logo (geometric, abstract, typographic)
   et les presenter au fondateur. Livrer en SVG optimise pour les 4 contextes
   (favicon, sidebar, landing, dark mode). Fichier : `web/public/brand/`.

3. **Sprint 9** : Auditer tous les composants frontend existants et remplacer les
   couleurs Shadcn par defaut par les tokens OdooAI. Verifier le contraste WCAG AA
   sur chaque combinaison texte/fond. Fichier : `web/components/ui/`.

## Sources

1. Refactoring UI — Adam Wathan & Steve Schoger — Principes de design pour developpeurs
2. Linear.app — Etude de cas brand identity SaaS (design.linear.app)
3. "Building a Brand" — Michael Johnson (2022) — Methodologie de creation d'identite
