# Module Odoo 17 : account_payment - Guide Complet

## Vue d'ensemble

Le module `account_payment` est un pont entre les modules `payment` (transactions de paiement) et `account` (comptabilité). Il permet de gérer automatiquement la comptabilisation des paiements électroniques et leur réconciliation avec les factures.

---

## USE CASE 1 : Gestion des Transactions de Paiement liées aux Factures

### Modèle : `payment.transaction` (héritage)

**Champs clés ajoutés :**
- `payment_id` : Many2one vers `account.payment` (readonly)
- `invoice_ids` : Many2many vers `account.move` (factures liées)
- `invoices_count` : Integer (nombre de factures calculé)

### Workflow complet

1. **Création de transaction avec factures**
   - Une transaction est créée avec des factures liées via `invoice_ids`
   - Le préfixe de référence est généré automatiquement à partir des noms de factures

2. **Confirmation de transaction**
   - Méthode `_reconcile_after_done()` appelée automatiquement
   - Les factures en brouillon sont validées automatiquement
   - Un paiement comptable est créé via `_create_payment()`

3. **Annulation de transaction**
   - Méthode `_set_canceled()` appelée
   - Le paiement associé est automatiquement annulé

### Menu Odoo
- **Facturation > Clients > Paiements** pour voir les transactions
- **Facturation > Fournisseurs > Paiements** pour les transactions fournisseurs

### Pièges courants
- ⚠️ **Factures multiples** : S'assurer que toutes les factures sont dans la même devise
- ⚠️ **Droits d'accès** : La méthode `_compute_reference_prefix` doit être appelée en sudo
- ⚠️ **Validation automatique** : Les factures draft sont automatiquement validées

### Bonnes pratiques
```python
# Création correcte d'une transaction avec factures
transaction_vals = {
    'amount': 1000.0,
    'currency_id': invoice.currency_id.id,
    'partner_id': invoice.partner_id.id,
    'invoice_ids': [(6, 0, [invoice.id])],  # X2M command
    'reference': f'INV-{invoice.name}',
}
transaction = self.env['payment.transaction'].create(transaction_vals)
```

---

## USE CASE 2 : Paiements avec Tokens de Paiement Sauvegardés

### Modèle : `account.payment` (héritage)

**Champs clés ajoutés :**
- `payment_transaction_id` : Many2one vers `payment.transaction`
- `payment_token_id` : Many2one vers `payment.token`
- `suitable_payment_token_ids` : Many2many (tokens disponibles)
- `use_electronic_payment_method` : Boolean
- `source_payment_id` : Many2one (pour les remboursements)
- `amount_available_for_refund` : Monetary

### Workflow complet

1. **Sélection du mode de paiement électronique**
   - Choisir un journal avec méthode de paiement électronique
   - Le champ `use_electronic_payment_method` devient True

2. **Sélection du token de paiement**
   - Les tokens disponibles sont filtrés par partenaire et fournisseur
   - Seulement les fournisseurs sans capture manuelle

3. **Validation du paiement**
   - Méthode `action_post()` surchargée
   - Si un token est sélectionné, une transaction de paiement est créée automatiquement

### Menu Odoo
- **Facturation > Clients > Paiements**
- **Facturation > Fournisseurs > Paiements**
- Formulaire de paiement avec section "Paiement électronique"

### Pièges courants
- ⚠️ **Tokens invalidés** : Vérifier que le token est encore valide
- ⚠️ **Capture manuelle** : Les fournisseurs avec capture manuelle sont exclus
- ⚠️ **Droits sudo** : Les tokens sont recherchés en mode sudo

### Bonnes pratiques
```python
# Création d'un paiement avec token
payment_vals = {
    'amount': 500.0,
    'partner_id': partner.id,
    'journal_id': electronic_journal.id,
    'payment_token_id': saved_token.id,
}
payment = self.env['account.payment'].create(payment_vals)
payment.action_post()  # Créera automatiquement la transaction
```

---

## USE CASE 3 : Configuration des Fournisseurs de Paiement

### Modèle : `payment.provider` (héritage)

**Champs clés ajoutés :**
- `journal_id` : Many2one vers `account.journal` (journal de paiement)

### Workflow complet

1. **Activation d'un fournisseur**
   - Un journal bancaire est automatiquement assigné
   - Une ligne de méthode de paiement est créée automatiquement

2. **Configuration du journal**
   - Le journal peut être modifié manuellement
   - La ligne de méthode de paiement est mise à jour automatiquement

3. **Désactivation/Suppression**
   - Vérification qu'aucun paiement n'utilise cette méthode
   - Suppression de la méthode de paiement associée

