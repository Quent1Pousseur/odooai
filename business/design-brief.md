# OdooAI — Design Brief (UI/UX + Direction Artistique)

## Auteurs : UX Designer (27) + Brand Designer (42) + CPO (03)
## Date : 2026-03-17

---

## 1. Direction Artistique

### Positionnement visuel
OdooAI est un **outil professionnel pour PME**. Pas un jouet, pas une startup tech cool. C'est l'equivalent d'un consultant senior — serieux, fiable, accessible.

### Valeurs a transmettre
| Valeur | Ce que ca veut dire visuellement |
|--------|--------------------------------|
| **Fiabilite** | Couleurs sobres, typographie propre, pas de decoration superflue |
| **Accessibilite** | Langage simple, icones claires, responsive, accessible WCAG 2.1 AA |
| **Intelligence** | Donnees structurees, visualisations, pas de mur de texte |
| **Securite** | Cadenas, badges, indicateurs de confidentialite |

### Palette de couleurs (proposition)
```
Primary:    #1B4965  (bleu fonce — confiance, professionnel)
Secondary:  #62B6CB  (bleu clair — accessible, moderne)
Accent:     #BEE9E8  (turquoise pale — fraicheur)
Success:    #2D6A4F  (vert — confirmation, securite)
Warning:    #E76F51  (orange — attention, action requise)
Danger:     #D62828  (rouge — erreur, blocage)
Background: #F8F9FA  (gris tres clair)
Text:       #212529  (quasi-noir)
```

> **Brand Designer (42)** : "Le bleu fonce transmet la confiance. C'est la couleur des banques et des outils enterprise. Le turquoise ajoute de la modernite sans etre flashy."
>
> **CPO (03)** : "Marie (notre persona) utilise Odoo tous les jours. L'interface doit etre aussi propre qu'Odoo, pas un choc visuel."

### Typographie
- **Titres** : Inter (sans-serif, propre, lisible)
- **Corps** : Inter (meme famille, coherent)
- **Code/donnees** : JetBrains Mono (monospace, technique)

### Logo (a creer)
- Concept : "AI + Odoo" — un symbole qui evoque l'intelligence artificielle appliquee a l'ERP
- Direction : minimaliste, geometrique, monochrome compatible
- A eviter : trop de couleurs, effets 3D, gradients complexes

---

## 2. UI/UX — Architecture des ecrans

### Flow utilisateur principal
```
1. LANDING PAGE
   → "Votre Odoo peut faire plus" + CTA "Commencer"

2. CONNEXION ODOO
   → URL instance + login + API key
   → Detection auto version + modules installes
   → Indicateur de securite (cadenas, chiffrement)

3. DASHBOARD (aha moment)
   → Score d'utilisation : "Vous utilisez 34% de votre Odoo"
   → Top 5 fonctionnalites non-activees
   → Chaque suggestion = 1 carte cliquable

4. CHAT (interaction principale)
   → Zone de saisie en bas (comme tous les chats)
   → Reponses structurees (pas de mur de texte)
   → Sources citees (module, champ, version)
   → Actions proposees avec bouton "Executer" (double validation)

5. ACTIONS
   → Modal de confirmation AVANT execution
   → Affichage avant/apres
   → Bouton "Annuler" si possible
```

### Ecrans detailles

#### Landing Page
```
┌─────────────────────────────────────────┐
│  [Logo OdooAI]           [Connexion]    │
│                                         │
│    Votre Odoo peut faire plus.          │
│    L'IA vous montre comment.            │
│                                         │
│    [Commencer gratuitement]             │
│                                         │
│  ┌─────┐ ┌─────┐ ┌─────┐               │
│  │ 1218│ │5514 │ │ 24/7│               │
│  │ mod.│ │ mod.│ │     │               │
│  │ ana.│ │ ext.│ │dispo│               │
│  └─────┘ └─────┘ └─────┘               │
│                                         │
│  Plans a partir de 49€/mois            │
└─────────────────────────────────────────┘
```

#### Dashboard (post-connexion)
```
┌─────────────────────────────────────────┐
│  [Logo]  Marie ▾   [?] [⚙]             │
│─────────────────────────────────────────│
│                                         │
│  Score d'utilisation Odoo               │
│  ████████████░░░░░░░░░░░░ 34%          │
│                                         │
│  Fonctionnalites a decouvrir :          │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 📦 Reception 3 etapes          │    │
│  │ Automatisez vos receptions     │    │
│  │ stock avec validation qualite  │    │
│  │                  [En savoir +] │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │ 💰 Relances automatiques       │    │
│  │ Configurez les rappels de      │    │
│  │ paiement automatiques          │    │
│  │                  [En savoir +] │    │
│  └─────────────────────────────────┘    │
│                                         │
│  [💬 Poser une question a OdooAI]      │
└─────────────────────────────────────────┘
```

