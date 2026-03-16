# OdooAI — Glossary

## Termes Produit

| Terme | Definition |
|-------|-----------|
| **OdooAI** | Notre produit. Un Business Analyst IA qui a lu chaque ligne de code d'Odoo et aide les PME a exploiter Odoo a 100%. |
| **Knowledge Graph** | Representation structuree (JSON) de tout ce qu'un module Odoo peut faire. Extrait du code source par le Code Analyst. Contient : modeles, champs, contraintes, actions, vues, securite. |
| **BA Profile** | Profil de Business Analyst specialise dans un domaine fonctionnel. Genere par le BA Factory a partir des Knowledge Graphs. Contient : scope fonctionnel, arbres de decision, recommandations, limites, audit checklist. |
| **Expert Profile** | Profil d'execution technique. Contient les "recettes" exactes : quels appels API faire, dans quel ordre, avec quelles valeurs, comment verifier, comment rollback. |
| **BA Factory** | Le processus (offline) qui transforme les Knowledge Graphs techniques en BA Profiles (business) et Expert Profiles (execution). Utilise un LLM pour la transformation. |
| **Code Analyst** | Le processus (offline) qui parse le code source Odoo et extrait les Knowledge Graphs. Analyse Python AST + XML. |
| **Module Knowledge Graph** | Knowledge Graph specifique a un module Odoo (ex: stock, sale, account). |
| **Triangle d'Or** | Pattern de collaboration : Code Analyst + Business Analyst + Feasibility Expert collaborent systematiquement sur chaque question business. |
| **Double Validation** | Mecanisme de securite : toute ecriture dans Odoo necessite une confirmation explicite de l'utilisateur avant execution. |
| **Aggregation Forcing** | Securite : quand un utilisateur demande trop de records sur un modele sensible, le systeme retourne automatiquement un resume (read_group) au lieu des records individuels. |
| **Field Scoring** | Algorithme qui selectionne automatiquement les 15 champs les plus pertinents d'un modele Odoo, reduisant les tokens de 85%. |

## Termes Techniques

| Terme | Definition |
|-------|-----------|
| **XML-RPC** | Protocole de communication avec Odoo 17/18. Plus ancien, plus lent. |
| **JSON-RPC 2.0** | Protocole de communication avec Odoo 19+. Plus moderne, plus rapide. |
| **MCP** | Model Context Protocol. Standard ouvert pour connecter des LLM a des outils. Phase 2 du produit. |
| **LLM** | Large Language Model (Claude, GPT, etc.). Le cerveau IA derriere les agents. |
| **Token** | Unite de mesure du texte pour les LLM. ~4 caracteres = 1 token. Le cout est facture par million de tokens. |
| **System Prompt** | Instructions donnees au LLM pour definir sa personnalite et ses regles. Chaque agent produit a un system prompt unique. |
| **Eval** | Test automatise qui verifie la qualite des reponses du LLM. Suite de questions avec reponses attendues. |
| **Hallucination** | Quand le LLM invente une information qui n'existe pas. Ennemi #1 du produit. |
| **Prompt Injection** | Attaque ou des donnees malicieuses essaient de manipuler le LLM. |
| **Frozen Dataclass** | Objet Python immutable. Utilisé pour les donnees qui circulent entre agents (securite). |

## Termes Business

| Terme | Definition |
|-------|-----------|
| **PME** | Petites et Moyennes Entreprises. Notre cible principale. |
| **MRR** | Monthly Recurring Revenue. Revenu mensuel recurrent. |
| **ARR** | Annual Recurring Revenue. MRR x 12. |
| **ARPU** | Average Revenue Per User. Revenu moyen par client. |
| **LTV** | Lifetime Value. Revenu total genere par un client pendant toute sa relation avec nous. |
| **CAC** | Customer Acquisition Cost. Cout pour acquerir un nouveau client. |
| **Churn** | Taux de clients qui annulent leur abonnement. |
| **NRR** | Net Revenue Retention. Revenue retention incluant expansion. Cible > 100%. |
| **CSAT** | Customer Satisfaction Score. Mesure de satisfaction client. |

## Termes Securite

| Terme | Definition |
|-------|-----------|
| **BLOCKED** | Categorie de modeles Odoo JAMAIS exposes (ir.rule, res.users, etc.). |
| **SENSITIVE** | Categorie de modeles soumis a anonymisation (account.*, hr.*). |
| **STANDARD** | Categorie par defaut pour les modeles business normaux. |
| **OPEN** | Categorie de modeles reference sans restriction (product.*, res.currency). |
| **Anonymisation** | Remplacement des donnees sensibles avant envoi au LLM (masquage emails, arrondis montants). |
| **AES-256-GCM** | Algorithme d'encryption utilise pour les credentials Odoo stockees en base. |

## Termes Process

| Terme | Definition |
|-------|-----------|
| **Spec** | Document de specification identifie par un ODAI-XXX. Redige AVANT le code. |
| **ADR** | Architecture Decision Record. Document qui explique pourquoi une decision technique a ete prise. |
| **VETO** | Droit de bloquer une decision. Remonte au fondateur pour arbitrage. |
| **DOD** | Definition of Done. Checklist qu'une tache doit remplir pour etre consideree terminee. |
| **Sprint** | Periode de 2 semaines avec des objectifs definis. |
| **SLA** | Service Level Agreement. Temps de reponse garanti au support client. |
