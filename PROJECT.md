# OdooAI — Description Detaillee du Projet

> Ce document est la BIBLE du projet. Chaque agent doit le lire et le comprendre
> avant de commencer a travailler. Il decrit CE QU'ON CONSTRUIT, POURQUOI, et COMMENT.

---

## 1. Le Probleme

### Le marche Odoo aujourd'hui

Odoo est un ERP open source utilise par des centaines de milliers de PME dans 180+ pays. Il couvre : ventes, achats, stock, comptabilite, CRM, RH, fabrication, projets, helpdesk, e-commerce, point de vente, et bien plus.

**Le probleme fondamental :**

Les PME n'utilisent Odoo qu'a 10-30% de ses capacites.

Pourquoi :
1. **L'outil est trop permissif** — Odoo couvre tellement de cas d'usage que les PME ne savent pas ce qui est possible
2. **La documentation est volumineuse** — personne n'a le temps de la lire
3. **Les consultants coutent cher** — un Business Analyst Odoo facture 150-300€/heure
4. **Les packs de consulting sont limites** — les PME paient pour couvrir leurs besoins primaires et utilisent d'autres outils pour le reste
5. **Il n'y a aucun outil qui explique Odoo a ses utilisateurs** — tu l'utilises ou tu paies quelqu'un pour te l'expliquer

### Les consequences

- Les PME paient des milliers d'euros en consulting pour de la configuration basique
- Apres le consulting, elles ne savent gerer que ce qui a ete installe
- Elles ne connaissent pas le champ des possibles
- Elles utilisent des outils externes pour des besoins qu'Odoo couvre deja nativement
- Elles n'ont personne a qui demander "est-ce qu'Odoo peut faire ca ?"

### Ce qui existe aujourd'hui (et pourquoi ca ne suffit pas)

| Solution | Ce qu'elle fait | Ce qu'elle ne fait PAS |
|----------|----------------|----------------------|
| Consultants Odoo | Configuration sur mesure, formation | Pas scalable, 150-300€/h, limites dans le temps |
| Serveurs MCP Odoo | CRUD basique (search, read, write) | Aucune intelligence business, aucun conseil |
| ChatGPT + doc Odoo | Reponses generiques | Pas connecte a l'instance, pas de contexte, hallucinations |
| Odoo Studio | Customisation low-code | Pas de conseil, pas d'analyse, technique |
| Forums Odoo | Reponses communautaires | Lent, pas personnalise, pas connecte |

**Le trou dans le marche : personne ne transforme la connaissance contenue dans le code source d'Odoo en intelligence business accessible aux PME.**

---

## 2. La Solution : OdooAI

### En une phrase

**OdooAI est un Business Analyst IA qui a lu et compris chaque ligne de code de chaque version d'Odoo, connecte a l'instance du client, capable de conseiller, executer et optimiser.**

### Ce que fait OdooAI

1. **Comprendre le business du client** — Se connecte a l'instance Odoo, detecte les modules installes, analyse la configuration actuelle

2. **Expliquer le champ des possibles** — Parce qu'il a analyse le code source d'Odoo, il sait TOUT ce que chaque module peut faire, y compris ce que le client ne soupconnne pas

3. **Proposer des plans d'action** — Recommandations concretes, etape par etape, adaptees a la configuration actuelle du client

4. **Executer les actions** — CRUD dans Odoo avec double validation : creer des devis, configurer des entrepots, activer des fonctionnalites

5. **Diagnostiquer et debugger** — Identifier les problemes, proposer des fixes, expliquer les erreurs

6. **Optimiser les flux** — Analyser les workflows existants, identifier les inefficacites, proposer des ameliorations

7. **Dire ce qui n'est pas possible** — Et quand ca ne l'est pas, proposer les alternatives : configuration, Studio, module OCA, developpement custom

### Ce qui nous differencie

| Nous | Les autres |
|------|-----------|
| Connaissance extraite du CODE SOURCE | Connaissance de la documentation (incomplete, pas a jour) |
| BA Profiles pre-generes par domaine | Reponses generiques a la volee |
| Expert Profiles avec recettes d'execution | L'utilisateur doit savoir quoi faire |
| Connecte a l'instance live du client | Reponses deconnectees du contexte |
| Double validation avant ecriture | Execution aveugle ou pas d'execution |
| Vision cross-modules (Visionary) | Un module a la fois |
| Faisabilite + alternatives (Feasibility) | "C'est pas possible" sans alternative |

