# Review — ODAI-UI-001 (Frontend Chat + Backend Streaming)

## Reviewer : Security Architect (07) + CTO (02)
## Date : 2026-03-18
## Status : APPROVED avec notes

---

## Verdict
**Go pour MVP.** L'architecture est correcte. Notes pour Sprint 3.

## Points verifies

### Backend streaming
- SSE via FastAPI StreamingResponse ✅
- CORS configure (localhost:3000 seulement) ✅
- API key Anthropic cote serveur uniquement ✅
- Erreurs sanitisees (pas de leak) ✅

### Frontend
- Next.js 14 App Router ✅
- DA respectee (couleurs, typo) ✅
- Disclaimer visible ✅
- Responsive layout ✅

## Notes pour Sprint 3
1. **Streaming pas natif** : on chunk le texte apres reception (faux streaming). Le vrai streaming LLM (token par token) necessitera le streaming Anthropic SDK.
2. **Pas de conversation persistante** : chaque question est independante, pas d'historique.
3. **Pas d'auth frontend** : n'importe qui sur localhost peut utiliser le chat. A securiser avant deploiement.
4. **Odoo credentials dans le body** : en prod il faudra un formulaire HTTPS + session.
