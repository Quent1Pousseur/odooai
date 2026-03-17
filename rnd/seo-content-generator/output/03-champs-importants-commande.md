# Quels champs sont importants dans une commande Odoo ?

## Reponse courte
Une commande Odoo (`sale.order`) contient 56 champs dans le module sale. Les champs obligatoires sont `name`, `partner_id`, `date_order`, `partner_invoice_id` et `partner_shipping_id`. Les montants (`amount_untaxed`, `amount_tax`, `amount_total`) sont calcules automatiquement. Chaque ligne (`sale.order.line`) a 38 champs dont `product_id`, `product_uom_qty`, `price_unit`.

## Details
### Champs obligatoires de `sale.order`
- `name` (char) — Order Reference **obligatoire**
- `company_id` (many2one) — Company **obligatoire**
- `partner_id` (many2one) — Customer **obligatoire**
- `date_order` (datetime) — Order Date **obligatoire**
- `partner_invoice_id` (many2one) — Invoice Address **obligatoire** (calcule automatiquement)
- `partner_shipping_id` (many2one) — Delivery Address **obligatoire** (calcule automatiquement)

### Champs monetaires (calcules automatiquement)
- `amount_untaxed` (monetary) — Untaxed Amount (calcule automatiquement)
- `amount_tax` (monetary) — Taxes (calcule automatiquement)
- `amount_total` (monetary) — Total (calcule automatiquement)
- `amount_to_invoice` (monetary) — Amount to invoice (calcule automatiquement)
- `amount_invoiced` (monetary) — Already invoiced (calcule automatiquement)

### Champs relationnels cles
- `partner_id` (many2one) — Customer **obligatoire** → `res.partner`
- `partner_invoice_id` (many2one) — Invoice Address **obligatoire** → `res.partner`
- `partner_shipping_id` (many2one) — Delivery Address **obligatoire** → `res.partner`
- `order_line` (one2many) — Order Lines → `sale.order.line`
- `payment_term_id` (many2one) — Payment Terms → `account.payment.term`
- `pricelist_id` (many2one) — Pricelist → `product.pricelist`
- `currency_id` (many2one) — Currency → `res.currency`
- `user_id` (many2one) — Salesperson → `res.users`
- `team_id` (many2one) — Sales Team → `crm.team`
- `journal_id` (many2one) — Invoicing Journal → `account.journal`
- `fiscal_position_id` (many2one) — Fiscal Position → `account.fiscal.position`
- `invoice_ids` (many2many) — Invoices → `account.move`
- `transaction_ids` (many2many) — Transactions → `payment.transaction`
- `tag_ids` (many2many) — Tags → `crm.tag`
- `analytic_account_id` (many2one) — Analytic Account → `account.analytic.account`

### Champs obligatoires de `sale.order.line`
- `order_id` (many2one) — Order Reference **obligatoire** → `sale.order`
- `name` (text) — Description **obligatoire** (calcule automatiquement)
- `product_uom_qty` (float) — Quantity **obligatoire** (calcule automatiquement)
- `price_unit` (float) — Unit Price **obligatoire** (calcule automatiquement)
- `customer_lead` (float) — Lead Time **obligatoire** (calcule automatiquement)

### Champs monetaires des lignes
- `price_subtotal` (monetary) — Subtotal (calcule automatiquement)
- `price_tax` (float) — Total Tax (calcule automatiquement)
- `price_total` (monetary) — Total (calcule automatiquement)
- `price_reduce_taxexcl` (monetary) — Price Reduce Tax excl (calcule automatiquement)
- `price_reduce_taxinc` (monetary) — Price Reduce Tax incl (calcule automatiquement)
- `untaxed_amount_invoiced` (monetary) — Untaxed Invoiced Amount (calcule automatiquement)
- `untaxed_amount_to_invoice` (monetary) — Untaxed Amount To Invoice (calcule automatiquement)

### Statistiques
- **sale.order** : 56 champs, dont 6 obligatoires, 25 calcules, 5 monetaires
- **sale.order.line** : 38 champs, dont 5 obligatoires, 7 monetaires

## Comment activer
1. Installer le module **Sales** (`sale`) via **Applications**
2. Aller dans **Ventes > Commandes > Devis > Nouveau**
3. Remplir le client (`partner_id`) — les adresses de facturation et livraison se calculent automatiquement
4. Ajouter des lignes de commande avec produit, quantite et prix
5. Les montants totaux se mettent a jour automatiquement

## Modeles Odoo concernes
| Modele | Description | Nb champs | Obligatoires |
|--------|-------------|-----------|--------------|
| `sale.order` | Sales Order | 56 | 6 |
| `sale.order.line` | Sales Order Line | 38 | 5 |
| `res.partner` | Contact | - | relation via `partner_id` |
| `product.product` | Produit | - | relation via `product_id` |
| `account.tax` | Taxes | - | relation via `tax_id` |