### Menu Odoo
- **Facturation > Configuration > Fournisseurs de paiement**
- Onglet "Configuration" avec champ "Journal de paiement"

### Pièges courants
- ⚠️ **Suppression bloquée** : Impossible de supprimer si des paiements existent
- ⚠️ **Journal obligatoire** : Un fournisseur activé doit avoir un journal
- ⚠️ **Méthode de paiement unique** : Une seule méthode par code fournisseur

### Bonnes pratiques
```python
# Configuration correcte d'un fournisseur
provider = self.env['payment.provider'].create({
    'name': 'Mon Fournisseur',
    'code': 'my_provider',
    'state': 'enabled',
    'company_id': self.env.company.id,
})
# Le journal sera automatiquement assigné
```

---

## USE CASE 4 : Gestion des Factures avec Paiements en Ligne

### Modèle : `account.move` (héritage)

**Champs clés ajoutés :**
- `transaction_ids` : Many2many vers `payment.transaction`
- `authorized_transaction_ids` : Many2many (transactions autorisées)
- `amount_paid` : Monetary (montant payé)

### Workflow complet

1. **Facture avec paiements en ligne activés**
   - Méthode `_has_to_be_paid()` retourne True
   - Conditions : facture validée, partiellement payée, pas de transaction en cours

2. **Capture des paiements autorisés**
   - Action `payment_action_capture()` dans la facture
   - Toutes les transactions autorisées sont capturées

3. **Annulation des paiements**
   - Action `payment_action_void()` pour annuler les autorisations

### Menu Odoo
- **Facturation > Clients > Factures**
- Boutons "Capturer" et "Annuler" dans le formulaire de facture
- Onglet intelligent "Transactions" 

### Pièges courants
- ⚠️ **Paramètre système** : `account_payment.enable_portal_payment` doit être activé
- ⚠️ **État de facture** : Seulement les factures validées et non payées
- ⚠️ **Transactions en cours** : Bloque les nouveaux paiements si transaction pending

### Bonnes pratiques
```python
# Vérifier si une facture peut être payée en ligne
if invoice._has_to_be_paid():
    # Créer un lien de paiement
    payment_link_vals = invoice._get_default_payment_link_values()
    
# Capturer tous les paiements autorisés
invoice.payment_action_capture()
```

---

## USE CASE 5 : Lignes de Méthodes de Paiement avec Fournisseurs

### Modèle : `account.payment.method.line` (héritage)

**Champs clés ajoutés :**
- `payment_provider_id` : Many2one vers `payment.provider`
- `payment_provider_state` : Selection (état du fournisseur)

### Workflow complet

1. **Création automatique lors de l'ajout d'une méthode**
   - Si c'est une méthode électronique, un fournisseur est assigné automatiquement
   - Évite les doublons sur le même journal

2. **Gestion des fournisseurs actifs**
   - Impossible de supprimer une ligne liée à un fournisseur actif
   - Protection contre la suppression accidentelle

3. **Navigation vers le fournisseur**
   - Action `action_open_provider_form()` pour ouvrir la configuration

### Menu Odoo
- **Facturation > Configuration > Journaux**
- Onglets "Paiements entrants/sortants"
- Bouton "Configurer le fournisseur" sur chaque ligne

### Pièges courants
- ⚠️ **Suppression bloquée** : Vérifier l'état du fournisseur avant suppression
- ⚠️ **Assignment automatique** : Un seul fournisseur par méthode et journal
- ⚠️ **Méthodes électroniques** : Seulement pour les méthodes de type 'electronic'

### Bonnes pratiques
```python
# Vérification avant suppression
payment_method_line = self.env['account.payment.method.line'].browse(line_id)
if payment_method_line.payment_provider_state in ['enabled', 'test']:
    raise UserError("Impossible de supprimer une méthode active")
```

---

## Points d'Attention Généraux

### Configuration Système Requise
- Module `payment` installé
- Module `account` installé  
- Paramètre `account_payment.enable_portal_payment` pour les paiements portail

### Sécurité et Droits d'Accès
- Beaucoup d'opérations utilisent `sudo()` pour contourner les restrictions
- Les tokens de paiement sont toujours accessibles en lecture pour les utilisateurs ayant accès aux paiements

### Performance
- Index `btree_not_null` sur `source_payment_id`
- Requêtes SQL directes pour calculer le nombre de factures
- Auto-join sur `payment_transaction_id`

### Intégration avec d'Autres Modules
- Compatible avec tous les modules fournisseurs de paiement (Stripe, PayPal, etc.)
- S'intègre avec le portail client pour les paiements en ligne
- Synchronisé avec la comptabilité analytique si configurée