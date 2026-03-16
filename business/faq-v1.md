# OdooAI — FAQ v1 (20 questions)
## Redige par : Support Eng (41) + Customer Success (17)
## Valide par : Odoo Expert (10), Prompt Eng (25), Security Arch (07)
## Date : 2026-03-20

---

## Demarrage

### 1. Qu'est-ce qu'OdooAI ?
OdooAI est un Business Analyst IA qui connait chaque fonctionnalite d'Odoo. Il se connecte a votre instance, analyse votre configuration, et vous montre ce que vous n'utilisez pas — avec des recommandations concretes.

### 2. Comment me connecter ?
Ouvrez OdooAI, cliquez sur "Connecter Odoo" dans le header, et renseignez :
- L'URL de votre instance (ex: https://mon-odoo.com)
- Le nom de votre base de donnees
- Votre login (email)
- Votre cle API Odoo

### 3. Comment creer une cle API Odoo ?
Dans votre Odoo : Parametres → Utilisateurs → votre profil → onglet "Preferences" ou "Securite" → Cles API → Nouvelle cle API. Donnez un nom (ex: "OdooAI") et copiez la cle generee. Cette cle remplace votre mot de passe pour les connexions API.

### 4. Quelles versions d'Odoo sont supportees ?
OdooAI supporte Odoo 17, 18 et 19 (Community et Enterprise). La detection de version est automatique — XML-RPC pour 17/18, JSON-RPC 2.0 pour 19+.

### 5. OdooAI fonctionne-t-il avec Odoo Community ?
Oui. OdooAI analyse les modules installes sur votre instance, qu'ils soient Community ou Enterprise. Les recommandations s'adaptent aux modules disponibles.

---

## Fonctionnalites

### 6. Que peut faire OdooAI ?
- Analyser votre configuration Odoo et identifier les fonctionnalites non utilisees
- Repondre a vos questions sur les modules Odoo (vente, stock, comptabilite, RH, etc.)
- Proposer des optimisations basees sur votre configuration reelle
- Fournir des statistiques sur vos donnees (nombre de commandes, factures impayees, etc.)

### 7. Quels domaines sont couverts ?
9 domaines : Vente & CRM, Supply Chain (stock + achats), Fabrication, Comptabilite, RH & Paie, Projets & Services, Helpdesk, E-commerce, Point de Vente.

### 8. OdooAI peut-il modifier mes donnees ?
Non. OdooAI fonctionne en **lecture seule**. Il ne peut ni creer, ni modifier, ni supprimer de donnees dans votre Odoo. C'est un choix de securite — l'IA observe et recommande, elle n'agit pas.

### 9. L'IA peut-elle se tromper ?
Oui. Comme tout systeme d'IA, OdooAI peut parfois donner des reponses imprecises ou incompletes. C'est pourquoi :
- Chaque reponse cite ses sources (module, modele, champ)
- Un disclaimer rappelle de ne pas suivre aveuglément les conseils
- OdooAI ne fournit JAMAIS de conseil juridique, fiscal ou comptable

### 10. Puis-je utiliser OdooAI sans connecter mon Odoo ?
Oui. Sans connexion, OdooAI repond avec ses connaissances generales sur Odoo (basees sur l'analyse de 1218 modules). Les reponses sont pertinentes mais pas personnalisees a votre configuration.

---

## Securite

### 11. Mes donnees sont-elles en securite ?
Oui. OdooAI integre un Security Guardian qui :
- **Bloque** l'acces aux modeles systeme sensibles (ir.rule, ir.config_parameter)
- **Anonymise** les donnees sensibles (RH, salaires) avant traitement
- **Valide** chaque requete pour prevenir les injections
- **Ne stocke PAS** vos credentials Odoo — ils restent en memoire de session uniquement

### 12. Mes donnees sont-elles envoyees a un tiers ?
Les donnees de votre Odoo sont envoyees a l'API Anthropic (Claude) pour generer les reponses. Anthropic ne stocke pas les donnees des requetes API et ne les utilise pas pour entrainer ses modeles. Les donnees sensibles (RH, salaires) sont anonymisees AVANT l'envoi.

### 13. Qui peut acceder a mon OdooAI ?
Actuellement, OdooAI fonctionne en session locale. Un systeme d'authentification utilisateur (email + mot de passe) est prevu pour la version beta publique.

---

## Tarification

### 14. Combien coute OdooAI ?
Trois plans :
- **Starter** : 49€/mois — 100 requetes, 1 connexion Odoo
- **Professional** : 149€/mois — 500 requetes, 1 connexion, recommandations avancees
- **Enterprise** : 399€/mois — illimite*, 3 connexions, support prioritaire

*Fair use policy

### 15. Y a-t-il une periode d'essai ?
Une beta privee est en cours. Inscrivez-vous sur notre landing page pour obtenir un acces anticipe gratuit.

### 16. Puis-je changer de plan ?
Oui, a tout moment. L'upgrade est immediat, le downgrade prend effet a la fin du cycle de facturation.

---

## Troubleshooting

### 17. La connexion Odoo echoue
Verifiez que :
- L'URL est correcte et accessible (testez dans votre navigateur)
- Le nom de la base de donnees est exact
- Vous utilisez une **cle API** (pas votre mot de passe)
- Votre instance Odoo est demarree et accessible depuis votre machine

### 18. La reponse est vide ou tres courte
Cela peut arriver si le serveur IA est temporairement surcharge. Reessayez apres quelques secondes. Si le probleme persiste, posez la question differemment ou de maniere plus specifique.

### 19. Les reponses ne correspondent pas a mon Odoo
Assurez-vous que votre Odoo est connecte (indicateur vert dans le header). Sans connexion, OdooAI repond avec des connaissances generales, pas les donnees de votre instance.

### 20. Puis-je supprimer mes conversations ?
Les conversations sont stockees localement. La suppression de l'historique sera disponible dans une prochaine version. En attendant, les conversations ne sont pas partagees et ne sont accessibles que depuis votre session.

---

*Derniere mise a jour : 2026-03-20*
