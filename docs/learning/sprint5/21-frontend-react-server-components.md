# Learning — Frontend Eng (21) — React Server Components for Next.js

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **RSC execute le rendu cote serveur sans hydratation** : Les React Server Components tournent exclusivement sur le serveur. Leur code JS n'est jamais envoye au client, ce qui reduit drastiquement la taille du bundle. Dans Next.js 14+ App Router, tout composant est Server Component par defaut sauf s'il porte la directive `"use client"`.

2. **Le pattern "server-first, client-islands"** : La majorite des pages (layout, sidebar, listes) sont des Server Components. Seuls les elements interactifs (formulaire de chat, boutons d'action, modales) sont des Client Components. Cela minimise le JS client tout en gardant l'interactivite la ou elle est necessaire.

3. **Data fetching natif dans les composants** : Les Server Components peuvent directement appeler des fonctions async (fetch, base de donnees, API backend). Plus besoin de useEffect ou de react-query pour le chargement initial. Le cache Next.js gere la deduplication et le revalidation automatiquement.

4. **Streaming et Suspense ameliorent le TTFB** : Les Server Components supportent le streaming via Suspense boundaries. Le shell de la page arrive immediatement, les parties lentes (resultats d'analyse LLM) s'affichent progressivement. L'utilisateur voit du contenu utile en moins de 200ms.

5. **Les Server Actions remplacent les API routes simples** : Pour les mutations (creer conversation, envoyer message), les Server Actions permettent d'appeler une fonction serveur directement depuis un formulaire ou un bouton client, sans creer de route API intermediaire. Cela reduit le boilerplate.

## Comment ca s'applique a OdooAI

1. **Architecture frontend conversation** : La page de conversation OdooAI est un Server Component qui charge l'historique cote serveur (zero JS pour l'affichage). Le champ de saisie et le bouton d'envoi sont un Client Component `"use client"` qui gere le streaming de la reponse agent via SSE.

2. **Dashboard et sidebar en RSC pur** : La sidebar (liste des conversations), la page de connexions Odoo, et le dashboard usage sont des Server Components. Ils fetchent les donnees depuis le backend FastAPI a chaque navigation. Le bundle JS client reste minimal (< 50kB gzip).

3. **Streaming des reponses agent** : Quand l'agent OdooAI analyse un module Odoo, la reponse peut prendre 5-10 secondes. Avec Suspense + streaming, le frontend affiche immediatement le header de la conversation et le skeleton de la reponse, puis streame les tokens au fur et a mesure via un Client Component dedie.

## Ce que je recommande

1. **Sprint 6** : Auditer les composants frontend existants et convertir en Server Components tout ce qui n'a pas besoin d'interactivite. Objectif : reduire `"use client"` a moins de 30% des composants.

2. **Sprint 7** : Implementer le streaming des reponses agent avec Suspense boundaries. Le Server Component charge le contexte conversation, le Client Component gere le flux SSE temps reel. Mesurer le TTFB avant/apres.

3. **Sprint 7** : Remplacer les API routes simples (creation conversation, envoi formulaire connexion) par des Server Actions. Cela simplifie le code et reduit la surface d'API exposee.

## Sources

1. Next.js Documentation — Server Components & Server Actions (2025)
2. Dan Abramov, "RSC From Scratch" — GitHub Explainer (2024)
3. Lee Robinson, "Understanding React Server Components" — Vercel Blog (2025)
