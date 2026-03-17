# Module Odoo 17 : MRP (Manufacturing Resource Planning)

## Vue d'ensemble

Le module **MRP** d'Odoo 17 gère l'ensemble du processus de fabrication, depuis la planification des ordres de fabrication jusqu'à l'exécution sur les centres de travail. Il orchestre la production en gérant les nomenclatures (BoM), les ordres de fabrication, les ordres de travail et les centres de travail.

---

## USE CASE 1 : Création et gestion d'un Ordre de Fabrication

### Modèle principal : `mrp.production`

### Champs clés :
- **`name`** : Référence automatique (ex: "MO/001")
- **`product_id`** : Produit à fabriquer
- **`product_qty`** : Quantité à produire
- **`bom_id`** : Nomenclature utilisée
- **`state`** : État ('draft', 'confirmed', 'progress', 'to_close', 'done', 'cancel')
- **`date_start`** / **`date_finished`** : Dates de début/fin planifiées
- **`location_src_id`** : Emplacement des composants
- **`location_dest_id`** : Emplacement des produits finis
- **`move_raw_ids`** : Mouvements de stock des matières premières
- **`move_finished_ids`** : Mouvements de stock des produits finis
- **`workorder_ids`** : Ordres de travail associés

### Workflow complet :

1. **Création** (Draft)
   - Saisie manuelle ou génération automatique via MRP
   - Définition produit + quantité + nomenclature

2. **Confirmation** 
   - Validation de la nomenclature
   - Création des mouvements de stock
   - Génération des ordres de travail
   - Réservation des composants

3. **Lancement** (In Progress)
   - Début de production
   - Consommation des matières premières

4. **Finalisation** (To Close → Done)
   - Validation des quantités produites
   - Clôture des ordres de travail
   - Transfert vers stock produits finis

### Menu Odoo :
**Fabrication > Opérations > Ordres de fabrication**

### Pièges courants :
- Oublier de confirmer la disponibilité des composants avant lancement
- Nomenclature incohérente (produit fini non défini dans BoM)
- Dates de planification irréalistes par rapport aux capacités

### Bonnes pratiques :
- Toujours vérifier `reservation_state` avant confirmation
- Utiliser les back-orders pour les productions partielles
- Planifier avec marge sur les `date_start`/`date_finished`

---

## USE CASE 2 : Gestion des Ordres de Travail sur Centre de Travail

### Modèle principal : `mrp.workorder`

### Champs clés :
- **`name`** : Nom de l'opération
- **`workcenter_id`** : Centre de travail assigné
- **`production_id`** : Ordre de fabrication parent
- **`operation_id`** : Opération de la nomenclature (routing)
- **`state`** : État ('pending', 'waiting', 'ready', 'progress', 'done', 'cancel')
- **`qty_producing`** : Quantité en cours de production
- **`qty_produced`** : Quantité déjà produite
- **`date_start`** / **`date_finished`** : Dates réelles d'exécution
- **`duration_expected`** : Durée prévue (minutes)
- **`duration`** : Durée réelle
- **`move_raw_ids`** / **`move_finished_ids`** : Mouvements associés

### Workflow complet :

1. **Génération automatique** depuis ordre de fabrication
   - Basé sur les opérations de la nomenclature
   - Séquençage selon `operation_id.sequence`

2. **Planification** 
   - Attribution aux centres de travail
   - Calcul des créneaux via `leave_id`
   - Gestion des dépendances entre opérations

3. **Exécution**
   - Démarrage manuel ou automatique
   - Suivi temps réel via `mrp.workcenter.productivity`
   - Consommation des composants

4. **Validation**
   - Contrôle qualité
   - Validation quantités produites
   - Transfert vers opération suivante

### Menu Odoo :
**Fabrication > Opérations > Ordres de travail**
**Fabrication > Planification > Planning**

### Pièges courants :
- Capacité centre de travail sous-estimée (`default_capacity`)
- Dépendances d'opérations mal configurées
- Temps de setup/cleanup non pris en compte

### Bonnes pratiques :
- Utiliser les feuilles de route pour traçabilité
- Monitorer les KPI via `oee`, `performance`
- Prévoir des centres de travail alternatifs

---

## USE CASE 3 : Configuration des Nomenclatures (BoM)

### Modèle principal : `mrp.bom`

### Champs clés :
- **`product_tmpl_id`** : Modèle de produit
- **`product_id`** : Variante spécifique (optionnel)
- **`type`** : Type ('normal' = fabrication, 'phantom' = kit)
- **`product_qty`** : Quantité de base
- **`bom_line_ids`** : Lignes composants (`mrp.bom.line`)
- **`operation_ids`** : Opérations de fabrication (`mrp.routing.workcenter`)
- **`ready_to_produce`** : Politique de lancement
- **`consumption`** : Flexibilité consommation

