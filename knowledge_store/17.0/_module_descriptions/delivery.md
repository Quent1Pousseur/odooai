# Module Delivery Odoo 17 - Guide Complet Métier

## Vue d'ensemble

Le module **Delivery** d'Odoo 17 gère l'ensemble des méthodes de livraison et du calcul des frais de port. Il permet de définir différents transporteurs, calculer automatiquement les coûts de livraison selon diverses règles, et intégrer avec des fournisseurs externes.

## USE CASE 1 : Configuration des Méthodes de Livraison

### Modèle Principal
**delivery.carrier** - Méthodes de livraison

### Champs Clés
- `name` : Nom de la méthode (ex: "Colissimo", "Chronopost")
- `delivery_type` : Type de provider ('base_on_rule', 'fixed', ou extensions)
- `integration_level` : Niveau d'intégration ('rate' ou 'rate_and_ship')
- `product_id` : Produit de livraison associé (obligatoire)
- `company_id` : Société propriétaire
- `active` : Statut actif/inactif
- `sequence` : Ordre d'affichage

### Menu Odoo
**Inventaire > Configuration > Livraison > Méthodes de Livraison**

### Workflow Complet
1. **Création** : Aller dans Inventaire > Configuration > Livraison > Méthodes de Livraison
2. **Configuration de base** :
   - Saisir le nom (ex: "Livraison Express")
   - Choisir le type de provider
   - Associer un produit de livraison
   - Définir la séquence d'affichage
3. **Configuration avancée** :
   - Définir les pays/états de livraison
   - Configurer les préfixes de codes postaux
   - Paramétrer les marges et frais fixes
4. **Activation** : Cocher le champ "Actif"

### Pièges Courants
- **Produit manquant** : Le champ `product_id` est obligatoire, créer d'abord le produit
- **Contrainte marge** : La marge ne peut être inférieure à -100%
- **Devise** : La devise est héritée du produit associé

### Bonnes Pratiques
- Créer un produit dédié par méthode de livraison
- Utiliser des séquences logiques (10, 20, 30...)
- Tester en environnement de développement avant la production

## USE CASE 2 : Règles de Prix Basées sur Critères

### Modèle Principal
**delivery.price.rule** - Règles de tarification

### Champs Clés
- `carrier_id` : Transporteur associé
- `variable` : Variable de calcul (weight, volume, price, quantity)
- `operator` : Opérateur de comparaison (<=, <, >=, >, ==)
- `max_value` : Valeur seuil
- `list_base_price` : Prix de base fixe
- `list_price` : Prix variable
- `variable_factor` : Facteur multiplicateur

### Menu Odoo
**Inventaire > Configuration > Livraison > Méthodes de Livraison > [Méthode] > Onglet "Règles de Prix"**

### Workflow Complet
1. **Accès** : Ouvrir une méthode de livraison existante
2. **Création de règle** :
   - Cliquer sur "Ajouter une ligne" dans l'onglet "Règles de Prix"
   - Choisir la variable (poids, volume, prix, quantité)
   - Définir l'opérateur et la valeur seuil
   - Configurer le prix de base et/ou variable
3. **Exemple concret** :
   - Si poids <= 5kg alors prix fixe 10€
   - Si poids <= 10kg alors prix fixe 15€
   - Si poids > 10kg alors 15€ + 2€ × poids

### Formule de Calcul
```
Prix = list_base_price + (list_price × valeur_variable_factor)
```

### Pièges Courants
- **Ordre des règles** : Respecter la séquence, la première règle matchée est appliquée
- **Overlapping** : Éviter les chevauchements de conditions
- **Variable factor** : Bien comprendre la différence entre variable de condition et facteur

### Bonnes Pratiques
- Ordonner les règles de la plus restrictive à la plus générale
- Documenter chaque règle avec un nom explicite
- Tester avec différents scénarios de commande

## USE CASE 3 : Intégration avec les Commandes de Vente

### Modèle Principal
**sale.order** (héritage)

### Champs Clés
- `carrier_id` : Méthode de livraison sélectionnée
- `delivery_message` : Message de livraison
- `delivery_set` : Booléen indiquant si livraison configurée
- `recompute_delivery_price` : Indicateur de recalcul nécessaire
- `shipping_weight` : Poids de livraison calculé

### Modèle Ligne
**sale.order.line** (héritage)
- `is_delivery` : Identifie les lignes de livraison
- `product_qty` : Quantité en unité du produit

### Menu Odoo
**Ventes > Commandes > Commandes de Vente**

### Workflow Complet
1. **Sur la commande** :
   - Créer/modifier une commande de vente
   - Cliquer sur "Ajouter une méthode de livraison"
