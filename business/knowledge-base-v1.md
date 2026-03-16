# OdooAI — Knowledge Base v1
## Support Engineer (41) + Customer Success (17)
## Date : 2026-03-21

---

## Structure

### Categorie 1 — Demarrage
| # | Article | Source |
|---|---------|--------|
| 1 | Qu'est-ce qu'OdooAI ? | FAQ #1 |
| 2 | Comment me connecter ? | FAQ #2 |
| 3 | Comment creer une cle API Odoo ? | FAQ #3 |
| 4 | Guide de demarrage en 5 minutes | guide-utilisateur-5min.md |
| 5 | Versions Odoo supportees | FAQ #4 |

### Categorie 2 — Fonctionnalites
| # | Article | Source |
|---|---------|--------|
| 6 | Que peut faire OdooAI ? | FAQ #6 |
| 7 | Les 9 domaines couverts | FAQ #7 |
| 8 | Comment fonctionne la connexion live ? | Nouveau |
| 9 | OdooAI peut-il modifier mes donnees ? | FAQ #8 |
| 10 | Utiliser OdooAI sans connexion Odoo | FAQ #10 |

### Categorie 3 — Securite & Confidentialite
| # | Article | Source |
|---|---------|--------|
| 11 | Mes donnees sont-elles en securite ? | FAQ #11 |
| 12 | Quelles donnees sont envoyees a l'IA ? | FAQ #12 |
| 13 | Comment fonctionne l'anonymisation ? | Nouveau |
| 14 | Politique de confidentialite | privacy-policy-draft.md |

### Categorie 4 — Plans & Facturation
| # | Article | Source |
|---|---------|--------|
| 15 | Les plans et tarifs | FAQ #14 |
| 16 | Changer de plan | FAQ #16 |
| 17 | Periode d'essai et beta | FAQ #15 |

### Categorie 5 — Troubleshooting
| # | Article | Source |
|---|---------|--------|
| 18 | La connexion Odoo echoue | FAQ #17 |
| 19 | La reponse est vide ou courte | FAQ #18 |
| 20 | Les reponses ne correspondent pas | FAQ #19 |

---

## Articles nouveaux (pas dans la FAQ)

### Article 8 — Comment fonctionne la connexion live ?

Quand vous connectez votre Odoo, OdooAI :
1. Detecte automatiquement la version (17, 18, 19) et le protocole (XML-RPC ou JSON-RPC)
2. Verifie vos credentials
3. Liste les modules installes sur votre instance
4. Peut ensuite interroger vos donnees en temps reel

La connexion est en lecture seule. OdooAI ne modifie jamais rien.

Vos credentials restent en memoire de session — ils ne sont jamais stockes.

### Article 13 — Comment fonctionne l'anonymisation ?

Le Security Guardian anonymise automatiquement les donnees sensibles AVANT qu'elles soient envoyees a l'IA :

| Type de donnee | Avant | Apres |
|---------------|-------|-------|
| Nom employe | Marie Dupont | M*** D*** |
| Email | marie@acme.fr | m***@a***.fr |
| Telephone | +33 6 12 34 56 78 | +** * ** ** ** ** |
| Salaire | 3 850€ | ~3 900€ (arrondi) |
| Mot de passe | *** | [SUPPRIME] |

Les modeles systeme (ir.rule, res.users) sont completement bloques — l'IA n'y a jamais acces.

---

## Integration prevue (Sprint 6)
- Page `/help` sur le site web
- Recherche dans la KB depuis le chat ("aide connexion" → article #2)
- In-app tooltips sur les boutons