### Modèles liés :
- **`mrp.bom.line`** : Composants avec quantités
- **`mrp.routing.workcenter`** : Opérations sur centres de travail

### Workflow de configuration :

1. **Définition produit fini**
   - Sélection `product_tmpl_id`
   - Quantité de référence `product_qty`

2. **Ajout composants** (`bom_line_ids`)
   - Produit + quantité + UdM
   - Gestion variantes produits

3. **Définition gamme** (`operation_ids`)
   - Séquence opérations
   - Centre de travail par opération
   - Temps de setup, production, cleanup

4. **Paramétrage avancé**
   - Politique de lancement (`ready_to_produce`)
   - Flexibilité consommation (`consumption`)

### Menu Odoo :
**Fabrication > Données de base > Nomenclatures**

### Pièges courants :
- UdM incohérentes entre BoM et composants
- Gammes mal séquencées
- Type 'phantom' utilisé à tort

### Bonnes pratiques :
- Une BoM par variante produit si nécessaire
- Tester avec ordres de fabrication pilotes
- Documenter les modifications via suivi

---

## USE CASE 4 : Gestion des Centres de Travail

### Modèle principal : `mrp.workcenter`

### Champs clés :
- **`name`** : Nom du centre
- **`code`** : Code unique
- **`default_capacity`** : Capacité par défaut
- **`time_efficiency`** : Efficacité (%)
- **`costs_hour`** : Coût horaire
- **`time_start`** / **`time_stop`** : Temps setup/cleanup
- **`working_state`** : État ('normal', 'blocked', 'done')
- **`alternative_workcenter_ids`** : Centres alternatifs
- **`capacity_ids`** : Capacités par produit

### Workflow de configuration :

1. **Création centre**
   - Définition nom, code, séquence
   - Paramétrage capacités et coûts

2. **Configuration calendrier**
   - Via `resource_id` (héritage `resource.mixin`)
   - Horaires de travail, congés

3. **Optimisation**
   - Centres alternatifs pour flexibilité
   - Capacités spécifiques par produit
   - Suivi KPI (OEE, performance)

### Menu Odoo :
**Fabrication > Configuration > Centres de travail**

### Pièges courants :
- Calendrier mal configuré (cause pannes planning)
- Capacités irréalistes
- Coûts horaires obsolètes

### Bonnes pratiques :
- Calibrer capacités sur données réelles
- Monitorer `oee_target` vs réalisé
- Maintenir centres alternatifs actifs

---

## USE CASE 5 : Traçabilité et Suivi de Production

### Modèles impliqués :
- **`stock.move.line`** : Mouvements détaillés avec lots
- **`mrp.workcenter.productivity`** : Temps de travail
- **`stock.lot`** : Numéros de lot/série

### Champs de traçabilité :
- **`lot_producing_id`** : Lot en cours de production
- **`move_line_ids`** : Détail mouvements avec lots
- **`workorder_id`** : Lien ordre de travail
- **`production_id`** : Lien ordre de fabrication

### Workflow traçabilité :

1. **Configuration produits**
   - `tracking` = 'lot' ou 'serial'
   - Activation traçabilité matières

2. **Production avec lots**
   - Génération/saisie `lot_producing_id`
   - Scan lots composants
   - Association automatique via `move_line_ids`

3. **Reporting**
   - Traçabilité amont/aval
   - Rapports consommation/production
   - Analyse écarts

### Menu Odoo :
**Inventaire > Données de base > Lots/Numéros de série**
**Fabrication > Rapports > Traçabilité**

### Pièges courants :
- Lots non scannés → traçabilité incomplète
- Configuration `picking_type_id` manquante
- Mouvements manuels non tracés

### Bonnes pratiques :
- Scanner systématiquement tous les lots
- Utiliser codes-barres pour fiabilité
- Former utilisateurs aux bonnes pratiques scan

---

## Intégrations et Points d'attention

### Avec module Stock :
- Synchronisation `stock.move` ↔ `mrp.production`
- Réservations automatiques composants
- Mise à jour stock temps réel

### Avec module Purchase :
- Règles réapprovisionnement automatique
- Ordres d'achat pour composants manquants

### Paramètres système critiques :
- **Type d'opération** : `picking_type_id` avec code 'mrp_operation'
- **Emplacements** : Source/destination bien configurés
- **Calendriers** : Ressources et centres de travail alignés

### Performance :
- Index sur `production_id`, `workcenter_id`
- Archivage des productions anciennes
- Monitoring des `_compute` fields intensifs

Ce module MRP constitue le cœur du système de production d'Odoo, avec une architecture modulaire permettant une gestion complète depuis la planification jusqu'à l'exécution et le contrôle qualité.