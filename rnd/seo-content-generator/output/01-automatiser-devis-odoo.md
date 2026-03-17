# Comment automatiser mes devis dans Odoo ?

## Reponse courte
Odoo permet d'automatiser la creation et le suivi des devis grace au modele `sale.order`. Les devis peuvent etre envoyes automatiquement par email, signer en ligne et convertis en commande de vente en un clic. Le champ `state` gere le cycle de vie complet (brouillon, envoye, confirme, annule).

## Details
Le modele **sale.order** (Odoo 17) gere l'ensemble du processus devis-commande. Voici les champs cles pour l'automatisation :

- `validity_date` (date) — Expiration (calcule automatiquement)
- `require_signature` (boolean) — Online signature (calcule automatiquement)
- `require_payment` (boolean) — Online payment (calcule automatiquement)
- `prepayment_percent` (float) — Prepayment percentage (calcule automatiquement)
- `state` (selection) — Status
- `note` (html) — Terms and conditions (calcule automatiquement)

### Signature et paiement en ligne
Le champ `require_signature` (boolean) permet d'exiger une signature electronique du client avant confirmation. Il est calcule via `_compute_require_signature` et peut etre active par defaut dans les parametres.

Le champ `require_payment` (boolean) exige un prepaiement en ligne. Le pourcentage est controle par `prepayment_percent` (calcule via `_compute_prepayment_percent`).

### Date d'expiration automatique
Le champ `validity_date` (date) est calcule automatiquement via `_compute_validity_date` a partir des parametres de la societe. Le champ `is_expired` (boolean, compute `_compute_is_expired`) indique si le devis a expire.

### Conditions et notes
Le champ `note` (html) contient les conditions generales, calculees automatiquement via `_compute_note` depuis les parametres de la societe (`terms_type` est un related sur `company_id.terms_type`).

## Comment activer
1. Aller dans **Ventes > Configuration > Parametres**
2. Activer **Signature en ligne** pour exiger la signature client
3. Activer **Paiement en ligne** et definir le pourcentage de prepaiement
4. Definir la **duree de validite par defaut** des devis
5. Configurer les **conditions generales** dans les parametres de la societe
6. Creer un devis via **Ventes > Commandes > Devis > Nouveau**

## Modeles Odoo concernes
| Modele | Description | Role |
|--------|-------------|------|
| `sale.order` | Sales Order | Modele principal des devis et commandes |
| `res.partner` | Contact | Client du devis (`partner_id`, required) |
| `product.pricelist` | Pricelist | Liste de prix applicable (`pricelist_id`, compute) |
| `res.company` | Societe | Source des parametres par defaut (validite, conditions) |
