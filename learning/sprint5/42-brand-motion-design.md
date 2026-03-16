# Learning — Brand Designer (42) — Micro-animations and Motion Design for SaaS Chat
## Date : 2026-03-21 (Sprint 5, session 2)
## Duree : 3 heures

## Ce que j'ai appris

1. **Les micro-animations servent 3 fonctions dans un chat IA** — Feedback (confirmer qu'une
   action a ete prise), etat (montrer que le systeme travaille), et transition (guider l'oeil
   entre deux etats de l'UI). Chaque animation doit servir exactement une de ces fonctions.
   Si elle ne sert aucune, elle doit etre supprimee.

2. **Le timing "snappy" est entre 150ms et 300ms** — En dessous de 100ms, l'animation est
   invisible. Au-dessus de 400ms, elle ralentit l'interface. Pour un chat ou la reactivite
   est attendue, viser 200ms pour les transitions d'elements et 150ms pour les feedbacks
   tactiles (bouton press, hover). Le cubic-bezier(0.4, 0, 0.2, 1) de Material Design est
   un excellent defaut.

3. **Le "typing indicator" est un contrat de confiance** — Les trois points animes qui
   indiquent que l'IA "reflechit" reduisent l'anxiete d'attente de 40% selon les etudes
   UX. Mais il doit apparaitre dans les 500ms suivant l'envoi du message. Au-dela, l'user
   pense que son message n'a pas ete recu. Pour les reponses longues (>5s), ajouter un
   texte contextuel ("Analyse du schema en cours...").

4. **Framer Motion est le standard React pour les animations complexes** — `AnimatePresence`
   gere les animations d'entree/sortie des messages. `layout` anime automatiquement les
   repositionnements quand de nouveaux messages arrivent. Le pattern `variants` permet de
   definir des animations reutilisables coherentes dans toute l'app.

5. **Le "skeleton loading" bat le spinner pour le contenu structure** — Pour les reponses IA
   qui contiennent du code, des tableaux, ou des listes, afficher un skeleton qui imite la
   forme du contenu attendu. Ca reduit le perceived loading time de 30% par rapport a un
   spinner generique et evite le "layout shift" quand le contenu arrive.

## Comment ca s'applique a OdooAI

- **Animation d'arrivee des messages avec stagger** — Chaque bulle de message apparait avec
   un fade-in + slide-up leger (translateY: 8px -> 0, opacity: 0 -> 1, 200ms). Quand
   plusieurs messages arrivent en sequence (ex: reponse multi-parties), un stagger de 80ms
   entre chaque bulle cree un rythme naturel et lisible.

- **Typing indicator contextuel pour les agents** — Plutot qu'un simple "..." generique,
   afficher le type d'operation en cours : "Recherche dans le knowledge graph...",
   "Analyse des champs du modele...", "Generation de la reponse...". Ca eduque l'utilisateur
   sur la puissance du systeme tout en reduisant la frustration d'attente.

- **Transition fluide entre sidebar et chat** — Quand l'utilisateur selectionne une
   conversation dans la sidebar, le chat doit transitionner sans flash blanc. Un crossfade
   de 250ms sur le contenu du chat pendant que le header slide les infos de la conversation
   cree une experience premium.

## Ce que je recommande

1. **Sprint 6 : creer un fichier motion-tokens.ts** — Definir les constantes d'animation
   globales : durations (fast: 150ms, normal: 200ms, slow: 300ms), easings, et variants
   Framer Motion reutilisables. Toute l'equipe frontend utilise ces tokens.

2. **Sprint 7 : implementer le typing indicator contextuel** — Composant React avec 3 etats
   visuels (dots, texte contextuel, skeleton preview). Connecte au stream SSE du backend
   pour afficher l'etape en cours.

3. **Sprint 8 : audit de performance des animations** — Mesurer le FPS pendant les animations
   sur mobile (iPhone 12 min) et desktop. Objectif : 60fps constant. Desactiver les
   animations sur les appareils avec `prefers-reduced-motion`.

## Sources

- Google Material Design — "Understanding Motion" guidelines (2025)
- Framer Motion Documentation — "AnimatePresence" and "Layout Animations" (2025)
- Val Head — "Designing Interface Animation" (Rosenfeld Media, 2023)
