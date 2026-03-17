# Learning — CPO (03) — Benchmark UX Chat : ChatGPT, Claude, Intercom
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

1. **Le streaming token-by-token est devenu le standard minimum** — ChatGPT et Claude
   affichent les reponses en streaming. Les utilisateurs percoivent un delai > 2s avant
   le premier token comme un bug. Notre implementation SSE dans FastAPI doit viser
   un Time-To-First-Token (TTFT) < 1.5s.

2. **Les "artifacts" de Claude sont un game-changer UX** — Separer le contenu
   actionnable (code, tableaux, configs) du texte conversationnel dans un panneau
   lateral. Pour OdooAI, afficher les recommandations de configuration Odoo dans
   un artifact editable serait un differenciateur fort vs. un simple chatbot.

3. **Intercom utilise le "Resolution Bot" pattern** — Le bot tente de resoudre, puis
   escalade a un humain. Pour OdooAI, le pattern equivalent : le chat IA analyse,
   puis propose une action concrete dans Odoo (avec confirmation utilisateur).
   Le taux de "self-service resolution" est la metrique cle.

4. **La conversation multi-tour avec contexte est critique** — ChatGPT conserve le
   contexte sur 128k tokens. Notre sidebar de conversations (ODAI-UI-002) doit
   permettre de reprendre une analyse complexe jours apres. Le resume automatique
   des conversations longues (> 10 messages) evite la degradation de qualite.

5. **Les raccourcis clavier et slash commands augmentent la retention power users** —
   Claude utilise `/` pour les commandes, ChatGPT a les GPTs. Pour OdooAI :
   `/audit sale`, `/compare v16 v17`, `/explain ir.rule` seraient des accelerateurs.

## Comment ca s'applique a OdooAI

1. **Panneau d'artifacts OdooAI** : Quand l'IA genere une recommandation de
   configuration (ex: droits d'acces, workflows), l'afficher dans un panneau lateral
   avec syntaxe Odoo XML/Python coloree et un bouton "Appliquer dans Odoo".
   Ceci differencie OdooAI d'un simple wrapper ChatGPT.

2. **Slash commands metier** : Implementer 5 commandes de base dans le chat :
   `/audit [module]`, `/compare [v1] [v2]`, `/explain [model]`, `/security [model]`,
   `/optimize [workflow]`. Chaque commande declenche un agent specialise.

3. **Resume automatique** : Apres 8 messages dans une conversation, generer un
   resume contextuel stocke en DB. Utiliser ce resume comme system prompt pour
   les messages suivants, preservant la qualite sans exploser les tokens.

## Ce que je recommande

1. **Sprint 8** : Designer le composant Artifact dans le frontend Next.js.
   Spec : panneau lateral droit, syntax highlighting pour Python/XML/CSV,
   boutons Copy + Download + "Apply to Odoo". Fichier : `web/components/artifact/`.

2. **Sprint 9** : Implementer 3 slash commands prioritaires (`/audit`, `/explain`,
   `/security`) dans le router chat. Chaque commande mappe vers un agent specifique
   du backend. Fichier : `web/components/chat/slash-commands.tsx`.

3. **Sprint 10** : Implementer le resume automatique de conversation cote backend
   avec Haiku (cout minimal). Seuil : 8 messages ou 4000 tokens de contexte.
   Fichier : `odooai/services/conversation_summarizer.py`.

## Sources

1. Nielsen Norman Group — "AI Chat UX Guidelines" (2025) — Patterns de conversation IA
2. Lenny's Newsletter — "How the best AI products handle chat UX" (Jan 2026)
3. Intercom Blog — "Resolution Bot: designing for self-service" (2025)
