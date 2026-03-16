# OdooAI — Modele de Cout LLM v1

## Auteur : CFO (15) + AI Engineer (09)
## Date : 2026-03-16

---

## 1. Couts Anthropic (prix public, mars 2026)

| Modele | Input ($/1M tokens) | Output ($/1M tokens) | Usage OdooAI |
|--------|--------------------|--------------------|-------------|
| Haiku 4.5 | $1.00 | $5.00 | Classification, summarisation |
| Sonnet 4.6 | $3.00 | $15.00 | Analyse business, configuration |
| Opus 4.6 | $15.00 | $75.00 | Cross-module, rare (<2%) |

## 2. Estimation par type de requete

### Simple (data lookup, classification)
- Modele : Haiku
- Input : ~800 tokens (system prompt 500 + question 200 + context 100)
- Output : ~200 tokens
- **Cout : $0.002**

### Moyen (conseil configuration, analyse business)
- Modele : Sonnet
- Input : ~4000 tokens (system prompt 500 + BA Profile 2000 + question 500 + context Odoo 1000)
- Output : ~1000 tokens
- **Cout : $0.027**

### Complexe (plan multi-module, diagnostic)
- Modele : Sonnet
- Input : ~8000 tokens (system prompt 500 + 2 BA Profiles 4000 + question 500 + context 3000)
- Output : ~2000 tokens
- **Cout : $0.054**

### Maximal (Visionary cross-module, Opus)
- Modele : Opus
- Input : ~10000 tokens
- Output : ~3000 tokens
- **Cout : $0.375**

### Moyenne ponderee
| Type | % requetes | Cout | Cout pondere |
|------|-----------|------|-------------|
| Simple | 50% | $0.002 | $0.001 |
| Moyen | 35% | $0.027 | $0.009 |
| Complexe | 13% | $0.054 | $0.007 |
| Maximal | 2% | $0.375 | $0.008 |
| **Total** | **100%** | | **$0.025** |

> **Revision vs PROJECT.md** : $0.025 vs $0.031 estime. Legèrement mieux grace a l'architecture 3+2 (field scoring, dynamic tools).

## 3. Cout de generation des Knowledge Graphs

### Generation offline (une seule fois par version Odoo)
- Code Analyst (AST parsing) : **$0** — pas de LLM, logique pure
- BA Profiles (via BA Factory, Sprint 2) : estimation
  - ~1218 modules * ~2000 tokens input * Sonnet = ~2.4M tokens input
  - ~1218 modules * ~1000 tokens output = ~1.2M tokens output
  - **Cout total generation BA Profiles : ~$25**
- Expert Profiles : estimation similaire, ~$25
- **Total generation offline : ~$50 par version Odoo**

> **AI Engineer (09)** : "On ne genere pas un BA Profile par module. On genere par domaine fonctionnel (9 domaines). Ca reduit a ~9 * 5000 tokens = 45K tokens. Cout < $5."
>
> **CFO (15)** : "Beaucoup mieux. $5 one-time vs $50. La strategie par domaine est la bonne."

## 4. Marges par plan

| Plan | Prix | Requetes/mois | Cout LLM/mois | Marge brute |
|------|------|--------------|--------------|------------|
| Starter (€49) | €49 | 100 | $2.50 (~€2.30) | **95%** |
| Professional (€149) | €149 | 500 | $12.50 (~€11.50) | **92%** |
| Enterprise (€399) | €399 | 2000* | $50.00 (~€46) | **88%** |

*Fair use cap a 2000 requetes/mois pour Enterprise

> **CFO (15)** : "Les marges sont excellentes. Meme le plan Enterprise a 88% de marge brute. Le break-even est a ~4 clients Starter. C'est viable."

## 5. Couts infrastructure mensuels (Phase 1)

| Poste | Cout/mois | Notes |
|-------|-----------|-------|
| Hebergement (VPS) | ~€20 | DigitalOcean/Hetzner, 1 instance |
| PostgreSQL managed | €0 | SQLite en Phase 1 |
| Redis | €0 | In-memory en Phase 1 |
| Domain + DNS | ~€2 | Cloudflare free tier |
| GitHub | €0 | Free private repos |
| Monitoring | €0 | Structlog + self-hosted |
| **Total infra** | **~€22/mois** | |

## 6. Break-even

| Scenario | Clients necessaires | MRR |
|----------|-------------------|-----|
| Seulement Starter | 1 client (€49 > €22 infra) | €49 |
| Mix (5 Starter + 2 Pro) | 7 clients | €543 |
| Cible Phase 2 (20 clients) | 20 mix | ~€2000 |

> **Vendor Manager (40)** : "A ce volume, on est au prix public Anthropic. Pas de negociation possible avant ~$500/mois de consommation. Plan B : OpenAI ou Mistral si Anthropic augmente."

## 7. Risques financiers

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|-----------|
| Anthropic +50% prix | Moyen | Marge -5 a -10 points | ILLMProvider agnostic, switch possible |
| Requetes abusives (fair use) | Moyen | Cout explose sur Enterprise | Rate limiting + quota par plan |
| Generation BA Profiles plus couteuse que prevu | Faible | +$50 one-time | Strategie par domaine (9 vs 1218) |

---

> **Decision CFO** : Le modele est viable. Break-even a 1 client Starter pour couvrir l'infra. Marges > 88% sur tous les plans. Feu vert financier pour continuer.
