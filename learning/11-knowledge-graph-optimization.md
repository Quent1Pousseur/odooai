# Learning — Data Engineer (11) — Knowledge Graph Optimization
## Date : 2026-03-21
## Duree : 4 heures

## Ce que j'ai appris

### Probleme actuel
Les 1218 KG JSON font ~150MB au total. Quand le LLM a besoin de contexte, on charge un BA Profile entier (~50-100KB) en memoire. C'est inefficace pour les questions multi-domaines.

### Solutions etudiees
1. **Embedding + vector search** : convertir les KG en embeddings, chercher par similarite semantique. Overkill pour le MVP.
2. **Index inverse** : creer un index champ→module→modele pour des lookups O(1). Simple et efficace.
3. **Compression** : gzip les KG JSON. Reduction 70-80% en stockage. Decompression rapide.
4. **Lazy loading** : ne charger que les modeles necessaires, pas tout le KG.

## Comment ca s'applique a OdooAI
- L'index inverse serait utile pour les questions cross-domaine ("ou est defini le champ partner_id ?")
- Le lazy loading reduirait l'usage memoire de 80%
- La compression aiderait au deploiement (Docker image plus legere)

## Ce que je recommande
1. Sprint 5 : index inverse des champs (1 jour de dev)
2. Sprint 6 : lazy loading des KG
3. Plus tard : embeddings si besoin de recherche semantique

## Sources
- Knowledge Graph best practices (Neo4j blog)
- Python gzip + json performance benchmarks
