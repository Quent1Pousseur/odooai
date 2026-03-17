# Learning — AI Safety Lead (33) — Hallucination Detection Techniques in LLM Outputs
## Date : 2026-03-22 (Sprint 5, session 4)
## Duree : 3 heures

## Ce que j'ai appris

1. **Les hallucinations LLM se classent en deux categories** : les hallucinations "intrinseques" (le modele contredit le contexte fourni) et les hallucinations "extrinseques" (le modele invente des informations non presentes dans le contexte). Pour OdooAI, les hallucinations intrinseques sont les plus dangereuses : si le Business Analyst dit "votre champ `x_margin` est de type Float" alors qu'il est de type Monetary, l'utilisateur prend des decisions sur des donnees fausses.

2. **La detection par grounding verification est la plus fiable** : comparer chaque fait de la reponse LLM contre les donnees source (le Knowledge Graph Odoo). Technique : extraire les claims factuelles de la reponse, puis verifier chacune contre la source. Pour OdooAI, chaque mention d'un modele, champ, ou type peut etre verifiee automatiquement contre le Knowledge Graph qui contient les 5514 models et 21013 fields.

3. **Le self-consistency check detecte les hallucinations sans source externe** : on demande au LLM de repondre N fois (N=3) a la meme question, puis on compare les reponses. Les faits qui divergent entre les reponses sont probablement hallucines. Cout : 3x les tokens, donc a utiliser uniquement sur les reponses critiques (recommandations de configuration Odoo, par exemple).

4. **Les metriques de confiance du modele sont un signal faible mais utile** : la log-probability des tokens generes indique la "certitude" du modele. Les tokens avec une faible probabilite dans une assertion factuelle sont suspects. Claude via l'API Anthropic ne fournit pas les logprobs directement, mais on peut demander au modele de scorer sa propre confiance (calibration explicite).

5. **Le "retrieval-augmented verification" combine RAG et detection** : apres la generation, un second appel LLM (plus petit, Haiku) verifie la reponse contre les documents sources. C'est un pattern "generate then verify" qui coute peu en tokens supplementaires et catch les erreurs les plus flagrantes.

## Comment ca s'applique a OdooAI

1. **Implementer un "fact checker" automatique post-generation** : chaque reponse du Business Analyst qui mentionne un modele Odoo, un champ, ou un type est verifiee contre le Knowledge Graph. Si un fait ne matche pas, la reponse est flaggee et le fait incorrect est corrige ou supprime avant d'atteindre l'utilisateur. C'est du code pur (ZERO LLM), coherent avec l'architecture du Guardian.

2. **Ajouter un confidence score visible pour l'utilisateur** : afficher un indicateur de fiabilite dans le chat UI. "Reponse verifiee contre le code source Odoo" (vert) vs "Reponse basee sur des connaissances generales" (orange). Ca gere les attentes et renforce la confiance quand la verification passe.

3. **Utiliser le self-consistency check pour les recommandations critiques** : quand le Business Analyst recommande une modification de workflow ou une configuration Odoo, lancer 3 generations et ne retourner que les recommandations coherentes entre les 3. Le surcout en tokens est justifie par le risque d'une mauvaise recommandation.

## Ce que je recommande

1. **Sprint 6** : Implementer le fact checker ZERO LLM dans `odooai/security/` qui verifie les noms de modeles et champs contre le Knowledge Graph. Interface : `verify_response(response: str, knowledge: KnowledgeGraph) -> VerificationResult`. Cout : 5h.

2. **Sprint 7** : Ajouter le confidence score dans l'API de reponse (`confidence: "verified" | "unverified" | "partial"`) et l'afficher dans le chat UI avec un badge visuel. Cout : 3h.

3. **Sprint 8** : Evaluer le self-consistency check sur 100 questions business reelles. Mesurer le taux de detection vs le surcout en tokens. Decider si on l'active par defaut ou uniquement sur les recommandations critiques.

## Sources

1. Ji et al. — "Survey of Hallucination in Natural Language Generation" (ACM Computing Surveys, 2023) : https://dl.acm.org/doi/10.1145/3571730
2. Manakul et al. — "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection" (EMNLP, 2023) : https://arxiv.org/abs/2303.08896
3. Anthropic — "Reducing Hallucinations in Claude" (2025) : https://docs.anthropic.com/en/docs/build-with-claude/reduce-hallucinations
