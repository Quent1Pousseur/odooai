# Learning — SaaS Architect (06) — Pricing Psychology et Plan Design
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

1. **L'effet d'ancrage avec 3 plans est prouve** — Presenter 3 plans (Starter, Pro,
   Enterprise) avec le plan du milieu mis en avant pousse 60% des acheteurs vers
   celui-ci. Le plan Enterprise sert principalement d'ancrage psychologique pour
   rendre le Pro "raisonnable". Notre grille actuelle (49/149/499 EUR) suit ce pattern.

2. **Le "value metric" doit etre aligne avec la valeur percue** — Facturer au nombre
   de "requetes IA" est abstrait. Facturer au nombre de "modules Odoo analyses" ou
   "utilisateurs Odoo couverts" est concret et correle avec la taille du client.
   Notion facture par membre, pas par "blocks" — c'est intuitif.

3. **Le prix annuel avec -20% cree un engagement et reduit le churn** — Le churn
   mensuel moyen en B2B SaaS est de 5-7%. Le plan annuel le reduit a 1-2% car
   le cout de switching est psychologiquement plus eleve. Afficher le prix mensuel
   meme pour l'annuel ("12 EUR/mois facture annuellement") maximise la conversion.

4. **Les "feature gates" sont plus efficaces que les "usage limits"** — Limiter le
   nombre de requetes frustre. Bloquer l'acces a des features premium (audit securite,
   export PDF, multi-utilisateurs) motive l'upgrade. Le client ne se sent pas "puni"
   pour avoir trop utilise le produit.

5. **Le freemium tue les SaaS B2B a petit marche** — Avec un TAM de ~50k entreprises
   utilisant Odoo, chaque lead compte. Un free tier attire des curieux qui ne
   convertiront jamais. Mieux : un trial de 14 jours avec acces complet au plan Pro,
   puis downgrade vers Starter ou upgrade vers Pro.

## Comment ca s'applique a OdooAI

1. **Restructurer les limites par plan** : Au lieu de limiter les requetes, limiter
   les features. Starter : 1 connexion Odoo, analyse basique, chat uniquement.
   Pro : 3 connexions, audit securite, slash commands, export PDF. Enterprise :
   connexions illimitees, API, SSO, audit compliance.

2. **Trial 14 jours sur le plan Pro** : Donner acces complet au Pro pendant 14 jours.
   A J10, envoyer un email montrant les features Pro utilisees qui seront perdues.
   Conversion target : 15% trial -> payant (benchmark B2B SaaS).

3. **Pricing annuel agressif** : Proposer -25% sur l'annuel (pas -20%) pour compenser
   notre manque de notoriete. Starter : 37 EUR/mois annuel (vs 49 mensuel).
   Pro : 112 EUR/mois annuel (vs 149 mensuel). L'economie affichee motive.

## Ce que je recommande

1. **Sprint 8** : Revoir la grille tarifaire avec le fondateur. Proposer le passage
   de "usage limits" a "feature gates". Document : `docs/pricing-v2.md` avec
   tableau comparatif des 3 plans et les features par gate.

2. **Sprint 9** : Implementer la logique de trial 14 jours dans le backend.
   Tables : `subscriptions` avec `trial_ends_at`, `plan_id`, `billing_cycle`.
   Emails automatiques a J1, J7, J10, J13. Fichier : `odooai/services/billing/`.

3. **Sprint 9** : Creer la page pricing sur le frontend avec le toggle
   mensuel/annuel, le plan Pro mis en avant visuellement (badge "Most Popular"),
   et le CTA "Start 14-day free trial". Fichier : `web/app/pricing/page.tsx`.

## Sources

1. "Monetizing Innovation" — Madhavan Ramanujam (Wiley, 2016) — Feature gating vs usage limits
2. Patrick Campbell (ProfitWell) — "The SaaS Pricing Page Teardown" series (YouTube)
3. Kyle Poyar (OpenView) — "2025 Product-Led Growth Benchmarks" — Conversion trial -> paid
