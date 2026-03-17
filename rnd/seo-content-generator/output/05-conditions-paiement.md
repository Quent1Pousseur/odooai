# Comment gerer les conditions de paiement ?

## Reponse courte
Les conditions de paiement dans Odoo sont gerees via le champ `payment_term_id` du modele `sale.order`, qui reference le modele `account.payment.term`. Ce champ est calcule automatiquement a partir du client (`_compute_payment_term_id`) mais peut etre modifie manuellement. Les transactions de paiement en ligne sont tracees via `transaction_ids`.

## Details
### Conditions de paiement sur la commande
- `payment_term_id` (many2one) — Payment Terms (calcule automatiquement)

Le champ `payment_term_id` est un **many2one** vers `account.payment.term`. Il est calcule automatiquement via `_compute_payment_term_id` qui recupere les conditions de paiement par defaut du client (`partner_id`). Ce champ controle :
- Les echeances de facturation
- Les dates d'echeance sur les factures generees
- Le calcul des paiements partiels

### Position fiscale
- `fiscal_position_id` (many2one) — Fiscal Position (calcule automatiquement)

La position fiscale adapte automatiquement les taxes et comptes comptables selon le client ou le pays. Son help text dans le code source Odoo : *"Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices.The default value comes from the customer."*

### Paiement en ligne
- `transaction_ids` (many2many) — Transactions
- `amount_paid` (float) — Amount Paid (calcule automatiquement)
- `reference` (char) — Payment Ref.

Les transactions de paiement (`payment.transaction`) sont liees a la commande via `transaction_ids` (many2many, readonly). Le montant deja paye est calcule par `_compute_amount_paid`.

### Configuration du fournisseur de paiement
Le module sale etend le modele `payment.provider` avec le champ :
- `so_reference_type` (selection) — Communication

Ce champ definit la communication sur le paiement : soit basee sur la reference du document (`so_name` — "Based on Document Reference"), soit sur l'ID client (`partner` — "Based on Customer ID"). Valeur par defaut : `so_name`.

### Prepaiement
Le champ `require_payment` (boolean) exige un paiement en ligne avant confirmation. Le pourcentage minimum est controle par `prepayment_percent` (float, compute `_compute_prepayment_percent`).

## Comment activer
1. Aller dans **Comptabilite > Configuration > Conditions de paiement**
2. Creer ou modifier les conditions (ex: 30 jours, 50% a la commande + 50% a 30 jours)
3. Assigner les conditions par defaut sur la fiche client (**Contacts > onglet Ventes**)
4. Sur chaque commande, le champ **Conditions de paiement** est rempli automatiquement
5. Pour le paiement en ligne : **Ventes > Configuration > Parametres > Paiement en ligne**
6. Configurer les fournisseurs de paiement dans **Comptabilite > Configuration > Fournisseurs de paiement**

## Modeles Odoo concernes
| Modele | Description | Role |
|--------|-------------|------|
| `sale.order` | Sales Order | Porte `payment_term_id` et `transaction_ids` |
| `account.payment.term` | Conditions de paiement | Definit les echeances et modalites |
| `account.fiscal.position` | Position fiscale | Adapte taxes selon le client (`fiscal_position_id`) |
| `payment.transaction` | Transaction de paiement | Paiements en ligne lies a la commande |
| `payment.provider` | Fournisseur de paiement | Etendu avec `so_reference_type` pour la communication |
