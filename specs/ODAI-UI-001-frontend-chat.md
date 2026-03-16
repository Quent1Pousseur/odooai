# ODAI-UI-001 — Frontend Chat + Backend Streaming API

## Status
IN PROGRESS

## Auteur
Frontend Engineer (21) + Chat Engineer (43) + Backend Architect (08)

## Reviewers
CTO (02), CPO (03), Security Architect (07)

## Date
2026-03-18

## Contexte
Le MVP CLI fonctionne (tool-use, connexion live, BA Profiles). Il faut maintenant une interface web pour que les PME puissent utiliser OdooAI sans terminal.

Sprint 2 scope : **chat page uniquement** (pas de landing, billing, multi-user, dashboard).

## Objectif
1. Scaffold Next.js 14 (App Router) + Tailwind + Shadcn/ui
2. Endpoint streaming FastAPI (SSE) pour le chat
3. Chat page avec Vercel AI SDK (`useChat`)
4. Formulaire de connexion Odoo optionnel

## Definition of Done
- [ ] `frontend/` avec Next.js scaffold operationnel (`npm run dev`)
- [ ] Endpoint `POST /api/chat` avec SSE streaming dans FastAPI
- [ ] Chat page : input → question → reponse streamee
- [ ] Sources et tokens affiches apres chaque reponse
- [ ] Disclaimer visible
- [ ] Responsive (mobile-friendly)
- [ ] DA respectee (palette, typo du design brief)
- [ ] Review dans reviews/ODAI-UI-001-review.md
- [ ] Fondateur teste dans le navigateur

## Design

### Architecture
```
Browser (Next.js)
  → useChat() → POST /api/chat
  → FastAPI SSE endpoint
    → Orchestrator.handle_question() (streamable)
    → Tool calls (si connexion Odoo live)
    → Tokens streames au fur et a mesure
  ← StreamingResponse → affiche progressif
```

### Backend : endpoint streaming
```python
# odooai/api/routers/chat.py
@router.post("/api/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    # Stream LLM response via SSE
```

### Frontend : structure
```
frontend/
  app/
    layout.tsx        # Root layout (Inter font, Tailwind)
    page.tsx          # Chat page
    globals.css       # Tailwind + DA colors
  components/
    chat-message.tsx  # Message bubble (user/assistant)
    chat-input.tsx    # Input + send button
  lib/
    api.ts            # API client
  package.json
  tailwind.config.ts
  tsconfig.json
```

### Chat UX (design brief)
- Messages en bulles (user a droite, assistant a gauche)
- Streaming visible (tokens apparaissent progressivement)
- Sources et tokens sous chaque reponse assistant
- Disclaimer en bas de page
- Input fixe en bas avec bouton envoyer

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `frontend/` | Creer — scaffold complet Next.js |
| `odooai/api/routers/chat.py` | Creer — endpoint streaming |
| `odooai/main.py` | Modifier — ajouter chat router + CORS |
| `reviews/ODAI-UI-001-review.md` | Creer |

## Securite
- CORS configure (localhost en dev, domaine en prod)
- Anthropic API key cote serveur uniquement (jamais dans le frontend)
- Credentials Odoo optionnels, transmis via formulaire (HTTPS en prod)
- Review Security Architect (07)

## Dependances
- ODAI-AGENT-003 (DONE) — Tool-use
- ODAI-CORE-004 (DONE) — Connexion live
- Design brief (DONE) — DA et wireframes

## Estimation
L (3-5 jours)
