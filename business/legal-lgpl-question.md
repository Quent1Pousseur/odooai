# Question Juridique — LGPL et Extraction de Code Source Odoo

## Auteur : Legal & Compliance (16)
## Date : 2026-03-16
## Status : A SOUMETTRE A UN AVOCAT

---

## Contexte

OdooAI est un produit commercial SaaS closed source. Il utilise un "Code Analyst" (parseur AST Python + XML) pour extraire des informations structurelles du code source d'Odoo, qui est distribue sous licence LGPL v3.

### Ce que fait le Code Analyst
1. Parse le code source Python via `ast.parse()` (pas d'execution de code)
2. Extrait des **faits structurels** : noms de modeles, types de champs, noms de methodes, contraintes SQL, structure des vues XML
3. Stocke ces faits dans des fichiers JSON (Knowledge Graphs)
4. Les Knowledge Graphs sont ensuite utilises par un LLM pour generer des conseils business

### Ce que le Code Analyst NE fait PAS
- Ne copie PAS le code source (pas de reproduction du code)
- N'execute PAS le code Odoo
- Ne distribue PAS le code Odoo aux utilisateurs
- Ne link PAS avec le code Odoo (pas de dependance runtime)
- Ne modifie PAS le code Odoo

## Question juridique

**L'extraction systematique d'informations structurelles (noms de modeles, types de champs, interfaces API) depuis du code source LGPL v3, pour les stocker dans un format proprietaire (JSON) et les utiliser dans un produit commercial closed source, constitue-t-elle une oeuvre derivee au sens de la LGPL ?**

## Analyse preliminaire

### Arguments en faveur de la legalite
1. **Les faits ne sont pas protegeables par le copyright** : les noms de modeles (`sale.order`), les types de champs (`Char`, `Many2one`), et les structures (heritage, contraintes) sont des faits, pas des expressions creatives.

2. **Precedent Oracle v Google (2021)** : la Cour Supreme US a juge que la reimplementation d'interfaces API (declarations de fonctions) etait un fair use. Les Knowledge Graphs sont analogues a des descriptions d'interfaces.

3. **La LGPL autorise l'utilisation sans contamination** : la LGPL v3 section 5 autorise les "Combined Works" qui linkent avec une bibliotheque LGPL sans devenir LGPL elles-memes. OdooAI ne link meme pas avec Odoo.

4. **Pas de reproduction du code** : le Code Analyst produit des JSON structurels, pas une copie du code. C'est comparable a un index ou un catalogue.

5. **Pratique courante** : les IDE, linters, et outils d'analyse statique parsent du code LGPL/GPL sans etre consideres comme des oeuvres derivees.

### Arguments contre (risques)
1. **Pas de precedent exact** : l'extraction systematique et commerciale de l'ensemble du code source d'un produit LGPL pour un concurrent commercial n'a pas de precedent clair.

2. **Odoo SA pourrait argumenter** : la LGPL protege le "work based on the Library" — si les KG sont consideres comme bases sur le code source, ils pourraient etre contestes.

3. **Volume d'extraction** : parser 1218 modules complets pourrait etre vu comme une extraction substantielle, meme si chaque fait individuel n'est pas protegeable (doctrine des bases de donnees en droit europeen).

4. **Droit sui generis des bases de donnees (UE)** : le code source d'Odoo pourrait etre considere comme une "base de donnees" protegee par le droit sui generis, et l'extraction systematique pourrait violer ce droit.

## Recommandations

1. **Consulter un avocat specialise en open source et propriete intellectuelle** — priorite P0
2. **Ne pas distribuer les Knowledge Graphs** aux utilisateurs (les garder cote serveur)
3. **Documenter que les KG sont des faits structurels**, pas des copies de code
4. **Ajouter un disclaimer** : "OdooAI n'est pas affilie a Odoo SA. Les informations sur les modules Odoo sont extraites d'analyses structurelles du code source open source."
5. **Preparer un plan B** : si un avocat deconseille l'extraction du code Enterprise, se limiter au code Community (disponible sur GitHub sous LGPL)

---

## Disclaimer Systeme AI (co-redige avec AI Safety 33)

### Disclaimer legal (a afficher dans l'UI et les CGU)
```
OdooAI est un outil d'assistance. Il ne se substitue pas a un
consultant professionnel.

- OdooAI ne fournit pas de conseil juridique, fiscal ou comptable.
- Les recommandations sont basees sur l'analyse du code source Odoo
  et peuvent ne pas refleter votre configuration specifique.
- Toute modification de votre instance Odoo est sous votre
  responsabilite. OdooAI applique une double validation avant
  chaque action.
- OdooAI n'est pas affilie a Odoo SA.
```

### Disclaimer technique (dans le system prompt du LLM)
```
Tu es un assistant specialise Odoo. Tu NE fournis PAS de conseil
juridique, fiscal ou comptable. Si l'utilisateur demande un conseil
dans ces domaines, reponds : "Je ne suis pas habilite a fournir ce
type de conseil. Consultez un professionnel qualifie."

Cite toujours la source de tes recommandations (module, champ,
documentation). Si tu n'es pas sur, dis-le explicitement.
```

> **AI Safety (33)** : "Le disclaimer dans le system prompt est critique. Sans lui, le LLM pourrait donner des conseils fiscaux qui engagent notre responsabilite."
>
> **Legal (16)** : "Le disclaimer doit etre visible AVANT la premiere utilisation, pas enterre dans les CGU. Proposition : ecran d'acceptation au premier login."
