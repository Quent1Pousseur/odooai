# Learning — Customer Success (17) — NPS and CSAT Measurement for Early-Stage SaaS
## Date : 2026-03-21 (Sprint 5, session 2)
## Duree : 3 heures

## Ce que j'ai appris

1. **NPS et CSAT mesurent des choses differentes** — Le NPS (Net Promoter Score) mesure la
   loyaute et la propension a recommander. Le CSAT (Customer Satisfaction Score) mesure la
   satisfaction sur une interaction specifique. En early-stage, le CSAT par feature est plus
   actionnable que le NPS global, car la base utilisateur est trop petite pour un NPS fiable.

2. **Le NPS devient significatif a partir de 50 reponses** — En dessous, les variations
   statistiques rendent le score non fiable. Pour une beta avec 6-8 design partners, il faut
   privilegier le CSAT transactionnel (apres chaque interaction cle) et les interviews
   qualitatives plutot que le NPS.

3. **Le "CES" (Customer Effort Score) est sous-estime** — "A quel point c'etait facile ?"
   est souvent plus predictif du churn que le NPS. Pour un produit conversationnel comme
   OdooAI, mesurer l'effort percu pour obtenir une reponse utile est directement correle
   a la retention.

4. **Le timing de la mesure change tout** — Envoyer un survey NPS le lundi matin donne des
   scores 15-20% plus bas qu'en milieu de semaine. Pour le CSAT in-app, le declencher
   immediatement apres une action reussie (pas apres un echec) donne un baseline sain qu'on
   peut ensuite comparer.

5. **Les verbatims des detracteurs valent plus que le score** — Le chiffre NPS seul est un
   vanity metric. La vraie valeur est dans les commentaires ouverts des detracteurs (score
   0-6). Chaque verbatim negatif doit etre traite comme un bug report prioritaire en beta.

## Comment ca s'applique a OdooAI

- **CSAT post-conversation comme metrique primaire** — Apres chaque conversation resolue,
  demander "Cette reponse etait-elle utile ?" (echelle 1-5). Agreger par type de question
  (schema, workflow, config, debug) pour identifier les zones faibles du knowledge graph.

- **CES sur le flow de connexion Odoo** — Le setup de la connexion a l'instance Odoo est le
  moment de verite. Mesurer l'effort percu immediatement apres : si c'est superieur a 3/5,
  le funnel d'onboarding a un probleme critique.

- **NPS trimestriel a partir du launch public** — Attendre d'avoir 50+ utilisateurs actifs
  avant de lancer le premier NPS. D'ici la, les interviews qualitatives mensuelles avec les
  design partners donnent un signal plus riche.

## Ce que je recommande

1. **Sprint 6 : implementer le CSAT post-conversation** — Rating 1-5 apres chaque echange,
   stockage en base, dashboard simple. Objectif : CSAT moyen > 4.0 sur les reponses schema.

2. **Sprint 7 : ajouter le CES sur l'onboarding** — Mesurer l'effort percu a la fin du
   flow de connexion Odoo. Correlater avec le taux d'activation (premiere question posee).

3. **Sprint 9 : premier NPS si la base le permet** — Viser 50 reponses minimum. Mettre en
   place un process de traitement des verbatims detracteurs sous 48h.

## Sources

- Bain & Company — "The Ultimate Question 2.0" (Fred Reichheld, NPS methodology)
- Gartner — "Effortless Experience" (CES research, Dixon et al., 2013)
- Jason Lemkin (SaaStr) — "NPS for Early-Stage SaaS: When It Matters" (2025)