---

## 3. Architecture du Produit

### Vue d'ensemble

Le produit a deux parties : le **moteur d'intelligence** (offline) et le **runtime** (live).

```
PARTIE 1 — MOTEUR D'INTELLIGENCE (offline, run par nous)

  Code source Odoo (fourni par le fondateur a chaque release)
         |
    [Code Analyst]
    Parse Python AST + XML
    Extrait modeles, champs, contraintes, actions, vues, securite
         |
    Knowledge Graphs (JSON structures, versionnes par version Odoo)
         |
    [BA Factory]
    LLM transforme la connaissance technique en expertise metier
         |
    ├── BA Profiles (par domaine fonctionnel)
    |   Scope, recommandations, arbres de decision, limites, audit checklist
    |
    └── Expert Profiles (par domaine fonctionnel)
        Recettes d'execution, CRUD precis, validations, rollback


PARTIE 2 — RUNTIME (live, pour chaque client)

  Client pose une question
         |
    [Orchestrator] — classifie l'intent, route vers le bon agent
         |
    [Security Guardian] — verifie permissions, anonymise les donnees
         |
    [Agent(s) Specialise(s)]
    |   BA Inventory, BA Sales, BA Accounting, etc.
    |   Chaque BA a : son BA Profile + son Expert Profile + acces a l'instance live
    |
    |   Pour les questions business :
    |   [Business Analyst] — consulte le BA Profile + l'instance → recommandation
    |   [Visionary] — si pas de solution directe → combinaison creative
    |   [Feasibility Expert] — faisable en standard/config/Studio/custom ?
    |
    |   Pour l'execution :
    |   [Data Operations] — CRUD Odoo via Expert Profile (recettes precises)
    |   [Schema Intelligence] — introspection live de l'instance
    |
    |   Pour le support :
    |   [Support & Debug] — diagnostic, root cause, fix
    |   [Workflow Optimizer] — analyse flux, propose ameliorations
    |
    [Security Guardian] — anonymise la reponse avant LLM
         |
    [Orchestrator] — compose la reponse finale
         |
    [User Translator] — adapte au niveau technique du client
         |
    Reponse au client
```

### Les agents du PRODUIT (pas l'equipe, le produit)

Ces agents tournent en production et servent les clients :

| Agent Produit | Role | Modele LLM |
|---------------|------|------------|
| **Orchestrator** | Route les requetes, compose les reponses | Haiku (rapide) → Sonnet (si ambigu) |
| **Security Guardian** | Anonymise, audit, permissions | ZERO LLM (logique pure) |
| **BA specialises** | Conseil business par domaine (generes par BA Factory) | Sonnet |
| **Visionary** | Combinaisons creatives cross-modules | Opus (rare) |
| **Feasibility Expert** | Faisabilite : standard/config/Studio/custom | Sonnet |
| **Data Operations** | CRUD Odoo avec double validation | ZERO LLM (pipeline) |
| **Schema Intelligence** | Introspection live de l'instance | Haiku (summarisation) |
| **Support & Debug** | Diagnostic et resolution de problemes | Sonnet |
| **Workflow Optimizer** | Analyse et amelioration des flux | Sonnet |
| **Context Compressor** | Optimisation des tokens | Haiku ou logique pure |
| **Knowledge Manager** | Index et recherche dans les Knowledge Graphs | Logique pure |

---

## 4. Knowledge Graphs — Le Coeur du Moat

### Ce que c'est

Un Knowledge Graph est une representation JSON structuree de TOUT ce qu'un module Odoo peut faire, extrait directement du code source.

### Comment il est genere

1. Le fondateur fournit le code source d'une version Odoo (ex: 17.0)
2. Le Code Analyst parse :
   - `__manifest__.py` → dependances, categorie
   - `models/*.py` → modeles, champs, computed, constraints, onchange, actions
   - `security/*.csv` → access rights
   - `security/*.xml` → record rules
   - `views/*.xml` → structure des vues (form, tree, kanban)
   - `data/*.xml` → donnees par defaut, sequences
   - `wizards/*.py` → TransientModels
   - `controllers/*.py` → routes HTTP
3. Le resultat est stocke en JSON structure, versionne

### Structure d'un Knowledge Graph

