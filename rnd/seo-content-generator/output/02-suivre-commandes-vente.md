# Comment suivre mes commandes de vente ?

## Reponse courte
Odoo offre un suivi complet des commandes de vente via le modele `sale.order`. Le champ `state` indique l'etat (brouillon, confirme, annule), tandis que `invoice_status` suit l'avancement de la facturation. Les quantites livrees et facturees sont tracees ligne par ligne dans `sale.order.line`.

## Details
### Suivi de l'etat de la commande
Le champ `state` (selection, default `draft`) controle le cycle de vie de la commande. Il est en lecture seule (`readonly=True`) et change via les actions du workflow :
- **draft** : Brouillon / Devis
- **sent** : Devis envoye au client
- **sale** : Commande confirmee
- **cancel** : Annulee

Le tri par defaut est `date_order desc, id desc`, ce qui affiche les commandes les plus recentes en premier.

### Suivi de la facturation
- `invoice_status` (selection) — Invoice Status (calcule automatiquement)
- `invoice_count` (integer) — Invoice Count (calcule automatiquement)
- `amount_to_invoice` (monetary) — Amount to invoice (calcule automatiquement)
- `amount_invoiced` (monetary) — Already invoiced (calcule automatiquement)

Le champ `invoice_status` est calcule via `_compute_invoice_status` et peut prendre les valeurs : a facturer, facture, rien a facturer.

### Suivi par ligne de commande (`sale.order.line`)
Chaque ligne suit individuellement :
- `qty_delivered` (float) — Delivery Quantity (calcule automatiquement)
- `qty_invoiced` (float) — Invoiced Quantity (calcule automatiquement)
- `qty_to_invoice` (float) — Quantity To Invoice (calcule automatiquement)

La methode de mise a jour de la quantite livree est controlee par `qty_delivered_method` (selection : `manual` ou `analytic`).

## Comment activer
1. Aller dans **Ventes > Commandes > Commandes** pour voir toutes les commandes confirmees
2. Utiliser les **filtres** par etat (`state`) ou statut de facturation (`invoice_status`)
3. Cliquer sur une commande pour voir le detail des lignes
4. L'onglet **Factures** montre les factures liees (`invoice_ids`, `invoice_count`)
5. Le bouton **Creer une facture** apparait quand `invoice_status = "to invoice"`

## Modeles Odoo concernes
| Modele | Description | Role |
|--------|-------------|------|
| `sale.order` | Sales Order | Commande principale avec etat et montants |
| `sale.order.line` | Sales Order Line | Lignes de detail avec quantites livrees/facturees |
| `account.move` | Facture | Factures liees via `invoice_ids` (many2many, compute `_get_invoiced`) |
| `crm.team` | Sales Team | Equipe commerciale (`team_id`, compute `_compute_team_id`) |
