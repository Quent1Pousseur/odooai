# Module Stock Odoo 17 - Description Métier Complète

## Vue d'ensemble du module

Le module Stock d'Odoo 17 est le cœur de la gestion des stocks et de la logistique. Il gère les mouvements de marchandises, les emplacements, les entrepôts, et tous les processus de réception, stockage, préparation et expédition.

---

## USE CASE 1 : Gestion des Mouvements de Stock (Stock Move)

### Modèle principal : `stock.move`

**Champs clés :**
- `name` : Description du mouvement
- `product_id` : Produit concerné
- `product_qty` : Quantité réelle (calculée)
- `product_uom_qty` : Quantité demandée
- `product_uom` : Unité de mesure
- `location_id` : Emplacement source
- `location_dest_id` : Emplacement destination
- `state` : États (draft, waiting, confirmed, partially_available, assigned, done, cancel)
- `picking_id` : Référence vers le bon de transfert
- `date` : Date prévue/effective

**Workflow complet :**
1. **Création** (draft) : Le mouvement est créé mais pas confirmé
2. **Confirmation** (confirmed) : Le mouvement est confirmé mais pas réservé
3. **Réservation** (assigned) : Les produits sont réservés
4. **Traitement** (done) : Le mouvement est effectué
5. **Annulation** (cancel) : Le mouvement est annulé

**Menu dans Odoo :**
- Inventaire → Opérations → Mouvements de stock
- Inventaire → Rapports → Mouvements de stock

**Pièges courants :**
- Modifier `product_uom_qty` sur un mouvement assigné affecte les réservations
- Les mouvements chaînés via `move_dest_ids` peuvent créer des blocages
- L'état `partially_available` nécessite une attention particulière

**Bonnes pratiques :**
- Toujours vérifier l'état avant modification
- Utiliser les méthodes `_action_confirm()`, `_action_assign()`, `_action_done()`
- Gérer les unités de mesure avec précaution

---

## USE CASE 2 : Gestion des Types d'Opération (Picking Types)

### Modèle principal : `stock.picking.type`

**Champs clés :**
- `name` : Nom du type d'opération
- `code` : Type (incoming, outgoing, internal)
- `default_location_src_id` : Emplacement source par défaut
- `default_location_dest_id` : Emplacement destination par défaut
- `warehouse_id` : Entrepôt associé
- `sequence_code` : Préfixe de séquence
- `use_create_lots` : Créer de nouveaux lots
- `use_existing_lots` : Utiliser les lots existants
- `reservation_method` : Méthode de réservation (at_confirm, manual, by_date)

**Workflow complet :**
1. **Configuration** : Définir le type d'opération et ses paramètres
2. **Association** : Lier à un entrepôt et définir les emplacements
3. **Utilisation** : Utilisation automatique lors de la création des bons de transfert
4. **Personnalisation** : Adapter selon les besoins métier

**Menu dans Odoo :**
- Inventaire → Configuration → Types d'opération
- Configuration → Entrepôts → Types d'opération

**Pièges courants :**
- Mauvaise configuration des emplacements par défaut
- Oublier de configurer les séquences
- Mauvais paramétrage de la méthode de réservation

**Bonnes pratiques :**
- Créer des types d'opération spécialisés par processus
- Bien configurer les emplacements par défaut
- Utiliser des codes mnémotechniques

---

## USE CASE 3 : Gestion des Quantités et Quants

### Modèle principal : `stock.quant`

**Champs clés :**
- `product_id` : Produit
- `location_id` : Emplacement
- `lot_id` : Lot/numéro de série
- `package_id` : Conditionnement
- `owner_id` : Propriétaire
- `quantity` : Quantité totale
- `reserved_quantity` : Quantité réservée
- `available_quantity` : Quantité disponible (calculée)
- `in_date` : Date d'entrée

**Workflow complet :**
1. **Création automatique** : À la validation d'un mouvement entrant
2. **Réservation** : Lors de la confirmation des commandes
3. **Consommation** : À la validation d'un mouvement sortant
4. **Ajustement** : Via les inventaires physiques

