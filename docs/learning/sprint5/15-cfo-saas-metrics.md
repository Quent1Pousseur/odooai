# Learning — CFO (15) — SaaS Financial Metrics (MRR, ARR, LTV, CAC)

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **MRR est la metrique reine du SaaS** : Le Monthly Recurring Revenue se decompose en New MRR (nouveaux clients), Expansion MRR (upgrades), Contraction MRR (downgrades) et Churn MRR (departs). Pour OdooAI, chaque plan (Free > Pro > Enterprise) a un MRR unitaire fixe, plus un MRR variable lie aux credits usage-based.

2. **LTV/CAC ratio determine la viabilite** : Le ratio Lifetime Value / Customer Acquisition Cost doit etre superieur a 3 pour un SaaS sain. LTV = ARPU x Gross Margin / Monthly Churn Rate. Pour un AI SaaS, le cout des tokens LLM impacte directement la gross margin, donc le LTV.

3. **Net Revenue Retention (NRR) mesure la croissance organique** : Un NRR > 100% signifie que les clients existants depensent plus chaque mois (expansion). Pour OdooAI, si les clients ajoutent des connexions Odoo ou consomment plus de credits agent, le NRR augmente sans effort d'acquisition.

4. **Gross margin AI SaaS est sous pression** : Contrairement au SaaS classique (80%+ gross margin), un AI SaaS paie les tokens LLM par requete. OdooAI doit viser 65-70% de gross margin en optimisant le routing des modeles (Haiku pour le simple, Opus uniquement quand necessaire).

5. **Payback period guide les depenses marketing** : Le temps pour recuperer le CAC doit etre inferieur a 12 mois. Si le plan Pro est a 49 EUR/mois et le CAC est de 300 EUR, le payback est de 6 mois — acceptable. Au-dela de 18 mois, le modele est risque.

## Comment ca s'applique a OdooAI

1. **Dashboard financier interne** : OdooAI a besoin d'un dashboard interne (pas client) qui track MRR, NRR, churn, LTV/CAC en temps reel. Les donnees viennent de Stripe (billing) et du metering interne (usage tokens). Cela guide les decisions de pricing et d'investissement.

2. **Optimisation de la gross margin via le routing modele** : La strategie 3+2 tokens (validee Gate 3.5) impacte directement la gross margin. Chaque point de pourcentage gagne sur le cout token se traduit en LTV superieur. Le CFO doit recevoir un rapport mensuel cout/revenu par agent.

3. **Projections de tresorerie basees sur la cohorte** : Les cohortes mensuelles (clients acquis en mars, avril, etc.) permettent de projeter le MRR futur et d'anticiper les besoins de tresorerie. Critique pour un SaaS pre-revenue qui doit lever ou etre rentable rapidement.

## Ce que je recommande

1. **Sprint 6** : Definir les KPIs financiers cibles pour le lancement : MRR objectif a M+6, gross margin cible (65%), churn mensuel max (5%), LTV/CAC ratio min (3x). Documenter dans `docs/business/financial-targets.md`.

2. **Sprint 7** : Integrer Stripe webhooks pour alimenter automatiquement un calcul de MRR en temps reel. Stocker les events billing dans une table dediee pour le reporting.

3. **Sprint 8** : Construire un modele de projection financier (spreadsheet ou script Python) base sur les cohortes, le churn observe, et le cout token reel. Presenter au fondateur pour valider le plan de croissance.

## Sources

1. David Skok, "SaaS Metrics 2.0" — For Entrepreneurs Blog (2024)
2. Bessemer Venture Partners, "State of the Cloud" — Annual Report (2025)
3. a16z, "The Cost of AI Infrastructure" — Andreessen Horowitz Research (2025)
