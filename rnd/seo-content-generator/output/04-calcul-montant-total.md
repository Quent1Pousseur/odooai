# Comment Odoo calcule le montant total d'une commande ?

## Reponse courte
Le montant total d'une commande Odoo est calcule automatiquement par la methode `_compute_amounts` du modele `sale.order`. Il additionne les sous-totaux de chaque ligne (`sale.order.line`), ou chaque ligne calcule `price_subtotal` et `price_tax` via sa propre methode `_compute_amount`. La formule de base est : `price_unit * product_uom_qty * (1 - discount/100)` + taxes.

## Details
### Niveau ligne (`sale.order.line`)
Chaque ligne de commande calcule ses montants via `_compute_amount` :

- `price_unit` (float) — Unit Price **obligatoire** (calcule automatiquement)
- `product_uom_qty` (float) — Quantity **obligatoire** (calcule automatiquement)
- `discount` (float) — Discount (%) (calcule automatiquement)
- `price_subtotal` (monetary) — Subtotal (calcule automatiquement)
- `price_tax` (float) — Total Tax (calcule automatiquement)
- `price_total` (monetary) — Total (calcule automatiquement)

**Formule** :
```
subtotal = price_unit * product_uom_qty * (1 - discount / 100)
total = subtotal + taxes calculees via tax_id
```

Les prix reduits sont aussi disponibles :
- `price_reduce_taxexcl` (monetary) — Price Reduce Tax excl (calcule automatiquement)
- `price_reduce_taxinc` (monetary) — Price Reduce Tax incl (calcule automatiquement)

### Niveau commande (`sale.order`)
Les montants de la commande sont agreges via `_compute_amounts` :

- `amount_untaxed` (monetary) — Untaxed Amount (calcule automatiquement)
- `amount_tax` (monetary) — Taxes (calcule automatiquement)
- `amount_total` (monetary) — Total (calcule automatiquement)
- `amount_undiscounted` (float) — Amount Before Discount (calcule automatiquement)

**Formule** :
```
amount_untaxed = SUM(order_line.price_subtotal)
amount_tax     = SUM(order_line.price_tax)
amount_total   = amount_untaxed + amount_tax
```

### Gestion multi-devises
Le champ `currency_id` (many2one vers `res.currency`) definit la devise de la commande. Le taux de change est stocke dans `currency_rate` (float, compute `_compute_currency_rate`). Les montants totaux detailles incluant les regroupements par taux de taxe sont dans `tax_totals` (binary, compute `_compute_tax_totals`).

### Methode d'arrondi
Le champ `tax_calculation_rounding_method` (selection, related `company_id.tax_calculation_rounding_method`) controle si les taxes sont arrondies ligne par ligne ou globalement.

## Comment activer
1. Les calculs sont **automatiques** — aucune configuration requise
2. Pour changer la devise : modifier `pricelist_id` ou `currency_id` sur la commande
3. Pour appliquer des remises : remplir le champ `discount` (%) sur chaque ligne
4. Les taxes sont definies dans **Comptabilite > Configuration > Taxes**
5. La position fiscale (`fiscal_position_id`) peut adapter les taxes automatiquement selon le client

## Modeles Odoo concernes
| Modele | Methode compute | Champs calcules |
|--------|-----------------|-----------------|
| `sale.order` | `_compute_amounts` | `amount_untaxed`, `amount_tax`, `amount_total` |
| `sale.order` | `_compute_amount_undiscounted` | `amount_undiscounted` |
| `sale.order` | `_compute_currency_rate` | `currency_rate` |
| `sale.order.line` | `_compute_amount` | `price_subtotal`, `price_tax`, `price_total` |
| `sale.order.line` | `_compute_price_reduce_taxexcl` | `price_reduce_taxexcl` |
| `sale.order.line` | `_compute_price_reduce_taxinc` | `price_reduce_taxinc` |