**Menu dans Odoo :**
- Inventaire → Rapports → Quantités en stock
- Inventaire → Produits → Quantités en stock
- Inventaire → Opérations → Quants

**Pièges courants :**
- Les quants négatifs indiquent un problème de configuration
- La fragmentation des quants peut impacter les performances
- Attention aux quants réservés lors des ajustements

**Bonnes pratiques :**
- Surveiller la fragmentation des quants
- Utiliser les règles de rangement pour optimiser
- Effectuer des inventaires réguliers

---

## USE CASE 4 : Calcul des Quantités Produit

### Extension du modèle : `product.product`

**Champs clés ajoutés :**
- `qty_available` : Quantité en stock
- `virtual_available` : Quantité prévisionnelle
- `free_qty` : Quantité libre d'utilisation
- `incoming_qty` : Quantité entrante
- `outgoing_qty` : Quantité sortante
- `orderpoint_ids` : Règles de stock minimum

**Workflow complet :**
1. **Calcul temps réel** : Les quantités sont recalculées à chaque mouvement
2. **Contexte filtré** : Par emplacement, entrepôt, ou date
3. **Prévisionnel** : Intègre les mouvements futurs planifiés
4. **Alertes** : Génération d'alertes sur les stocks minimum

**Menu dans Odoo :**
- Inventaire → Produits → Produits (onglet Inventaire)
- Inventaire → Rapports → Évaluation du stock
- Inventaire → Configuration → Règles de stock

**Pièges courants :**
- Les calculs peuvent être lents sur de gros volumes
- Le contexte influence fortement les résultats
- Attention aux unités de mesure dans les calculs

**Bonnes pratiques :**
- Utiliser des vues matérialisées pour les performances
- Configurer des règles de réapprovisionnement
- Monitorer les performances des calculs

---

## USE CASE 5 : Gestion des Entrepôts

### Modèle principal : `stock.warehouse`

**Champs clés :**
- `name` : Nom de l'entrepôt
- `code` : Code court (5 caractères max)
- `company_id` : Société
- `partner_id` : Adresse
- `reception_steps` : Étapes de réception (1, 2, ou 3 étapes)
- `delivery_steps` : Étapes de livraison (1, 2, ou 3 étapes)
- `lot_stock_id` : Emplacement stock principal
- Emplacements spécialisés : `wh_input_stock_loc_id`, `wh_output_stock_loc_id`, etc.

**Workflow complet :**
1. **Création** : Création automatique des emplacements et types d'opération
2. **Configuration** : Paramétrage des flux de réception/expédition
3. **Utilisation** : Les processus utilisent automatiquement la configuration
4. **Optimisation** : Ajustement selon les besoins opérationnels

**Menu dans Odoo :**
- Inventaire → Configuration → Entrepôts
- Inventaire → Configuration → Emplacements

**Pièges courants :**
- Modification des étapes sur un entrepôt existant peut créer des incohérences
- Le code doit être unique par société
- Les droits d'accès multi-entrepôts nécessitent configuration

**Bonnes pratiques :**
- Planifier la structure avant création
- Utiliser des codes mnémotechniques
- Tester les flux après configuration
- Documenter les processus spécifiques

---

## Intégrations et Dépendances

**Modules liés :**
- `purchase` : Gestion des achats
- `sale` : Gestion des ventes  
- `mrp` : Fabrication
- `quality` : Contrôle qualité

**APIs importantes :**
- `_compute_quantities()` : Calcul des quantités
- `_action_confirm()` : Confirmation des mouvements
- `_action_assign()` : Réservation des produits
- `_action_done()` : Validation des mouvements

**Données de base essentielles :**
- Emplacements (stock.location)
- Catégories d'emplacements
- Unités de mesure
- Séquences pour numérotation

Ce module est le fondement de toute gestion logistique dans Odoo et nécessite une configuration soigneuse pour optimiser les flux opérationnels.