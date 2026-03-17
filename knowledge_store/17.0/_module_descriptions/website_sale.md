# Module Odoo 17 : website_sale - Description métier complète

## PRÉSENTATION GÉNÉRALE

Le module **website_sale** est le module central du e-commerce d'Odoo 17. Il transforme votre site web en boutique en ligne complète avec gestion des produits, panier, commandes, moyens de paiement et processus de checkout.

---

## USE CASE 1 : GESTION DES PRODUITS E-COMMERCE

### Modèle : product.template

**Champs clés spécifiques e-commerce :**
- `website_description` : Description HTML pour le site web
- `description_ecommerce` : Description spécifique e-commerce
- `alternative_product_ids` : Produits alternatifs (upsell)
- `accessory_product_ids` : Produits accessoires (cross-sell)
- `website_size_x/website_size_y` : Taille d'affichage sur la grille
- `website_ribbon_id` : Ruban promotionnel
- `website_sequence` : Ordre d'affichage
- `public_categ_ids` : Catégories publiques e-commerce
- `product_template_image_ids` : Images supplémentaires
- `base_unit_count/base_unit_id` : Prix à l'unité de mesure
- `compare_list_price` : Prix comparé (barré)

**Workflow complet :**
1. **Création produit** : Vente > Produits > Créer
2. **Configuration e-commerce** : Onglet "Vente" du produit
   - Cocher "Publié sur le site web"
   - Définir catégories publiques
   - Ajouter description web
3. **Images et média** : Onglet "Images supplémentaires"
4. **Prix et promotions** : 
   - Prix de comparaison pour affichage barré
   - Prix à l'unité si pertinent
5. **Cross-selling** :
   - Produits alternatifs (suggestions)
   - Produits accessoires (panier)

**Menu principal :** Site Web > Configuration > Produits

**Pièges courants :**
- Ne pas publier le produit → invisible sur le site
- Oublier les catégories publiques → produit difficile à trouver
- Images de mauvaise qualité → impact sur conversions
- Séquence non définie → ordre d'affichage aléatoire

**Bonnes pratiques :**
- Utiliser des descriptions riches avec HTML
- Optimiser les images (ratio, taille)
- Définir une séquence logique
- Configurer les produits liés pour l'upsell

---

## USE CASE 2 : CONFIGURATION BOUTIQUE

### Modèle : website

**Champs clés configuration :**
- `salesperson_id/salesteam_id` : Commercial et équipe par défaut
- `show_line_subtotals_tax_selection` : Affichage TTC/HT
- `shop_ppg/shop_ppr` : Produits par page/par ligne
- `shop_default_sort` : Tri par défaut
- `add_to_cart_action` : Action après ajout panier
- `account_on_checkout` : Gestion comptes clients
- `prevent_zero_price_sale` : Masquer prix zéro
- `cart_abandoned_delay` : Délai panier abandonné

**Workflow configuration :**
1. **Accès configuration** : Site Web > Configuration > Paramètres
2. **Section E-commerce** :
   - Commercial par défaut
   - Équipe de vente
   - Affichage prix (TTC/HT)
3. **Boutique** :
   - Nombre produits par page (défaut : 20)
   - Colonnes grille (défaut : 4)
   - Tri par défaut
4. **Processus checkout** :
   - Comptes obligatoires/optionnels/désactivés
   - Action après ajout panier
5. **Marketing** :
   - Email panier abandonné
   - Délai avant envoi

**Menu principal :** Site Web > Configuration > Paramètres

**Pièges courants :**
- Oublier de configurer les taxes → prix incorrects
- Mauvais paramétrage grille → UX dégradée
- Email panier abandonné mal configuré → perte ventes

**Bonnes pratiques :**
- Tester les différents affichages prix
- Adapter grille selon type produits
- Configurer emails transactionnels
- Définir processus checkout selon cible (B2B/B2C)

---

## USE CASE 3 : GESTION COMMANDES E-COMMERCE

### Modèle : sale.order

**Champs clés e-commerce :**
- `website_order_line` : Lignes affichées sur le site
- `cart_quantity` : Quantité totale panier
- `only_services` : Commande uniquement services
- `is_abandoned_cart` : Panier abandonné
- `website_id` : Site web origine
- `amount_delivery` : Montant livraison
- `access_point_address` : Adresse point relais

