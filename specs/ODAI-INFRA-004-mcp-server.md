# ODAI-INFRA-004 — MCP Server

## Status
SPEC READY

## Auteur
Integration Engineer (35) + AI Engineer (09) + CTO (02)

## Date
2026-03-21

## Contexte
Le MCP (Model Context Protocol) permet aux assistants IA (Claude Desktop, etc.) d'utiliser OdooAI comme source de donnees. C'est complementaire au chat web — les power users pourront interroger Odoo depuis Claude directement.

## Scope Sprint 7

### 4 outils MCP
| Outil | Description |
|-------|------------|
| `odooai_analyze` | Analyser la configuration d'une instance Odoo |
| `odooai_ask` | Poser une question et obtenir une reponse BA |
| `odooai_search` | Chercher dans les Knowledge Graphs |
| `odooai_stats` | Statistiques sur une instance (modules, modeles, fields) |

### Transport
- **SSE (Server-Sent Events)** — compatible MCP 1.x
- Endpoint : `POST /mcp/sse`
- Auth : Bearer token (API key OdooAI)

### Architecture
```
Claude Desktop → MCP Protocol → OdooAI MCP Server
                                    ↓
                              Orchestrator (existant)
                                    ↓
                              BA Agent + Tools (existant)
```

Le MCP Server reutilise 100% du pipeline existant. C'est juste un nouveau transport.

### Fichiers
- `odooai/interfaces/mcp/server.py` — MCP server
- `odooai/interfaces/mcp/tools.py` — 4 tool definitions
- `odooai/api/routers/mcp.py` — SSE router

### Dependance
```
pip install mcp
```

## Pre-requis
- Auth utilisateur (JWT/API key)
- Le pipeline chat doit etre stable

## Estimation
M (3 jours)

## Pourquoi Sprint 7 et pas avant
- Le chat web est la priorite (PME ne connaissent pas MCP)
- MCP est pour les power users et integrateurs (Sprint 7+)
- Le pipeline doit etre stable et teste avant d'ajouter un transport
