# Module Odoo 17 : sale_stock - Analyse Complète

## Vue d'ensemble
Le module `sale_stock` intègre la gestion des ventes avec la gestion des stocks dans Odoo. Il permet de gérer automatiquement les livraisons, le suivi des quantités disponibles, et la synchronisation entre commandes de vente et mouvements de stock.

---

## USE CASE 1 : Gestion des Commandes de Vente avec Livraisons

### Modèle principal : `sale.order`
**Champs clés :**
- `warehouse_id` : Entrepôt associé à la commande
- `picking_policy` : Politique de livraison ('direct' ou 'one')
- `picking_ids` : Bons de livraison associés
- `delivery_count` : Nombre de bons de livraison
- `delivery_status` : Statut de livraison ('pending', 'started', 'partial', 'full')
- `procurement_group_id` : Groupe de procurement
- `effective_date` : Date de livraison effective
- `expected_date` : Date de livraison prévue
- `incoterm` : Termes commerciaux internationaux

### Workflow complet :
1. **Création de la commande** : L'utilisateur crée une commande de vente
2. **Attribution de l'entrepôt** : Le système attribue automatiquement un entrepôt selon les règles de la société
3. **Confirmation de la commande** : Passage à l'état 'sale' déclenche la création des mouvements de stock
4. **Génération des bons de livraison** : Création automatique des `stock.picking`
5. **Traitement des livraisons** : Validation des bons de livraison
6. **Mise à jour du statut** : Le `delivery_status` évolue selon l'avancement

### Menu dans Odoo :
- **Ventes > Commandes > Commandes de vente**
- Onglet "Autres informations" pour les paramètres de livraison
- Smart buttons "Livraisons" pour accéder aux bons de livraison

### Pièges courants :
- Modifier l'entrepôt après confirmation peut créer des incohérences
- La politique de livraison 'one' peut retarder toute la commande si un produit n'est pas disponible
- Les annulations de commandes confirmées nécessitent l'annulation manuelle des mouvements de stock

### Bonnes pratiques :
- Définir des entrepôts par défaut par société/utilisateur
- Utiliser les termes Incoterm pour clarifier les responsabilités
- Surveiller le `delivery_status` pour le suivi client

---

## USE CASE 2 : Gestion des Lignes de Commande et Disponibilités

### Modèle principal : `sale.order.line`
**Champs clés :**
- `qty_delivered_method` : Méthode de calcul des quantités livrées (ajout 'stock_move')
- `route_id` : Route de stock sélectionnable
- `move_ids` : Mouvements de stock associés
- `virtual_available_at_date` : Stock virtuel à la date prévue
- `scheduled_date` : Date programmée de livraison
- `qty_to_deliver` : Quantité restant à livrer
- `is_mto` : Indique si c'est du Make To Order
- `display_qty_widget` : Affichage du widget de quantités
- `customer_lead` : Délai client

### Workflow complet :
1. **Saisie de la ligne** : Ajout d'un produit avec quantité
2. **Calcul de disponibilité** : Le système calcule `virtual_available_at_date` et `free_qty_today`
3. **Détermination de la route** : Attribution automatique ou manuelle de `route_id`
4. **Génération des besoins** : Création des mouvements de stock via `move_ids`
5. **Suivi des livraisons** : Mise à jour continue de `qty_to_deliver`

### Menu dans Odoo :
- **Ventes > Commandes > Commandes de vente > Lignes de commande**
- Widget de disponibilité visible sur les lignes de produits stockables

### Pièges courants :
- Les calculs de disponibilité peuvent être lents sur de gros volumes
- Le widget ne s'affiche que pour les produits stockables en état 'draft', 'sent', 'sale'
- Les modifications de quantité après confirmation nécessitent une gestion manuelle des mouvements

### Bonnes pratiques :
- Utiliser les routes personnalisées pour des flux spécifiques
- Surveiller `display_qty_widget` pour informer les commerciaux
- Paramétrer correctement les délais clients (`customer_lead`)

---

## USE CASE 3 : Intégration Stock-Facturation