```
knowledge_store/
  17.0/
    _index.json           ← Liste des modules, date, hash
    sale/
      manifest.json       ← Metadata (depends, category, description)
      models.json         ← Modeles + champs + types + required + compute
      constraints.json    ← SQL constraints + Python constraints
      actions.json        ← Methodes d'action (buttons)
      wizards.json        ← TransientModels
      views.json          ← Structure des vues
      security.json       ← Groups, ACL, record rules
      menus.json          ← Arborescence des menus
      cross_modules.json  ← Interactions avec d'autres modules
    stock/
      ...
  18.0/
    ...
```

### Exemple concret (extrait de models.json pour sale)

```json
{
  "sale.order": {
    "name": "sale.order",
    "description": "Sales Order",
    "fields": {
      "name": {
        "type": "char",
        "required": true,
        "readonly": true,
        "string": "Order Reference",
        "default": "New"
      },
      "state": {
        "type": "selection",
        "selection": [
          ["draft", "Quotation"],
          ["sent", "Quotation Sent"],
          ["sale", "Sales Order"],
          ["done", "Locked"],
          ["cancel", "Cancelled"]
        ],
        "required": true,
        "default": "draft"
      },
      "partner_id": {
        "type": "many2one",
        "relation": "res.partner",
        "required": true,
        "string": "Customer"
      },
      "amount_total": {
        "type": "monetary",
        "compute": "_compute_amounts",
        "depends": ["order_line.price_subtotal", "order_line.price_tax"],
        "store": true,
        "string": "Total"
      }
    },
    "actions": {
      "action_confirm": {
        "string": "Confirm",
        "type": "method",
        "preconditions": ["state == 'draft' or state == 'sent'"],
        "effects": ["Creates stock.picking if delivery needed", "state → 'sale'"]
      }
    },
    "constraints": {
      "_sql_constraints": [
        ["date_order_conditional_required", "..."]
      ]
    }
  }
}
```

---

## 5. BA Profiles et Expert Profiles

### BA Profile = LE QUOI (intelligence business)

Genere par le BA Factory a partir des Knowledge Graphs. Un par domaine fonctionnel.

**Contenu d'un BA Profile :**
1. **Scope fonctionnel** — tout ce que le domaine permet de faire
2. **Arbres de decision** — "si le client a tel besoin → voici le chemin"
3. **Configurations possibles** — chaque setting, son effet, ses dependances
4. **Combinaisons inter-modules** — "stock + sale = livraison auto"
5. **Limites connues** — ce qui necessite du dev custom
6. **Pieges et gotchas** — extraits des contraintes dans le code
7. **Audit checklist** — questions a poser pour evaluer l'usage du client

**Domaines fonctionnels (pas 1:1 avec les modules) :**

| Domaine | Modules couverts |
|---------|-----------------|
| Sales & CRM | sale, crm, sale_management, sale_subscription |
| Supply Chain | stock, purchase, stock_landed_costs, delivery |
| Manufacturing | mrp, mrp_workorder, quality, quality_control |
| Accounting & Finance | account, account_payment, account_bank_statement |
| HR & Payroll | hr, hr_contract, hr_payslip, hr_expense, hr_holidays |
| Project & Services | project, hr_timesheet, planning |
| Helpdesk | helpdesk, rating |
| E-commerce | website_sale, website, payment |
| POS | point_of_sale |

### Expert Profile = LE COMMENT (intelligence d'execution)

Genere par le BA Factory. Contient les recettes d'execution exactes.

**Contenu d'un Expert Profile :**
1. **Operations CRUD par entite** — champs requis, defaults, precautions
2. **Recettes d'execution pas-a-pas** — quels appels, quel ordre, quelles valeurs
3. **Chaines de dependances** — "si tu fais X, Odoo fait automatiquement Y"
4. **Validations pre-execution** — "avant d'appeler Z, verifie que..."
5. **Patterns d'erreur connus** — "si tu as cette erreur, voici pourquoi"
6. **Rollback procedures** — comment annuler chaque action

**Exemple de recette :**
```json
{
  "recipe_id": "stock_enable_3step_reception",
  "name": "Activer reception 3 etapes",
  "steps": [
    {
      "order": 1,
      "operation": "search_read",
      "model": "stock.warehouse",
      "domain": [],
      "fields": ["id", "name", "reception_steps"]
    },
    {
      "order": 2,
      "operation": "write",
      "model": "stock.warehouse",
      "values": {"reception_steps": "three_steps"},
      "precondition": "reception_steps != 'three_steps'"
    },
    {
      "order": 3,
      "operation": "search_read",
      "model": "stock.picking.type",
      "domain": [["warehouse_id","=","$step1.id"], ["code","=","internal"]],
      "fields": ["id", "name"],
      "verify": "len(result) >= 1"
    }
  ],
  "rollback": {
    "operation": "write",
    "model": "stock.warehouse",
    "values": {"reception_steps": "one_step"}
  }
}
```

