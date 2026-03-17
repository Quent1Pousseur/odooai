# Analyse LGPL — Les Knowledge Graphs sont-ils du "derived work" ?
## Redige par : Legal & Compliance (16) + CTO (02)
## Date : 2026-03-20
## Status : POSITION PRELIMINAIRE — a confirmer avec un avocat

---

## Question

OdooAI parse le code source d'Odoo (licence LGPL-3.0) pour generer des Knowledge Graphs (JSON). Ces KG sont-ils du "derived work" au sens de la LGPL ?

## Contexte

- Odoo Community est sous licence **LGPL-3.0**
- OdooAI parse les fichiers Python et XML d'Odoo avec un analyseur AST
- Le resultat est un Knowledge Graph JSON contenant : noms de modeles, noms de champs, types, contraintes, vues, menus
- Le KG ne contient PAS de code executable Odoo
- OdooAI est closed-source

## Analyse

### Ce que dit la LGPL-3.0

La LGPL-3.0 autorise :
- L'utilisation du logiciel sans restriction
- La creation de "works that use the Library" (applications qui UTILISENT la lib, pas qui la copient)
- L'analyse du code source (reverse engineering explicitement autorise par la LGPL)

La LGPL impose des obligations quand on cree un "derivative work" :
- Un derivative work = une oeuvre basee sur le code source, contenant du code modifie ou copie
- L'obligation est de distribuer le derivative work sous LGPL

### Les Knowledge Graphs sont-ils du derivative work ?

**Notre position : NON.** Voici pourquoi :

1. **Pas de code copie** — Les KG ne contiennent aucune ligne de code Odoo. Ils contiennent des METADONNEES : noms de modeles (`sale.order`), noms de champs (`amount_total`), types (`monetary`). Ce sont des faits, pas du code.

2. **Analogie de l'index** — Un index de livre n'est pas le livre. Un catalogue de bibliotheque n'est pas les livres qu'il reference. Les KG sont un index du code Odoo, pas le code lui-meme.

3. **Precedent : APIs ne sont pas copyrightable** — Arret Google v. Oracle (US Supreme Court, 2021) : les interfaces API sont du "fair use". Les noms de modeles et de champs Odoo sont des interfaces, pas de l'implementation.

4. **Pas de code executable** — Les KG sont du JSON statique. Ils ne peuvent pas etre executes. Ils ne remplacent pas Odoo et ne permettent pas de se passer d'Odoo.

5. **LGPL autorise l'analyse** — La section 3 de la LGPL-3.0 autorise explicitement le reverse engineering pour comprendre le fonctionnement du logiciel.

### Risques residuels

| Risque | Probabilite | Impact | Mitigation |
|--------|------------|--------|------------|
| Odoo SA conteste | Faible | Eleve | Avocat + dialogue preventif |
| Tribunal considere les KG comme derivative | Tres faible | Eleve | Precedent Google v. Oracle |
| Confusion de marque "OdooAI" | Moyen | Moyen | Disclaimer + renommage si necessaire |

### Precedents et references

- **Google v. Oracle (2021)** — Les API Java ne sont pas copyrightable. Fair use pour la reimplementation. Par analogie, les noms de modeles/champs Odoo sont des interfaces.
- **Computer Associates v. Altai (1992)** — Le "filtration test" separe les idees (non protegees) du code (protege). Les noms de modeles sont des idees, pas du code.
- **LGPL-3.0 section 3** — Droit explicite au reverse engineering.

## Recommandations

### Court terme (maintenant)
1. **Ne PAS retarder le lancement** — le risque est faible
2. **Disclaimer explicite** : "OdooAI n'est pas affilie a Odoo SA. Les Knowledge Graphs sont des index de metadonnees, pas du code source."
3. **Ne JAMAIS inclure de code executable Odoo** dans les KG — uniquement des metadonnees

### Moyen terme
4. **Consulter un avocat** specialise en propriete intellectuelle et licences open source
5. **Envisager un dialogue preventif** avec Odoo SA — mieux vaut prevenir qu'etre surpris
6. **Preparer un plan B** : si LGPL problematique, generer les KG via l'API Odoo (pas le code source). C'est plus lent mais elimine tout risque LGPL.

### A NE JAMAIS FAIRE
- Copier du code Odoo dans les KG ou le produit
- Distribuer du code Odoo modifie
- Pretendre etre affilie a Odoo SA
- Utiliser le logo Odoo

## Conclusion

**Risque global : FAIBLE.** Les Knowledge Graphs sont des metadonnees extraites, pas du code derive. Mais une validation juridique formelle est recommandee avant la beta publique.

---

*A valider par un avocat specialise en propriete intellectuelle et licences open source.*