### Modèle principal : `account.move` (hérite)
**Champs et méthodes clés :**
- `_stock_account_get_last_step_stock_moves()` : Récupère les mouvements de stock pour facturation
- `_get_invoiced_lot_values()` : Gestion des lots dans les factures

### Workflow complet :
1. **Livraison des produits** : Validation des bons de livraison
2. **Génération de facture** : Création depuis la commande de vente
3. **Récupération des mouvements** : Liaison automatique avec les mouvements de stock livrés
4. **Affichage des lots** : Si gestion par lots, affichage dans le rapport de facture
5. **Validation comptable** : Écritures comptables liées aux mouvements

### Menu dans Odoo :
- **Facturation > Clients > Factures**
- **Ventes > Commandes > Créer une facture**

### Pièges courants :
- Les factures d'acompte ne génèrent pas de mouvements de stock
- Les avoirs nécessitent une gestion particulière des mouvements retour
- La gestion des lots peut complexifier les rapports

### Bonnes pratiques :
- Valider les livraisons avant facturation pour la cohérence
- Utiliser les liens automatiques entre factures et mouvements
- Vérifier les quantités facturées vs livrées

---

## USE CASE 4 : Configuration du Module

### Modèle principal : `res.config.settings`
**Champs clés :**
- `security_lead` : Délai de sécurité pour les ventes
- `use_security_lead` : Activation du délai de sécurité
- `default_picking_policy` : Politique de livraison par défaut

### Workflow de configuration :
1. **Accès aux paramètres** : Paramètres > Technique > Paramètres généraux
2. **Section Inventaire** : Configuration des délais de sécurité
3. **Section Ventes** : Paramétrage de la politique de livraison par défaut
4. **Application** : Sauvegarde et application aux nouvelles commandes

### Menu dans Odoo :
- **Paramètres > Configuration > Inventaire**
- **Paramètres > Configuration > Ventes**

### Pièges courants :
- Le délai de sécurité s'applique à tous les produits de la société
- Changer la politique par défaut n'affecte pas les commandes existantes

### Bonnes pratiques :
- Définir un délai de sécurité adapté au secteur d'activité
- Choisir la politique de livraison selon la stratégie commerciale
- Tester les paramètres sur un environnement de développement

---

## USE CASE 5 : Gestion des Mouvements de Stock

### Modèle principal : `stock.move` (hérite)
**Champs clés :**
- `sale_line_id` : Ligne de commande de vente associée

### Modèle : `stock.picking` (hérite)
**Champs clés :**
- `sale_id` : Commande de vente associée (relation via group_id)

### Workflow complet :
1. **Génération automatique** : Création depuis les lignes de commande confirmées
2. **Groupement** : Association via `procurement.group`
3. **Traitement** : Validation des mouvements
4. **Mise à jour des commandes** : Synchronisation des quantités livrées

### Menu dans Odoo :
- **Inventaire > Opérations > Bons de livraison**
- **Inventaire > Opérations > Mouvements de stock**

### Pièges courants :
- Modifier manuellement les mouvements peut casser la synchronisation
- Les retours nécessitent une gestion spécifique
- L'annulation de mouvements doit être cohérente avec les commandes

### Bonnes pratiques :
- Utiliser les processus standards pour les modifications
- Documenter les cas particuliers de retours
- Maintenir la traçabilité via `sale_line_id`

---

## Points d'Attention Globaux

### Performance :
- Les calculs de disponibilité peuvent être lents sur de gros stocks
- Indexer correctement `sale_line_id` sur `stock.move`
- Utiliser les domaines pour filtrer efficacement

### Sécurité :
- Contrôler les accès aux entrepôts par société
- Vérifier les droits sur les modifications post-confirmation
- Auditer les changements de quantités

### Intégration :
- Cohérence avec les modules comptables (stock_account)
- Synchronisation avec les modules de planification (MRP)
- Compatibilité avec les modules e-commerce

Ce module est fondamental pour toute activité de vente de produits physiques dans Odoo, car il assure la liaison critique entre les processus commerciaux et logistiques.