---

## 6. Securite — Priorite Absolue

### Principe : les donnees entreprise ne touchent JAMAIS le LLM en brut si elles sont sensibles

### Pipeline de securite

```
Requete client
    → [Orchestrator] classifie
    → [Security Guardian] verifie permissions
    → [Agent] a besoin de donnees Odoo
    → [Data Operations] appelle Odoo
    → Reponse Odoo brute
    → [Security Guardian] INTERCEPTE :
        1. Classification du modele (BLOCKED / SENSITIVE / STANDARD / OPEN)
        2. Resolution de la politique (champs autorises / interdits / anonymises)
        3. Anonymisation field-level :
           - Montants → arrondi centaine (45 780€ → 45 800€)
           - Emails → j***@domain.com
           - Noms → J*** D***
           - Confidentiel → supprime completement
    → Donnees sanitisees envoyees au LLM
```

### Modeles bloques (JAMAIS exposes)
`ir.rule`, `ir.model.access`, `res.users` (passwords), `res.groups`, `ir.config_parameter`

### Credentials
- Encryptees AES-256-GCM au repos
- Decryptees UNIQUEMENT pendant l'appel Odoo API (millisecondes)
- Jamais loggees, jamais dans le contexte LLM, jamais dans les messages d'erreur

### Operations d'ecriture
- Double validation utilisateur OBLIGATOIRE (modal avant/apres)
- Capture de l'etat precedent avant chaque write (rollback possible)
- JAMAIS de `unlink` (suppression) — toujours archiver
- JAMAIS de `sudo` — pas d'elevation de privileges
- Audit log de chaque operation

---

## 7. Optimisation des Tokens

### Architecture 3+2

| Couche | Strategie | Cout runtime |
|--------|-----------|--------------|
| L1 | Hints dans les descriptions de tools | 0 tokens |
| L2 | Top 20 gotchas dans le system prompt | ~500 tokens fixes |
| L3 | BA/Expert Profiles charges on-demand | Variable, seulement quand necessaire |
| +1 | Field scoring : auto-select top 15 champs par modele | -85% donnees |
| +2 | Dynamic tool loading : seuls les tools pertinents aux modules installes | -800 tokens/requete |

### Cout estime par requete

| Type de requete | Cout estime |
|----------------|------------|
| Simple (data lookup) | ~$0.002 |
| Moyen (conseil config) | ~$0.034 |
| Complexe (plan multi-module) | ~$0.17 |
| Maximal (Visionary, Opus) | ~$0.30 |
| **Moyenne ponderee** | **~$0.031** |

### Selection de modele par tache

| Tache | Modele LLM | Justification |
|-------|------------|---------------|
| Classification d'intent | Haiku | Rapide, pas cher, haute precision pour la classification |
| Summarisation schema | Haiku | Structure, pas de creativite necessaire |
| Analyse business | Sonnet | Sweet spot qualite/cout |
| Configuration guidance | Sonnet | Raisonnement complexe mais pas maximal |
| Cross-module planning | Opus | Raisonnement profond, rare (< 2% des requetes) |
| Securite | ZERO LLM | Logique deterministe, jamais de LLM pour la securite |

---

## 8. Connexion Odoo

### Protocoles supportes
- **XML-RPC** : Odoo 17.0, 18.0 (protocole historique)
- **JSON-RPC 2.0** : Odoo 19.0+ (protocole moderne)
- Detection automatique de la version a la premiere connexion

### Operations supportees
| Operation | Description |
|-----------|------------|
| `authenticate` | Connexion et detection des droits utilisateur |
| `search_read` | Rechercher et lire des records |
| `read_group` | Aggregation (GROUP BY) |
| `search_count` | Compter les records |
| `name_search` | Recherche par nom d'affichage |
| `create` | Creer un record (avec double validation) |
| `write` | Modifier un record (avec double validation) |
| `execute` | Appeler une methode (confirm, validate, etc.) |
| `get_model_fields` | Introspection des champs d'un modele |
| `check_access_rights` | Verifier les droits avant chaque operation |

