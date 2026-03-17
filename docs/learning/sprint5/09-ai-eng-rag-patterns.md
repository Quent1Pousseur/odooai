# Learning — AI Eng (09) — RAG Patterns for Knowledge Graph-Based Responses

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **RAG ajoute du contexte factuel au LLM avant generation** : Retrieval Augmented Generation fonctionne en 3 etapes : (1) la question utilisateur est transformee en query de recherche, (2) les documents pertinents sont recuperes depuis un store, (3) ces documents sont injectes dans le prompt comme contexte avant que le LLM genere sa reponse. Cela elimine les hallucinations sur les donnees factuelles.

2. **Le chunking est critique pour la qualite du retrieval** : Decouper un Knowledge Graph en chunks trop larges dilue la pertinence, trop petits perd le contexte. Pour des donnees structurees comme nos KG Odoo (modeles, champs, relations), le chunk optimal est le modele complet avec ses champs et relations directes — environ 500-1500 tokens par chunk.

3. **Le re-ranking ameliore drastiquement la precision** : Un premier retrieval (BM25 ou cosine similarity) retourne les top-20 candidats. Un re-ranker (cross-encoder ou LLM-based) re-evalue chaque candidat par rapport a la question originale pour ne garder que les top-5. Le gain de precision est typiquement de 15-30% sur les benchmarks.

4. **Les metadata filters reduisent l'espace de recherche** : Avant de chercher dans tout l'index, on filtre par metadata : module Odoo, type de modele (transactionnel, config, technique), categorie de question (comment faire, pourquoi, reference). Cela accelere le retrieval et ameliore la pertinence.

5. **Le hybrid search combine lexical et semantique** : BM25 excelle sur les termes exacts (noms de champs comme `payment_term_id`, noms de modeles comme `sale.order`). La recherche semantique excelle sur l'intention ("comment automatiser les devis"). Combiner les deux avec un score fusionne (Reciprocal Rank Fusion) donne les meilleurs resultats.

## Comment ca s'applique a OdooAI

1. **Injection de KG dans le contexte LLM** : Quand un utilisateur demande "comment fonctionne la facturation dans Odoo", le RAG pipeline cherche dans les KG les modeles `account.move`, `account.move.line`, `account.payment` et injecte les champs, compute methods et relations dans le prompt. Le LLM repond avec des donnees exactes du code source, pas de la doc approximative.

2. **Scoring de pertinence par module** : Le `field_scorer` existant peut servir de signal pour le re-ranking. Les champs avec un score eleve (business-critical, souvent utilises) sont priorises dans le contexte. Cela optimise l'utilisation des tokens : on envoie les champs les plus pertinents, pas tous les 56 champs de `sale.order`.

3. **Reduction des couts tokens** : Avec un bon RAG, on injecte seulement 2000-3000 tokens de contexte KG au lieu de 15000. L'architecture 3+2 tokens de Phase 4 beneficie directement de cette optimisation — chaque question coute moins cher tout en etant plus precise.

## Ce que je recommande

1. **Sprint 6** : Implementer un `KGRetriever` dans `odooai/services/retrieval.py` qui indexe les KG par modele et par champ. Premier retrieval en BM25 sur les noms de modeles/champs. Interface `IRetriever` dans les ports pour rester LLM-agnostic.

2. **Sprint 7** : Ajouter le re-ranking basique utilisant le field_scorer comme signal. Les champs avec score > 0.7 sont priorises. Mesurer le gain de pertinence sur un jeu de 50 questions Odoo frequentes.

3. **Sprint 8** : Implementer le hybrid search (BM25 + embeddings) avec Reciprocal Rank Fusion. Evaluer si les embeddings justifient le cout additionnel par rapport au BM25 + metadata filters seul.

## Sources

1. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — NeurIPS 2020 (Meta AI Research)
2. LlamaIndex Documentation, "Building RAG over Structured Data" — docs.llamaindex.ai (2025)
3. Anthropic Cookbook, "RAG Best Practices with Claude" — github.com/anthropics/anthropic-cookbook (2025)
