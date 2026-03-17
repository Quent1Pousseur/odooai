# Module Purchase - Odoo 17 : Guide Complet

## Vue d'ensemble
Le module Purchase d'Odoo 17 gère l'intégralité du cycle de vie des achats, depuis les demandes de devis (RFQ) jusqu'aux factures fournisseurs, en passant par les réceptions et le contrôle qualité.

---

## USE CASE 1 : Création et gestion des bons de commande

### Modèle principal
**`purchase.order`** - Bon de commande d'achat

### Champs clés
- **`name`** : Référence du BC (ex: "PO00123")
- **`partner_id`** : Fournisseur (obligatoire)
- **`state`** : Statut avec workflow complet
- **`date_order`** : Date limite de commande
- **`date_planned`** : Date de livraison prévue
- **`currency_id`** : Devise
- **`order_line`** : Lignes de commande (One2many vers purchase.order.line)

### Workflow complet

1. **Brouillon (draft)** 
   - Création du BC via menu Achats > Commandes > Bons de commande
   - Saisie fournisseur, produits, quantités, prix
   - Calcul automatique des totaux via `_amount_all()`

2. **Demande de devis envoyée (sent)**
   - Action "Envoyer par email" 
   - Le PDF du devis est envoyé au fournisseur

3. **À approuver (to approve)**
   - Si montant > seuil défini dans la configuration
   - Nécessite validation par un responsable

4. **Bon de commande confirmé (purchase)**
   - BC confirmé et verrouillé
   - Génération automatique des réceptions prévues
   - Début du suivi des réceptions et facturations

5. **Terminé (done)**
   - Toutes les réceptions et facturations terminées
   - BC archivé

6. **Annulé (cancel)**
   - Annulation possible uniquement si pas de réception

### Menu dans Odoo
**Achats > Commandes > Bons de commande**
- Liste : vue liste des BC avec filtres par statut
- Formulaire : création/modification des BC

### Pièges courants
- **Modification après confirmation** : Par défaut bloquée selon paramètre `po_lock`
- **Devises multiples** : Attention aux taux de change figés à la confirmation
- **Dates planifiées** : Ne pas oublier les délais fournisseur

### Bonnes pratiques
- Configurer les approbations selon les montants
- Utiliser les références fournisseur dans `partner_ref`
- Définir des conditions générales dans `notes`

---

## USE CASE 2 : Gestion des lignes de commande

### Modèle principal
**`purchase.order.line`** - Ligne de commande d'achat

### Champs clés
- **`product_id`** : Produit commandé
- **`product_qty`** : Quantité commandée
- **`price_unit`** : Prix unitaire
- **`date_planned`** : Date de livraison prévue
- **`taxes_id`** : Taxes applicables (Many2many)
- **`qty_received`** : Quantité reçue
- **`qty_invoiced`** : Quantité facturée
- **`qty_to_invoice`** : Quantité à facturer

### Workflow de réception
1. **Commande confirmée**
   - `qty_received = 0`
   - `qty_received_method = 'manual'` (ou automatique selon le produit)

2. **Réception partielle/totale**
   - Mise à jour de `qty_received` 
   - Calcul automatique de `qty_to_invoice`

3. **Facturation**
   - Création des lignes de facture via `invoice_lines`
   - Mise à jour de `qty_invoiced`

### Méthodes de réception
- **Manuelle** : Saisie directe des quantités reçues
- **Stock automatique** : Via les bons de livraison (si module stock actif)

### Calculs de prix
- **`price_subtotal`** : Prix HT calculé automatiquement
- **`price_total`** : Prix TTC avec taxes
- **`price_tax`** : Montant des taxes

### Bonnes pratiques
- Vérifier les unités de mesure (`product_uom`)
- Utiliser les remises (`discount`) plutôt que modifier le prix
- Contrôler les dates de livraison par ligne

---

## USE CASE 3 : Intégration avec les factures fournisseur

### Modèles concernés
- **`account.move`** (héritée) - Facture fournisseur
- **`account.move.line`** - Ligne de facture

### Champs d'intégration
- **`purchase_vendor_bill_id`** : Auto-complétion depuis BC
- **`purchase_id`** : BC source (champ technique)
- **`purchase_line_id`** : Lien vers ligne de BC (sur account.move.line)

### Workflow d'intégration

