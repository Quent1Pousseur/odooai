# Learning — Odoo Expert (10) — Parsing Odoo Workflow Transitions (State Machines)
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **Odoo n'utilise plus `workflow` depuis v11** : les anciens workflows XML (wkf, wkf_activity, wkf_transition) ont ete supprimes. Depuis Odoo 11+, toute la logique de transitions est dans les champs `state` (Selection field) avec des methodes `action_confirm()`, `action_done()`, etc. Le parsing doit cibler le code Python, pas du XML.

2. **Les patterns de state machine dans Odoo 17 sont repetitifs** : un champ `state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')])` suivi de methodes qui font `self.write({'state': 'confirmed'})`. Les transitions valides sont implicites dans le code des methodes, pas declarees explicitement.

3. **Les boutons XML declarent les transitions visibles** : dans les vues form, les `<button>` avec `states="draft"` et `name="action_confirm"` donnent le graphe des transitions accessibles par l'utilisateur. Croiser les vues XML et le code Python donne le state machine complet.

4. **Certains modules utilisent des patterns avances** : `mail.thread` ajoute des tracking sur les changements de state. `base.automation` peut declencher des actions sur changement de state. Les `@api.constrains` bloquent certaines transitions invalides.

5. **L'AST Python permet d'extraire les transitions automatiquement** : en parsant les methodes `action_*` avec `ast.parse()`, on peut detecter les `self.write({'state': ...})` et les conditions `if self.state == ...` pour reconstruire le graphe des transitions.

## Comment ca s'applique a OdooAI

1. **Enrichir le Knowledge Graph avec les state machines** : aujourd'hui le KG contient models, fields, relations. Ajouter un noeud "StateMachine" par model qui a un champ `state`, avec les transitions comme edges, donne au Business Analyst la capacite d'expliquer les workflows metier.

2. **Le Business Analyst peut repondre "que se passe-t-il quand je confirme une commande ?"** : avec le graphe de transitions, l'agent peut tracer le chemin draft > confirmed > done et expliquer chaque etape, les validations, les effets de bord (stock moves, accounting entries).

3. **Detection d'anomalies dans les workflows custom** : si un client a des modules custom, parser leurs state machines permet de detecter les etats orphelins ou les transitions manquantes.

## Ce que je recommande

1. **Sprint 7** : Creer un parser AST `workflow_extractor.py` dans `odooai/services/` qui extrait les state machines depuis le code source Odoo. Input : repertoire module. Output : JSON avec states, transitions, conditions.

2. **Sprint 8** : Integrer les state machines dans le Knowledge Graph existant. Nouveau type de noeud `WorkflowState`, nouvelles relations `TRANSITIONS_TO` avec attributs (method, conditions, button_label).

3. **Sprint 9** : Ajouter des vues XML parsing pour croiser les boutons declares avec les transitions code et generer des diagrammes de workflow pour le Business Analyst.

## Sources

1. Odoo Source Code — `odoo/addons/sale/models/sale_order.py` (Odoo 17) : reference state machine sale.order
2. Odoo Documentation — "Actions and Automations" (2025) : https://www.odoo.com/documentation/17.0/developer/reference/backend/actions.html
3. Python AST Module Documentation : https://docs.python.org/3/library/ast.html
