# Module Website Odoo 17 - Description Métier Complète

## Vue d'ensemble du module

Le module **Website** d'Odoo 17 est le cœur du système de gestion de sites web multi-sites. Il permet de créer, gérer et personnaliser des sites web avec un système complet de gestion des visiteurs, des pages, des vues et du routage.

---

## USE CASE 1 : Gestion Multi-Sites (Website)

### Modèle : `website`

**Champs clés :**
- `name` : Nom du site web (requis)
- `domain` : Domaine du site (ex: https://www.mondomaine.com)
- `company_id` : Entreprise associée
- `language_ids` : Langues disponibles sur le site
- `default_lang_id` : Langue par défaut
- `auto_redirect_lang` : Redirection automatique selon la langue du navigateur
- `user_id` : Utilisateur public du site
- `menu_id` : Menu principal (calculé)
- `homepage_url` : URL de la page d'accueil personnalisée

**Workflow complet :**
1. **Création d'un site** : Aller dans **Site Web > Configuration > Sites Web > Créer**
2. Définir le nom et domaine
3. Sélectionner la compagnie
4. Configurer les langues disponibles
5. Définir l'utilisateur public
6. **Activation** : Le site devient accessible

**Menu Odoo :** `Site Web > Configuration > Sites Web`

**Pièges courants :**
- ⚠️ L'utilisateur public doit avoir les droits appropriés
- ⚠️ Le domaine doit être unique si défini
- ⚠️ Au moins une langue doit être sélectionnée

**Bonnes pratiques :**
- ✅ Utiliser des noms de sites descriptifs
- ✅ Configurer le CDN pour les performances (`cdn_activated`, `cdn_url`)
- ✅ Définir une page d'accueil personnalisée via `homepage_url`

---

## USE CASE 2 : Gestion des Vues Website-Specific (ir.ui.view)

### Modèle : `ir.ui.view` (héritage)

**Champs clés spécifiques website :**
- `website_id` : Site web associé (si spécifique à un site)
- `page_ids` : Pages utilisant cette vue
- `track` : Activer le tracking des visites
- `visibility` : Visibilité ('', 'connected', 'restricted_group', 'password')
- `visibility_password` : Mot de passe si visibilité protégée
- `first_page_id` : Première page liée (calculé)

**Workflow complet (COW - Copy On Write) :**
1. **Édition d'une vue générique** depuis un contexte website
2. Le système détecte `website_id` dans le contexte
3. **Création automatique** d'une copie spécifique au site
4. L'édition s'applique uniquement à la copie spécifique
5. Les autres sites gardent la vue générique

**Menu Odoo :** `Site Web > Configuration > Vues`

**Pièges courants :**
- ⚠️ Le COW ne fonctionne que si `website_id` est dans le contexte
- ⚠️ Les vues orphelines peuvent s'accumuler
- ⚠️ Le champ `key` doit être unique par vue

**Bonnes pratiques :**
- ✅ Utiliser le contexte `no_cow=True` pour éviter la duplication
- ✅ Nettoyer régulièrement les vues spécifiques inutilisées
- ✅ Préfixer les clés des vues personnalisées

---

## USE CASE 3 : Tracking des Visiteurs (website.visitor)

### Modèle : `website.visitor`

**Champs clés :**
- `access_token` : Token unique d'identification (hash ou partner_id)
- `website_id` : Site web visité
- `partner_id` : Contact associé (si utilisateur connecté)
- `country_id` : Pays du visiteur
- `lang_id` : Langue du visiteur
- `visit_count` : Nombre de visites
- `last_connection_datetime` : Dernière connexion
- `is_connected` : Connecté actuellement (calculé)

**Workflow complet :**
1. **Arrivée sur le site** : Création automatique du visiteur
2. **Génération du token** : Hash basé sur IP + User-Agent + Session
3. **Tracking des pages** : Création d'enregistrements `website.track`
4. **Connexion utilisateur** : Association avec `partner_id`
5. **Mise à jour automatique** : Pays, langue, dernière visite

**Menu Odoo :** `Site Web > Rapports > Visiteurs`

**Pièges courants :**
- ⚠️ Les visiteurs ne peuvent être créés que depuis le frontend
- ⚠️ Le token doit être unique (contrainte SQL)
- ⚠️ Nettoyage périodique nécessaire pour éviter l'accumulation

**Bonnes pratiques :**
- ✅ Configurer des tâches cron pour nettoyer les anciens visiteurs
- ✅ Utiliser les statistiques pour analyser le comportement
- ✅ Respecter le RGPD pour la collecte de données

---

## USE CASE 4 : Tracking des Pages Visitées (website.track)

### Modèle : `website.track`

**Champs clés :**
- `visitor_id` : Visiteur concerné (requis)
- `page_id` : Page visitée (si page Odoo)
- `url` : URL visitée
- `visit_datetime` : Date/heure de la visite

**Workflow complet :**
1. **Navigation sur une page** : Détection automatique
2. **Enregistrement du track** : Création de l'enregistrement
3. **Association au visiteur** : Lien avec `website.visitor`
4. **Mise à jour des statistiques** : Compteurs sur le visiteur

**Menu Odoo :** Accessible via le visiteur (`website.visitor`)

**Pièges courants :**
- ⚠️ Peut générer beaucoup de données rapidement
- ⚠️ Les bots peuvent créer des faux tracks
- ⚠️ Performance impactée si pas d'indexes

**Bonnes pratiques :**
- ✅ Nettoyer régulièrement les anciens tracks
- ✅ Filtrer les bots via `ir.http.is_a_bot()`
- ✅ Utiliser des index sur les champs de recherche

---

## USE CASE 5 : Gestion des Thèmes (ir.module.module)

### Modèle : `ir.module.module` (héritage)

**Champs clés spécifiques :**
- `image_ids` : Screenshots du thème
- `is_installed_on_current_website` : Installé sur le site actuel

**Workflow d'installation de thème :**
1. **Sélection du thème** : Via l'interface ou installation module
2. **Détection du préfixe** : Module commençant par `theme_`
3. **Chargement automatique** : `_theme_load()` pour chaque site concerné
4. **Copie des templates** : Vues, menus, pages, assets
5. **Activation** : Le thème devient actif

**Menu Odoo :** `Applications > Thèmes` ou `Site Web > Configuration > Thèmes`

**Workflow de mise à jour :**
- **Interface web** : Mise à jour du site courant uniquement
- **Ligne de commande (-u)** : Mise à jour de tous les sites utilisant le thème

**Pièges courants :**
- ⚠️ Les dépendances entre thèmes peuvent créer des conflits
- ⚠️ La mise à jour peut écraser les personnalisations
- ⚠️ Les traductions peuvent être perdues lors des mises à jour

**Bonnes pratiques :**
- ✅ Tester les thèmes sur un environnement de développement
- ✅ Sauvegarder avant d'appliquer un thème
- ✅ Utiliser l'héritage de vues pour les personnalisations

---

## USE CASE 6 : Routage et Redirections (ir.http)

### Modèle : `ir.http` (héritage)

**Fonctionnalités clés :**
- Gestion du routage multi-sites
- Support des redirections 308 et 404
- Gestion des URLs slugifiées
- Cache du routage par site

**Workflow de routage :**
1. **Requête entrante** : Détection du site via domaine
2. **Construction des règles** : `_generate_routing_rules()` avec redirections
3. **Application des rewrites** : Via `website.rewrite`
4. **Résolution de la route** : Endpoint final

**Menu Odoo :** `Site Web > Configuration > Redirections`

**Types de redirections :**
- **308** : Redirection permanente vers nouvelle URL
- **404** : Retour d'erreur 404 pour l'URL

**Pièges courants :**
- ⚠️ Les redirections en boucle peuvent planter le site
- ⚠️ Cache du routage peut masquer les changements
- ⚠️ Les slugs doivent être uniques

**Bonnes pratiques :**
- ✅ Tester les redirections avant mise en production
- ✅ Nettoyer le cache de routage après modifications
- ✅ Utiliser des URLs SEO-friendly avec slugs

---

## Configuration et Optimisation

### Champs de configuration avancée (`website`) :

**SEO et Analytics :**
- `google_analytics_key` : Clé Google Analytics
- `google_search_console` : Console de recherche Google
- `plausible_shared_key` / `plausible_site` : Analytics Plausible

**Réseaux sociaux :**
- `social_twitter`, `social_facebook`, `social_linkedin`, etc.
- `social_default_image` : Image par défaut pour partage social

**Performance :**
- `cdn_activated` : Activation du CDN
- `cdn_url` : URL de base du CDN  
- `cdn_filters` : Filtres d'URLs pour le CDN

**Sécurité :**
- `cookies_bar` : Barre de cookies pour conformité RGPD

Cette architecture modulaire permet une gestion complète et scalable de sites web multiples avec un tracking avancé des visiteurs et une personnalisation poussée par site.