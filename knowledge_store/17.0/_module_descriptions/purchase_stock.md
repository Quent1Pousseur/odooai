# Module purchase_stock - Odoo 17

## Vue d'ensemble
Le module **purchase_stock** fait le pont entre les achats et la gestion des stocks dans Odoo 17. Il automatise la création de réceptions de stock lors de la confirmation des commandes d'achat et calcule les quantités reçues basées sur les mouvements de stock.

---

## USE CASE 1 : Création automatique de réceptions à partir des commandes d'achat

### Modèles concernés
- **purchase.order** (commandes d'achat)
- **purchase.order.line** (lignes de commande d'achat)
- **stock.picking** (bons de réception)
- **stock.move** (mouvements de stock)

### Champs clés
**purchase.order** :
- `picking_type_id` : Type d'opération (par défaut : réception entrante)
- `picking_ids` : Bons de réception liés (Many2many calculé)
- `incoming_picking_count` : Nombre de réceptions
- `dest_address_id` : Adresse de livraison
- `group_id` : Groupe d'approvisionnement
- `is_shipped` : Statut d'expédition
- `effective_date` : Date effective de réception
- `receipt_status` : Statut de réception ('pending', 'partial', 'full')

**purchase.order.line** :
- `move_ids` : Mouvements de stock liés (One2many)
- `qty_received_method` : Méthode de calcul ('stock_moves')
- `orderpoint_id` : Règle de réapprovisionnement
- `move_dest_ids` : Mouvements de stock aval
- `propagate_cancel` : Propagation d'annulation
- `forecasted_issue` : Problème prévu de stock

**stock.move** :
- `purchase_line_id` : Ligne de commande d'achat liée
- `created_purchase_line_ids` : Lignes créées par ce mouvement

### Workflow complet
1. **Création commande** : Navigation → Achats → Commandes d'achat → Créer
2. **Ajout lignes** : Sélection produits stockables (type 'product' ou 'consu')
3. **Confirmation** : Bouton "Confirmer la commande"
4. **Création automatique réception** : 
   - Méthode `button_approve()` appelle `_create_picking()`
   - Création `stock.picking` avec `picking_type_id`
   - Génération `stock.move` pour chaque ligne
5. **Réception** : Navigation → Stock → Opérations → Réceptions
6. **Traitement** : Validation des quantités reçues
7. **Mise à jour automatique** : `qty_received` calculé via mouvements

### Menu dans Odoo
- **Commandes d'achat** : Achats → Commandes d'achat
- **Réceptions** : Stock → Opérations → Réceptions
- **Règles de réapprovisionnement** : Stock → Configuration → Règles de réapprovisionnement

### Pièges courants
- **Type de produit incorrect** : Seuls les produits 'product' et 'consu' génèrent des réceptions
- **Picking type manquant** : Vérifier la configuration du type d'opération
- **Warehouse non configuré** : S'assurer qu'un entrepôt existe
- **Dates incohérentes** : La date prévue doit être cohérente

### Bonnes pratiques
- Configurer correctement les types d'opérations par défaut
- Utiliser les groupes d'approvisionnement pour organiser
- Vérifier les règles de stock avant confirmation
- Paramétrer les emplacements de destination

---

## USE CASE 2 : Calcul automatique des quantités reçues

### Modèles concernés
- **purchase.order.line**
- **stock.move**

### Champs clés
**purchase.order.line** :
- `qty_received` : Quantité reçue (calculé automatiquement)
- `qty_received_method` : 'stock_moves' pour produits stockables
- `qty_received_manual` : Quantité manuelle (backup)

### Workflow complet
1. **Base de calcul** : Méthode `_compute_qty_received()`
2. **Filtrage mouvements** : Méthode `_get_po_line_moves()`
3. **Calcul par mouvement** :
   - Mouvements 'done' uniquement
   - Gestion des retours (`_is_purchase_return()`)
   - Conversion UdM (`_compute_quantity()`)
4. **Mise à jour temps réel** : Dépendance sur `move_ids.state`

### Cas particuliers gérés
- **Retours fournisseur** : Soustraction des quantités
- **Dropshipping retourné** : Pas de double comptage
- **Mouvements annulés** : Exclusion du calcul

### Pièges courants
- **UdM différentes** : Conversion automatique mais vérifier cohérence
- **Mouvements partiels** : Calcul en temps réel, pas de problème
- **Dates d'écriture comptable** : Contexte `accrual_entry_date`

### Bonnes pratiques
- Ne pas forcer `qty_received_manual` sauf cas spécifique
- Vérifier les conversions d'unités de mesure
- Utiliser les dépendances pour le calcul automatique

---

## USE CASE 3 : Règles d'approvisionnement par achat

### Modèles concernés
- **stock.rule** (règles de stock)
- **stock.warehouse.orderpoint** (règles de réapprovisionnement)

### Champs clés
**stock.rule** :
- `action` : 'buy' pour déclenchement d'achat
- `picking_type_code_domain` : 'incoming'

### Workflow complet
1. **Configuration** : Stock → Configuration → Règles
2. **Sélection action** : "Acheter" dans le type d'action
3. **Paramétrage** : Type d'opération réception
4. **Déclenchement** : Méthode `_run_buy()` lors d'approvisionnement
5. **Recherche fournisseur** : `_select_seller()` sur le produit
6. **Création/mise à jour BC** : Regroupement par domaine

### Processus de regroupement
1. **Groupement par domaine** : Fournisseur, société, devises
2. **Recherche BC existant** : `_make_po_get_domain()`
3. **Création si inexistant** : `_prepare_purchase_order()`
4. **Ajout ligne si existant** : Mise à jour origine

### Pièges courants
- **Pas de fournisseur** : Erreur `ProcurementException`
- **Quantités minimales** : Vérifier les règles fournisseur
- **Délais fournisseur** : Dates non valides
- **Devise incompatible** : Problème de regroupement

### Bonnes pratiques
- Configurer tous les fournisseurs avec prix
- Paramétrer les quantités minimales
- Vérifier les délais de livraison
- Tester les règles d'approvisionnement

---

## USE CASE 4 : Gestion des écarts de prix (Price Difference)

### Modèles concernés
- **account.move.line** (lignes de facture)
- **stock.valuation.layer** (couches de valorisation)

### Champs clés
**account.move.line** :
- `purchase_line_id` : Ligne d'achat associée

### Workflow complet
1. **Réception marchandise** : Création couches valorisation
2. **Réception facture** : Prix facture ≠ prix réception
3. **Calcul écart** : Méthode `_apply_price_difference()`
4. **Génération écritures** : `_generate_price_difference_vals()`
5. **Création SVL/AML** : Nouvelles couches et écritures

### Logique de calcul
1. **Historique chronologique** : Tri couches et factures
2. **Matrice correspondance** : Couche ↔ Facture
3. **Calcul quantités restantes** : Par couche
4. **Génération écart** : Nouvelle valorisation

### Pièges courants
- **Factures non lettrées** : État 'posted' uniquement
- **Retours complexes** : Gestion des retours partiels
- **Devises multiples** : Conversion automatique
- **Quantités décimales** : Précision arrondi

### Bonnes pratiques
- Lettrer rapidement les factures
- Vérifier les écarts significatifs
- Utiliser les bons comptes comptables
- Contrôler les conversions de devises

---

## USE CASE 5 : Suivi des problèmes prévisionnels de stock

### Modèles concernés
- **purchase.order.line**

### Champs clés
- `forecasted_issue` : Problème de stock prévu (Boolean calculé)

### Workflow complet
1. **Calcul automatique** : `_compute_forecasted_issue()`
2. **Stock virtuel** : Avec contexte entrepôt et date
3. **Projection** : Ajout quantité commandée si brouillon
4. **Alerte** : Si stock virtuel < 0

### Paramètres de calcul
- **Entrepôt** : De la commande d'achat
- **Date** : Date prévue de la ligne
- **Stock virtuel** : Stock disponible projeté

### Pièges courants
- **Mauvais entrepôt** : Vérifier le picking_type_id
- **Dates incohérentes** : Date prévue incorrecte
- **Stock multi-emplacements** : Calcul par entrepôt

### Bonnes pratiques
- Surveiller les alertes de stock
- Anticiper les dates de livraison
- Configurer correctement les entrepôts
- Utiliser les tableaux de bord stock

---

## Bonnes pratiques générales

### Configuration initiale
1. **Types d'opérations** : Configurer réceptions par défaut
2. **Entrepôts** : Créer et paramétrer correctement
3. **Règles de stock** : Définir règles d'achat
4. **Fournisseurs** : Paramétrer avec prix et délais

### Utilisation quotidienne
1. **Confirmation rapide** : Éviter commandes en attente
2. **Réceptions régulières** : Traiter rapidement les arrivées
3. **Suivi écarts** : Contrôler les différences de prix
4. **Monitoring stock** : Utiliser les alertes prévisionnelles

### Maintenance système
1. **Nettoyage périodique** : Archiver anciennes commandes
2. **Vérification règles** : Tester approvisionnement
3. **Contrôle performances** : Optimiser requêtes complexes
4. **Formation utilisateurs** : Workflow standard

Le module purchase_stock automatise efficacement le lien achat-stock mais nécessite une configuration soignée pour éviter les pièges courants liés aux conversions, aux règles d'approvisionnement et à la valorisation des stocks.