**Workflow commande :**
1. **Création automatique** : Dès premier ajout au panier
2. **État "draft"** : Panier en cours
3. **Enrichissement** : Ajout/suppression produits
4. **Processus checkout** :
   - Informations client
   - Adresses livraison/facturation
   - Mode de livraison
   - Moyen de paiement
5. **Confirmation** : Passage à "sale" après paiement
6. **Traitement** : Préparation, expédition, facturation

**Calculs spécifiques :**
- Quantité panier : somme lignes visibles sur site
- Détection panier abandonné : délai configurable
- Montant livraison : TTC/HT selon configuration

**Menu principal :** Ventes > Commandes > Devis

**Pièges courants :**
- Paniers non nettoyés → base polluée
- Mauvaise gestion des abandons → emails spam
- Calculs livraison incorrects → mécontentement client

**Bonnes pratiques :**
- Automatiser nettoyage paniers expirés
- Segmenter emails selon comportement
- Valider calculs taxes/livraison
- Tracer origine commandes (website_id)

---

## USE CASE 4 : FILTRES ET SNIPPETS PRODUITS

### Modèle : website.snippet.filter

**Fonctionnalités disponibles :**
- `_get_products_latest_sold` : Derniers vendus
- `_get_products_latest_viewed` : Derniers consultés  
- `_get_products_recently_sold_with` : Cross-selling
- `product_cross_selling` : Filtre cross-sell

**Types de filtres :**
1. **Produits populaires** : Basé sur ventes
2. **Derniers consultés** : Par visiteur
3. **Cross-selling** : Produits complémentaires
4. **Nouveautés** : Par date création

**Workflow utilisation :**
1. **Éditeur site** : Glisser snippet "Produits dynamiques"
2. **Configuration snippet** :
   - Type de filtre
   - Nombre produits
   - Template affichage
3. **Critères** : Catégories, tags, prix...
4. **Personnalisation** : CSS, mise en page

**Menu principal :** Site Web > Aller au site web > Éditer

**Pièges courants :**
- Filtres sans résultats → zones vides
- Trop de produits → performance
- Mauvais ciblage → pertinence faible

**Bonnes pratiques :**
- Tester filtres avec données réelles
- Limiter nombre produits affichés
- Utiliser cache pour performance
- Adapter selon audience cible

---

## USE CASE 5 : CONFIGURATION AVANCÉE

### Modèle : res.config.settings

**Paramètres principaux :**
- `module_website_sale_wishlist` : Liste souhaits
- `module_website_sale_comparison` : Comparateur
- `group_product_price_comparison` : Prix de comparaison
- `enabled_extra_checkout_step` : Étape supplémentaire checkout
- `enabled_buy_now_button` : Bouton "Acheter maintenant"

**Extensions disponibles :**
1. **Wishlist** : Listes de souhaits clients
2. **Comparateur** : Comparaison produits
3. **Autocomplétion** : Adresses automatiques
4. **Point relais** : Mondial Relay
5. **Facturation** : Module comptabilité

**Workflow activation :**
1. **Apps** : Rechercher module souhaité
2. **Installation** : Cliquer "Installer"
3. **Configuration** : Site Web > Configuration > Paramètres
4. **Activation fonctionnalités** : Cocher options désirées
5. **Sauvegarde** : Appliquer changements

**Menu principal :** Apps ou Site Web > Configuration > Paramètres

**Pièges courants :**
- Modules incompatibles → erreurs
- Surcharge fonctionnalités → complexité
- Oubli configuration → fonctionnalités inactives

**Bonnes pratiques :**
- Installer progressivement
- Tester avant mise en production
- Former utilisateurs aux nouvelles fonctions
- Documenter configurations spécifiques

---

## POINTS D'ATTENTION TRANSVERSES

### Sécurité
- Validation données saisies
- Contrôle accès selon profils
- Protection contre attaques (CSRF, XSS)

### Performance  
- Cache intelligents
- Optimisation requêtes base
- Images optimisées
- CDN pour ressources statiques

### SEO
- URLs optimisées (slug)
- Métadonnées produits
- Structured data
- Plan de site automatique

### Intégrations
- ERP (stock, compta)
- CRM (leads, opportunités) 
- Logistique (transporteurs)
- Paiement (PSP, banques)

Ce module website_sale constitue le cœur du e-commerce Odoo avec une architecture modulaire permettant d'adapter finement l'expérience selon les besoins métier.