# ODAI-CORE-005 — Conversations Persistantes (DB)

## Status
IN PROGRESS

## Auteur
Chat Engineer (43) + DBA (30) + Backend Architect (08)

## Reviewers
CTO (02), Security Architect (07)

## Date
2026-03-18

## Contexte
Chaque question est independante — pas d'historique. L'utilisateur ne peut pas reprendre une conversation ni voir ses echanges precedents. Il faut persister les messages en DB.

## Objectif
1. SQLAlchemy models : Conversation + Message
2. API endpoints : creer, lister, reprendre, envoyer message
3. Historique envoye au LLM a chaque question (context window)
4. Frontend : afficher l'historique de la conversation courante

## Definition of Done
- [ ] Models SQLAlchemy (Conversation, Message) avec migrations
- [ ] Endpoint POST /api/conversations (creer)
- [ ] Endpoint GET /api/conversations (lister)
- [ ] Endpoint GET /api/conversations/{id}/messages (historique)
- [ ] POST /api/chat envoie l'historique au LLM
- [ ] Frontend charge et affiche l'historique
- [ ] SQLite en dev (aiosqlite)
- [ ] Review dans reviews/
- [ ] make check passe

## Design

### Models
```python
class Conversation(Base):
    id: UUID
    title: str  # Auto-genere a partir du premier message
    domain_id: str  # Domaine detecte
    created_at: datetime
    updated_at: datetime

class Message(Base):
    id: UUID
    conversation_id: FK → Conversation
    role: str  # "user" | "assistant"
    content: str
    tokens: int
    created_at: datetime
```

### API
```
POST /api/conversations        → {id, title}
GET  /api/conversations        → [{id, title, updated_at}]
GET  /api/conversations/{id}/messages → [{role, content, created_at}]
POST /api/chat                 → SSE (modifie: conversation_id optionnel)
```

### Context window
Les N derniers messages sont envoyes au LLM. Si la conversation depasse le contexte, les vieux messages sont resumes (Sprint 4).

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `odooai/infrastructure/db/models.py` | Creer |
| `odooai/infrastructure/db/database.py` | Remplir le stub |
| `odooai/api/routers/conversations.py` | Creer |
| `odooai/api/routers/chat.py` | Modifier (conversation_id) |
| `odooai/agents/_streaming.py` | Modifier (historique) |
| `frontend/app/page.tsx` | Modifier (sidebar + historique) |

## Securite
- Les conversations sont isolees (pas de multi-user en Sprint 3)
- Les messages contiennent des reponses anonymisees (pas de donnees brutes)

## Dependances
- ODAI-AGENT-004 (DONE) — Streaming

## Estimation
M-L (2-3 sessions)
