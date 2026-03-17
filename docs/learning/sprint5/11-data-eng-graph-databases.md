# Learning — Data Eng (11) — Graph Databases for Dependency Graphs

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **Les graph databases modelisent les relations comme des citoyens de premiere classe** : Contrairement a SQL ou les relations passent par des JOIN tables, Neo4j stocke les relations directement comme des edges entre noeud. Une requete "quels modeles dependent de sale.order" traverse le graphe en O(1) par hop au lieu d'un JOIN recursif en O(n*m).

2. **Cypher est le SQL des graphes** : Le langage de requete de Neo4j est declaratif et expressif. `MATCH (m:Model)-[:DEPENDS_ON]->(d:Model) WHERE d.name = "sale.order" RETURN m` retrouve tous les modeles dependants. Les patterns de traversee multi-niveaux sont naturels : `(a)-[:INHERITS*1..3]->(b)` trouve l'heritage sur 3 niveaux.

3. **NetworkX suffit pour les graphes en memoire** : Pour des graphes de taille moderee (< 100K noeuds), la librairie Python NetworkX fonctionne sans infrastructure. Elle offre des algorithmes de centralite, de plus court chemin, de detection de communautes. Pas besoin d'un serveur Neo4j en dev.

4. **La centralite identifie les modeles critiques** : L'algorithme de betweenness centrality mesure combien de chemins passent par un noeud. Dans un graphe de dependances Odoo, les modeles avec haute centralite (res.partner, product.product, account.move) sont les hubs critiques — les modifier impacte tout l'ecosysteme.

5. **Les property graphs ajoutent du contexte aux relations** : Chaque edge peut porter des proprietes. Une relation `DEPENDS_ON` peut avoir `type: "many2one"`, `field_name: "partner_id"`, `required: true`. Cela permet de filtrer les dependances par type et de calculer des metriques de couplage.

## Comment ca s'applique a OdooAI

1. **Visualisation des dependances inter-modules** : Les 1218 modules Odoo ont des dependances complexes. Un graph database permet de repondre instantanement a "si je desinstalle sale_subscription, quels modules cassent ?". C'est une question frequente des clients qui simplifient leur instance.

2. **Navigation intelligente dans les KG** : Quand l'utilisateur pose une question sur `sale.order`, le graphe de dependances permet de remonter automatiquement les modeles lies (`res.partner`, `product.product`, `account.move`) et de les inclure dans le contexte. Cela enrichit les reponses sans que l'utilisateur ait a formuler une requete complexe.

3. **Scoring de complexite des modeles** : En combinant le degree centrality (nombre de relations) avec le nombre de champs et de compute methods, on peut calculer un score de complexite par modele. Les modeles les plus complexes meritent une documentation plus detaillee dans les articles SEO et les reponses assistant.

## Ce que je recommande

1. **Sprint 6** : Creer un script `odooai/services/graph_builder.py` qui charge les KG JSON et construit un graphe NetworkX en memoire. Noeuds = modeles, edges = relations (many2one, one2many, many2many, inherits). Calculer la centralite des 5514 modeles.

2. **Sprint 7** : Ajouter des requetes de traversee dans le `KGRetriever` : "quels modeles sont a 2 hops de sale.order", "quels champs required pointent vers res.partner". Exposer via un endpoint `/api/graph/dependencies/{model_name}`.

3. **Sprint 9** : Evaluer Neo4j AuraDB (cloud) pour la production si le graphe depasse 50K noeuds avec les field-level dependencies. Benchmark NetworkX vs Neo4j sur les requetes de traversee a 3+ niveaux.

## Sources

1. Neo4j Documentation, "Graph Database Concepts" — neo4j.com/docs (2025)
2. Aric Hagberg et al., "NetworkX: Network Analysis in Python" — networkx.org (2024)
3. Ian Robinson et al., "Graph Databases" — O'Reilly Media, 3rd Edition (2024)
