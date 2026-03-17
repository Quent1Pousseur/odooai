# Learning — Prompt Eng (25) — Chain-of-Thought Prompting for Complex Odoo Questions

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **Chain-of-thought (CoT) force le LLM a raisonner etape par etape** : Au lieu de demander directement "quel modele gere la facturation Odoo", on ajoute "raisonne etape par etape" ou on fournit un exemple avec raisonnement. Le LLM decompose alors : (1) identifier le domaine (comptabilite), (2) trouver le modele principal (account.move), (3) lister les sous-modeles (account.move.line), (4) synthetiser. La precision augmente de 20-40% sur les questions complexes.

2. **Le few-shot CoT est plus fiable que le zero-shot** : Donner 2-3 exemples de raisonnement complet avant la question cible guide le LLM dans le format et la profondeur attendus. Pour Odoo, un exemple montre comment naviguer de la question business ("comment gerer les avoirs") vers les modeles techniques (account.move avec type=out_refund).

3. **Le self-consistency ameliore la fiabilite** : On genere 3-5 raisonnements CoT pour la meme question (avec temperature > 0), puis on prend la reponse majoritaire. Si 4 sur 5 raisonnements concluent que le champ `state` de sale.order a 4 valeurs, c'est probablement correct. Cela reduit les erreurs uniques de raisonnement.

4. **Les structured prompts combinent CoT et format** : On peut demander au LLM de raisonner dans un format structure : `<thinking>...</thinking>` pour le raisonnement interne, puis `<answer>...</answer>` pour la reponse finale. Le raisonnement est cachable/loggable pour debug, la reponse est propre pour l'utilisateur.

5. **Le tree-of-thought etend CoT pour les questions a branches** : Pour les questions complexes ("compare la facturation Odoo Community vs Enterprise"), le LLM explore plusieurs branches de raisonnement en parallele, evalue chaque branche, et converge vers la meilleure synthese. Plus couteux en tokens mais nettement meilleur pour les analyses comparatives.

## Comment ca s'applique a OdooAI

1. **Reponses fiables sur les questions multi-modules** : Quand un utilisateur demande "comment fonctionne le flux vente > livraison > facturation", le CoT decompose en etapes : (1) sale.order confirme, (2) stock.picking genere, (3) account.move cree via `_create_invoices()`. Le raisonnement explicite evite de confondre les etapes ou d'oublier des modeles intermediaires.

2. **System prompts des agents avec CoT integre** : Les 43 agents OdooAI peuvent avoir des system prompts qui incluent des exemples CoT specifiques a leur domaine. L'agent "Functional Analyst" a des exemples de raisonnement business > technique. L'agent "Security Analyst" a des exemples de raisonnement menace > impact > mitigation.

3. **Optimisation tokens avec extended thinking** : L'API Claude supporte le extended thinking nativement. On peut activer le thinking pour les questions complexes (detectees par le nombre de modeles impliques > 3) et le desactiver pour les questions simples. Cela optimise le budget tokens de l'architecture 3+2.

## Ce que je recommande

1. **Sprint 6** : Creer une librairie de 20 exemples CoT dans `odooai/prompts/cot_examples/` couvrant les 5 domaines les plus demandes : vente, achat, comptabilite, stock, CRM. Chaque exemple montre le raisonnement complet de la question business vers la reponse technique.

2. **Sprint 7** : Implementer la detection automatique de complexite dans le prompt router. Questions simples (1 modele) = reponse directe Haiku. Questions complexes (3+ modeles) = CoT avec Sonnet. Questions d'analyse (comparaison, audit) = extended thinking avec Opus.

3. **Sprint 8** : A/B tester CoT vs reponse directe sur 100 questions reelles. Mesurer la precision (validation manuelle), le cout tokens, et la satisfaction utilisateur. Objectif : +25% precision pour +40% tokens max.

## Sources

1. Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" — NeurIPS 2022 (Google Research)
2. Anthropic Documentation, "Extended Thinking with Claude" — docs.anthropic.com (2025)
3. Wang et al., "Self-Consistency Improves Chain of Thought Reasoning" — ICLR 2023 (Google Research)