### Ce qui est INTERDIT
- `unlink` → toujours archiver (`write({'active': False})`)
- `sudo` → jamais d'elevation de privileges
- Acces aux modeles BLOCKED → rejet immediat

---

## 9. Stack Technique

### Backend
| Composant | Technologie |
|-----------|------------|
| Langage | Python 3.11+ |
| Framework API | FastAPI |
| Validation | Pydantic |
| ORM / DB | SQLAlchemy + SQLite (MVP) → PostgreSQL (prod) |
| Cache | Redis |
| HTTP client | httpx (async, connection pooling) |
| Odoo XML-RPC | xmlrpc.client (wrape en asyncio.to_thread) |
| Encryption | cryptography (AES-256-GCM) |
| Logging | structlog (structured, JSON) |
| LLM | anthropic SDK (LLM-agnostic via interface abstraite) |

### Frontend
| Composant | Technologie |
|-----------|------------|
| Framework | Next.js 14+ (App Router) |
| Langage | TypeScript (strict) |
| Styling | Tailwind CSS |
| Composants | Shadcn/ui |
| Chat streaming | Vercel AI SDK |
| State | React Server Components + SWR |

### Mobile
| Composant | Technologie |
|-----------|------------|
| Framework | React Native |
| Platforms | iOS + Android (un seul codebase) |

### Infrastructure
| Composant | Technologie |
|-----------|------------|
| Containers | Docker |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |
| Tracing | OpenTelemetry |
| CDN | Cloudflare |
| DNS / DDoS | Cloudflare |

---

## 10. Modele de Deployment

### SaaS (Phase 1)
```
Internet → Cloudflare (CDN + DDoS + WAF)
         → Load Balancer (TLS termination)
         → App containers (FastAPI, stateless, auto-scaled)
            → Redis (cache, sessions)
            → PostgreSQL (donnees)
            → Claude API (LLM, externe)
            → Odoo client (API, externe)
```

### Self-Hosted (Phase 4)
```
docker-compose up -d
  → app (OdooAI)
  → redis
  → postgresql (ou sqlite en mode simple)

Le client fournit :
  → Sa cle API LLM (Claude, OpenAI, ou local)
  → Sa connexion Odoo
  → C'est tout.
```

---

## 11. Business Model

### Plans (draft, a valider par CFO + SaaS Architect + Sales)

| Plan | Prix | Connexions | Requetes/mois | Features |
|------|------|-----------|---------------|----------|
| **Starter** | €49/mois | 1 | 100 | BA Profiles basiques, lecture seule |
| **Professional** | €149/mois | 1 | 500 | Tous BA + Expert Profiles, lecture + ecriture |
| **Enterprise** | €399/mois | 3 | Illimite* | Tout + Visionary + audit complet + support prioritaire |

*Illimite = fair use cap a definir avec le CFO

### Marges estimees (voir CFO profile pour le detail)
- Starter : ~90% marge brute
- Professional : ~87%
- Enterprise : ~81%
- Break-even : ~6 clients payants

---

## 12. Versions Odoo Supportees

| Version | Protocole | Status |
|---------|-----------|--------|
| 17.0 | XML-RPC | Supporte (MVP) |
| 18.0 | XML-RPC | Supporte |
| 19.0+ | JSON-RPC 2.0 | Supporte |
| < 17.0 | — | Non supporte |

Community ET Enterprise sont supportes. Les differences Community/Enterprise sont documentees dans les BA Profiles (certaines features n'existent qu'en Enterprise).

---

## 13. Ce Qui Rend le Projet Perenne

1. **La connaissance s'accumule** — a chaque version Odoo, les Knowledge Graphs s'enrichissent. Plus le temps passe, plus le produit est intelligent. Un concurrent qui arrive dans 2 ans a 2 ans de retard.

2. **LLM-agnostic** — l'intelligence est dans les Knowledge Graphs + les agents, pas dans un modele specifique. Interface abstraite : si demain Llama 5 est meilleur que Claude, on switch.

3. **Closed source** — le code est protege. La connaissance structuree (BA/Expert Profiles) est le vrai actif.

4. **SaaS → self-hosted** — architecture modulaire qui fonctionne dans les deux modes.

5. **Effet compose** — chaque client qui utilise le produit enrichit la comprehension des patterns d'usage courants.

6. **Ecosystem Odoo** — 600+ partenaires integrateurs potentiels comme canal de distribution.