1. **Création facture depuis BC**
   - Menu Achats > BC > Bouton "Créer facture"
   - Auto-remplissage via `_onchange_purchase_auto_complete()`
   - Reprise des lignes non encore facturées

2. **Correspondance automatique**
   - Calcul de `qty_to_invoice` en temps réel
   - Statut `invoice_status` : 'no', 'to invoice', 'invoiced'

3. **Contrôle à 3 niveaux** (si module activé)
   - Commande → Réception → Facture
   - Vérification des quantités à chaque étape

### Menu d'accès
**Comptabilité > Fournisseurs > Factures**
- Utilisation du champ "Auto-complétion" pour sélectionner un BC

### Pièges courants
- **Doubles facturations** : Vérifier `qty_to_invoice` avant création
- **Devises différentes** : Problème si devise facture ≠ devise BC
- **Taxes manquantes** : Reprises automatiquement du BC mais à vérifier

### Bonnes pratiques
- Toujours créer les factures depuis les BC pour maintenir la traçabilité
- Utiliser les références fournisseur (`partner_ref`) pour le rapprochement
- Contrôler les écarts de prix avec les BC

---

## USE CASE 4 : Configuration des produits pour les achats

### Modèle principal
**`product.template`** et **`product.product`** (hérités)

### Champs spécifiques achats
- **`purchase_method`** : Politique de contrôle
  - 'purchase' : Sur quantités commandées
  - 'receive' : Sur quantités reçues
- **`purchase_line_warn`** : Avertissements achats
- **`purchased_product_qty`** : Quantité achetée (12 derniers mois)

### Configuration par produit

1. **Onglet Achat** dans la fiche produit
   - Politique de contrôle des factures
   - Messages d'avertissement
   - Fournisseurs avec tarifs (`product.supplierinfo`)

2. **Fournisseurs et prix** 
   - Configuration des fournisseurs principaux
   - Grille de prix selon quantités
   - Délais de livraison par fournisseur

### Menu d'accès
**Achats > Produits > Produits**
- Configuration dans l'onglet "Achat" de la fiche produit

### Bonnes pratiques
- Configurer au minimum un fournisseur principal par produit
- Définir les délais de livraison réalistes
- Utiliser les politiques de contrôle selon le type de produit

---

## USE CASE 5 : Configuration générale du module

### Modèle de configuration
**`res.config.settings`** (hérité)

### Paramètres clés

1. **Approbations**
   - **`po_double_validation`** : Niveaux d'approbation
   - **`po_double_validation_amount`** : Seuil monétaire
   - **`po_order_approval`** : Activation approbation

2. **Contrôles**
   - **`lock_confirmed_po`** : Verrouillage des BC confirmés
   - **`default_purchase_method`** : Méthode par défaut
   - **`module_account_3way_match`** : Rapprochement à 3 niveaux

3. **Délais**
   - **`po_lead`** : Délai de sécurité achats
   - **`use_po_lead`** : Activation délai de sécurité

### Menu de configuration
**Achats > Configuration > Paramètres**

### Workflow de configuration

1. **Approbations** 
   - Définir les seuils selon les budgets
   - Assigner les responsables par montant

2. **Contrôles qualité**
   - Activer le rapprochement 3 niveaux pour contrôle strict
   - Configurer les verrouillages selon la politique entreprise

3. **Modules complémentaires**
   - Accords de prix (`purchase_requisition`)
   - Matrice de saisie (`purchase_product_matrix`)

### Pièges courants
- **Seuils trop bas** : Approbations systématiques
- **Verrouillage strict** : Blocage des corrections nécessaires
- **Délais mal calibrés** : Commandes trop anticipées ou tardives

### Bonnes pratiques
- Commencer avec des paramètres souples puis durcir progressivement
- Adapter les seuils d'approbation à la structure hiérarchique
- Tester les workflows avant déploiement global

---

## INTÉGRATIONS PRINCIPALES

### Avec le module Stock
- Génération automatique des bons de livraison
- Calcul automatique des quantités reçues
- Suivi des mouvements de stock

### Avec le module Comptabilité  
- Création automatique des factures fournisseur
- Imputation comptable automatique
- Rapprochement bancaire des paiements

### Avec le module Projet
- Imputation des coûts d'achat sur projets
- Suivi budgétaire par projet/analytic

Cette architecture modulaire permet une grande flexibilité selon les besoins métier tout en maintenant une cohérence des données entre tous les processus.