# OdooAI — Politique de Confidentialite (DRAFT)

## Auteur : Legal & Compliance (16)
## Date : 2026-03-18
## Status : DRAFT v2 — reviewed 2026-03-21 — a valider par un avocat

---

## 1. Qui sommes-nous

OdooAI est un service d'assistance IA pour les utilisateurs d'Odoo, edite par [NOM SOCIETE A CREER].
OdooAI n'est PAS affilie a Odoo SA.

## 2. Donnees collectees

### Donnees de compte
- Email, nom (lors de l'inscription, Phase 2)
- Plan d'abonnement

### Donnees de connexion Odoo
- URL de l'instance Odoo
- Nom de la base de donnees
- Login Odoo
- Cle API Odoo (chiffree AES-256-GCM au repos)

### Donnees metier (transitoires)
- Questions posees par l'utilisateur
- Reponses Odoo (read-only, jamais modifiees sauf accord explicite)
- Les donnees metier sont **anonymisees** par le Security Guardian avant traitement par l'IA
- Les donnees metier ne sont **PAS stockees** de maniere permanente (Phase 1)

### Donnees techniques
- Logs d'acces (IP, timestamp, modele Odoo consulte)
- Tokens LLM consommes

## 3. Comment nous utilisons vos donnees

| Donnee | Utilisation | Duree de conservation |
|--------|------------|----------------------|
| Credentials Odoo | Connexion a votre instance | Session uniquement (Phase 1) |
| Questions utilisateur | Envoyees a l'IA pour generer une reponse | Non conservees (Phase 1) |
| Donnees Odoo lues | Anonymisees puis envoyees a l'IA | Non conservees |
| Logs d'acces | Securite et audit | 90 jours |

## 4. Sous-traitants

| Sous-traitant | Donnees partagees | Finalite | Localisation |
|---------------|-------------------|----------|-------------|
| Anthropic (Claude) | Questions + donnees Odoo anonymisees | Generation de reponses IA | USA |
| Hebergeur (a definir) | Toutes donnees | Infrastructure | EU (prevu) |

**Note RGPD** : Le transfert de donnees vers Anthropic (USA) necessite des clauses contractuelles types (CCT) ou un mecanisme adequat. A valider avec un avocat.

## 5. Securite

- Chiffrement AES-256-GCM pour les credentials au repos
- TLS pour toutes les communications
- Anonymisation automatique des donnees sensibles (montants, emails, noms)
- Modeles Odoo bloques : ir.rule, res.users, res.groups (jamais exposes)
- Audit log de chaque acces
- Aucun stockage de mot de passe Odoo (uniquement cle API)

## 6. Vos droits (RGPD)

- **Acces** : vous pouvez demander quelles donnees nous avons sur vous
- **Rectification** : vous pouvez demander la correction de donnees erronees
- **Suppression** : vous pouvez demander la suppression de votre compte et donnees
- **Portabilite** : vous pouvez demander l'export de vos donnees
- **Opposition** : vous pouvez vous opposer au traitement a tout moment

Contact : privacy@odooai.com (a creer)

## 7. Cookies

Phase 1 : aucun cookie. Phase 2 : cookie de session uniquement (fonctionnel, pas de tracking).

## 8. Disclaimer AI

OdooAI est un outil d'assistance. Il ne se substitue pas a un consultant professionnel.
- OdooAI ne fournit pas de conseil juridique, fiscal ou comptable
- Les recommandations sont basees sur l'analyse du code source Odoo
- Toute modification de votre instance est sous votre responsabilite
- Double validation obligatoire avant chaque action d'ecriture

## 9. Modifications

Cette politique peut etre mise a jour. Les utilisateurs seront informes par email.
Derniere mise a jour : 2026-03-21 (DRAFT v2 — reviewed by Security Arch + Legal).

## 10. Conversations

Les conversations (questions et reponses) sont stockees dans une base de donnees locale.
- Les conversations ne sont PAS partagees entre utilisateurs
- Les conversations ne sont PAS utilisees pour entrainer des modeles IA
- La suppression des conversations sera disponible dans une prochaine version
- En attendant, les conversations peuvent etre supprimees sur demande a privacy@odooai.com

---

> **Note Legal (16)** : Ce draft couvre les bases RGPD mais necessite une validation par un avocat specialise en droit du numerique, notamment pour le transfert de donnees vers Anthropic (USA) et la responsabilite en cas de recommandation IA erronee.