#### Chat
```
┌─────────────────────────────────────────┐
│  [Logo]  Marie ▾   [?] [⚙]             │
│─────────────────────────────────────────│
│                                         │
│  ┌─ OdooAI ──────────────────────────┐  │
│  │ Bonjour Marie ! Je vois que vous  │  │
│  │ utilisez Stock mais sans les      │  │
│  │ receptions en 3 etapes.           │  │
│  │                                   │  │
│  │ Voulez-vous que je vous explique  │  │
│  │ comment les activer ?             │  │
│  │                                   │  │
│  │ 📎 Source: stock.warehouse,       │  │
│  │    champ reception_steps          │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌─ Marie ───────────────────────────┐  │
│  │ Oui, explique-moi                 │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌─ OdooAI ──────────────────────────┐  │
│  │ Voici les 3 etapes :              │  │
│  │                                   │  │
│  │ 1. Allez dans Stock > Config     │  │
│  │ 2. Selectionnez votre entrepot   │  │
│  │ 3. Changez "Reception" → "3 et." │  │
│  │                                   │  │
│  │ [🔧 Activer automatiquement]     │  │
│  │                                   │  │
│  │ ⚠️ OdooAI ne fournit pas de     │  │
│  │ conseil juridique ou comptable.   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────[➤]─┐  │
│  │ Tapez votre question...           │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

#### Modal double validation (ecriture)
```
┌──────────────────────────────────────┐
│  ⚠️ Confirmer l'action               │
│                                      │
│  OdooAI va modifier votre Odoo :     │
│                                      │
│  Module : Stock                      │
│  Action : Activer reception 3 etapes │
│  Entrepot : Principal                │
│                                      │
│  Avant : reception_steps = "one"     │
│  Apres : reception_steps = "three"   │
│                                      │
│  ⚠️ Cette action est reversible.    │
│                                      │
│  [Annuler]          [✅ Confirmer]   │
└──────────────────────────────────────┘
```

---

## 3. Principes UX

### Regles non-negociables (CPO)
1. **Time-to-aha < 2 min** — de la connexion a la premiere decouverte
2. **Zero jargon technique** — pas de `ir.model`, pas de `res.partner`, parler business
3. **Sources toujours citees** — le LLM ne dit jamais "je pense", il cite le module et le champ
4. **Double validation** — jamais d'ecriture sans confirmation explicite
5. **Disclaimer visible** — "OdooAI ne fournit pas de conseil juridique/fiscal/comptable"
6. **Mobile-friendly** — 60%+ des dirigeants PME consultent sur mobile

### Responsive
- Desktop : 3 colonnes (sidebar + chat + detail)
- Tablet : 2 colonnes (chat + detail)
- Mobile : 1 colonne (chat only, navigation hamburger)

### Accessibilite (WCAG 2.1 AA)
- Contraste texte/fond >= 4.5:1
- Navigation clavier complete
- Labels sur tous les inputs
- Alt text sur toutes les images

---

## 4. Stack Frontend (confirme du kick-off)
- **Framework** : Next.js 14+ (App Router)
- **Language** : TypeScript strict
- **Styling** : Tailwind CSS
- **Components** : Shadcn/ui (base) + custom
- **Chat streaming** : Vercel AI SDK
- **State** : React Server Components + SWR
- **Icons** : Lucide

---

## 5. Prochaines etapes design

| Action | Qui | Deadline |
|--------|-----|----------|
| Finaliser palette + typographie | Brand Designer (42) | Sprint 2 |
| Wireframes Figma (5 ecrans) | UX Designer (27) | Sprint 2 |
| Logo v1 (3 propositions) | Brand Designer (42) | Sprint 2 |
| Design system Shadcn custom | UX Designer (27) | Phase 2 debut |
| Landing page design | Brand Designer (42) + Content (37) | Phase 2 |

> **UX Designer (27)** : "Les wireframes ASCII ci-dessus sont le point de depart. Je les transforme en Figma des Sprint 2. Le chat est le coeur — tout le reste en decoule."
>
> **Brand Designer (42)** : "Le logo est la prochaine priorite visuelle. Sans logo, pas de one-pager pro pour Sales."
>
> **CPO (03)** : "Le dashboard avec le score d'utilisation est le aha moment visuel. C'est ce qui differencie OdooAI d'un simple chatbot."
>
> **Frontend Engineer (21)** : "Shadcn/ui + Tailwind = composants propres sans reinventer la roue. Le chat streaming avec Vercel AI SDK est battle-tested. Je suis pret a coder des que le design est valide."
>
> **i18n Lead (36)** : "Rappel : francais d'abord, anglais ensuite. Tous les textes UI doivent passer par un systeme i18n (next-intl). Pas de strings hardcodees."
>
> **AI Safety (33)** : "Le disclaimer dans le chat est bien place. Mais il faut aussi un disclaimer dans le modal de double validation : 'Cette action modifie votre instance Odoo. Verifiez avant de confirmer.'"