2. **Wizard de sélection** :
   - Choisir le transporteur dans la liste
   - Le système calcule automatiquement le prix
   - Valider pour ajouter la ligne de livraison
3. **Mise à jour** :
   - Modifier les lignes de commande déclenche le flag `recompute_delivery_price`
   - Utiliser "Recalculer les frais de livraison" si nécessaire

### Actions Disponibles
- `action_open_delivery_wizard()` : Ouvre le wizard de sélection
- `set_delivery_line()` : Définit la ligne de livraison
- `_remove_delivery_line()` : Supprime les lignes existantes

### Pièges Courants
- **Facturé** : Impossible de modifier si déjà facturé
- **Lignes multiples** : Une seule ligne de livraison par commande
- **Recalcul automatique** : Attention aux modifications qui déclenchent le recalcul

### Bonnes Pratiques
- Configurer les méthodes avant de traiter les commandes
- Vérifier le poids estimé avant validation
- Utiliser le wizard plutôt que la modification manuelle

## USE CASE 4 : Gestion des Zones de Livraison

### Modèle Principal
**delivery.zip.prefix** - Préfixes de codes postaux

### Champs Clés
- `name` : Préfixe (automatiquement en majuscules)

### Relations dans delivery.carrier
- `country_ids` : Pays de livraison autorisés
- `state_ids` : États/régions autorisés  
- `zip_prefix_ids` : Préfixes de codes postaux

### Menu Odoo
**Inventaire > Configuration > Livraison > Préfixes de Codes Postaux**

### Workflow Complet
1. **Création des préfixes** :
   - Aller dans le menu préfixes
   - Créer les préfixes (ex: "75", "69", "13")
2. **Association aux transporteurs** :
   - Ouvrir la méthode de livraison
   - Dans l'onglet "Destination", ajouter :
     - Pays autorisés
     - États/régions (si applicable)
     - Préfixes de codes postaux
3. **Utilisation** : Le système filtre automatiquement selon l'adresse de livraison

### Expressions Régulières
- Support des regex pour codes postaux variables
- Exemple : "100$" pour matcher exactement "100" et pas "1000"

### Pièges Courants
- **Majuscules** : Les préfixes sont automatiquement convertis en majuscules
- **Unicité** : Contrainte d'unicité sur les préfixes
- **Regex** : Bien tester les expressions régulières complexes

### Bonnes Pratiques
- Utiliser des préfixes logiques par zones géographiques
- Tester la correspondance avec des adresses réelles
- Documenter les regex utilisées

## USE CASE 5 : Calculs de Frais et Marges

### Champs de Configuration
- `margin` : Pourcentage de marge (minimum -100%)
- `fixed_margin` : Marge fixe en devise
- `free_over` : Livraison gratuite si commande > seuil
- `amount` : Montant seuil pour livraison gratuite
- `shipping_insurance` : Pourcentage d'assurance (0-100%)

### Workflow de Calcul
1. **Calcul de base** : Selon les règles ou prix fixe
2. **Application des marges** :
   ```
   Prix = prix_base × (1 + margin/100) + fixed_margin
   ```
3. **Vérification seuil gratuit** :
   - Si `free_over` activé et montant commande ≥ `amount`
   - Alors prix = 0 et ajout mention "Livraison Gratuite"

### Méthodes de Calcul
- **Fixed** : Prix fixe défini sur le transporteur
- **Based on Rules** : Selon les règles de tarification configurées

### Pièges Courants
- **Marge négative** : Limitée à -100% par contrainte SQL
- **Assurance** : Doit être un pourcentage entre 0 et 100
- **Devise** : Tous les calculs dans la devise du produit associé

### Bonnes Pratiques
- Tester les calculs avec différents montants de commande
- Configurer des marges réalistes
- Valider les seuils de livraison gratuite

## Intégrations et Extensions

### Providers Externes
Le système est conçu pour être étendu avec des fournisseurs externes :
- Méthodes à implémenter : `_rate_shipment`, `_send_shipping`, `_get_tracking_link`
- Extension du champ `delivery_type`
- Configuration d'environnement prod/test

### Modules Complémentaires
- `delivery_barcode` : Code-barres pour livraisons
- `delivery_stock_picking_batch` : Intégration avec les lots de picking
- `delivery_iot` : Intégration IoT pour balances connectées

### Sécurité et Permissions
- Utilisation de `SUPERUSER_ID` pour certaines opérations
- Vérifications de société via `check_company=True`
- Protection contre suppression des produits via `ondelete='restrict'`

Ce module est central dans la gestion logistique d'Odoo et s'intègre parfaitement avec les ventes, stock et facturation pour offrir une expérience complète de gestion des livraisons.