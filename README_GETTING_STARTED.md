# OdooAI — Getting Started

> De l'installation au premier chat en 5 minutes.

## Prerequis

- Python 3.11+
- Node.js 18+ (pour le frontend)
- Une cle API Anthropic ([console.anthropic.com](https://console.anthropic.com))
- (Optionnel) Une instance Odoo 17/18/19 accessible

## 1. Installation

```bash
git clone git@github.com:VOTRE_USER/odooai.git
cd odooai

# Backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Frontend
cd frontend
npm install
cd ..
```

## 2. Configuration

```bash
cp .env.example .env
# Editez .env et ajoutez votre cle Anthropic :
# ANTHROPIC_API_KEY=sk-ant-...
```

## 3. Analyser Odoo (une seule fois)

Si vous avez le code source Odoo :

```bash
# Analyser tous les modules
odooai analyze-all /chemin/vers/odoo-17.0/addons --save --version-tag 17.0

# Generer les 9 BA Profiles
for domain in sales_crm supply_chain manufacturing accounting hr_payroll project_services helpdesk ecommerce pos; do
  odooai generate-ba $domain --save
done
```

## 4. Utiliser le chat CLI

```bash
# Sans connexion Odoo (utilise les BA Profiles)
odooai chat

# Avec connexion a votre instance Odoo
odooai chat --url http://localhost:8069 --db ma-base
```

## 5. Utiliser le chat Web

```bash
# Terminal 1 : backend
odooai serve

# Terminal 2 : frontend
cd frontend && npm run dev

# Ouvrir http://localhost:3000
```

## Commandes disponibles

| Commande | Description |
|----------|------------|
| `odooai analyze <path>` | Analyser un module Odoo |
| `odooai analyze-all <path>` | Analyser tous les modules |
| `odooai check-kg <module>` | Inspecter un Knowledge Graph |
| `odooai generate-ba <domain>` | Generer un BA Profile |
| `odooai chat` | Chat CLI |
| `odooai serve` | Lancer le serveur API |

## Qualite

```bash
make check    # Lint + types + tests + security
make test     # Tests uniquement
make lint     # Ruff lint + format
make typecheck # mypy --strict
```

## Structure du projet

```
odooai/             # Backend Python
  agents/           # Orchestrator, BA Agent, tool-use
  knowledge/        # Knowledge Graphs, Code Analyst, BA Factory
  security/         # Guardian, anonymizer, audit
  infrastructure/   # Odoo client, cache, crypto
  api/              # FastAPI routers (health, chat)
frontend/           # Next.js 14 chat interface
knowledge_store/    # Generated KGs and BA Profiles (gitignored)
specs/              # Specifications (ODAI-XXX)
reviews/            # Security reviews
meetings/           # Daily standups, kick-offs, retros
business/           # Pitch, personas, cost model, legal
```

## Questions ?

Consultez [PROJECT.md](PROJECT.md) pour la vision complete du projet.
