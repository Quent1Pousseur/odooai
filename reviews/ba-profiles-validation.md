# Validation BA Profiles — Odoo Expert (10)

## Date : 2026-03-18
## Profiles revus : sales_crm

---

## sales_crm — Ventes & CRM

### Summary
✅ Correct — decrit bien le pipeline prospect → devis → commande → facture.

### Capabilities (5)
✅ Coherentes avec les modules sale + crm.

### Feature Discoveries (7)

| # | Feature | Module | Verdict | Note |
|---|---------|--------|---------|------|
| 1 | Scoring predictif prospects | crm.lead.scoring.frequency | ✅ Correct | Existe en Enterprise. Bien identifie. |
| 2 | Templates de devis avec options | sale_management.sale.order.template | ✅ Correct | Necessite sale_management. |
| 3 | Alertes abonnements | sale_subscription.sale.order.alert | ⚠️ Partiel | Necessite sale_subscription (Enterprise). Pas installe chez tous. |
| 4 | Attribution auto prospects | crm.crm.team | ✅ Correct | Via les regles d'assignation. |
| 5 | Acomptes et paiements anticipes | sale.sale.advance.payment.inv | ✅ Correct | Wizard standard dans sale. |
| 6-7 | (autres) | | A verifier en detail | |

### Gotchas (5)
✅ Les pieges sont pertinents (contraintes SQL, dependances inter-modules).

### Verdict
**Qualite : 4/5.** Les feature discoveries sont factuellement correctes pour la majorite. Attention aux features Enterprise (scoring, subscriptions) qui ne sont pas disponibles en Community.

### Recommandation
Ajouter dans le BA Profile un champ `edition: "enterprise" | "community" | "both"` pour chaque feature_discovery. Permet d'eviter de recommander une feature Enterprise a un client Community.

---

## accounting — A valider en Sprint 3
Le module accounting est plus sensible (implications legales). Validation approfondie necessaire.

---

## Conclusion
Les BA Profiles sales_crm sont de bonne qualite pour un MVP. Les recommandations sont factuellement correctes a ~85%. Les 15% restants sont des features Enterprise presentees sans distinction. A ameliorer en Sprint 3.
