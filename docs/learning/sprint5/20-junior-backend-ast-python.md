# Learning — Junior Backend (20) — Python AST Module for Code Analysis

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **Le module ast transforme du code Python en arbre syntaxique** : `ast.parse(source_code)` retourne un arbre de noeuds typees. Chaque noeud represente un element du code : `ast.ClassDef` pour les classes, `ast.FunctionDef` pour les fonctions, `ast.Assign` pour les assignations. On peut traverser l'arbre sans executer le code, ce qui est securise pour analyser du code tiers.

2. **ast.NodeVisitor permet la traversee selective** : En heritant de `ast.NodeVisitor` et en implementant `visit_ClassDef()`, `visit_FunctionDef()`, etc., on parcourt uniquement les noeuds qui nous interessent. Le dispatch est automatique. Pour modifier l'arbre, on utilise `ast.NodeTransformer` qui retourne des noeuds modifies.

3. **Les decorateurs et attributs sont des noeuds accessibles** : `node.decorator_list` donne les decorateurs d'une classe/fonction. `node.body` contient les statements du corps. Pour un `ast.Assign`, `node.targets` donne les noms et `node.value` donne la valeur assignee. Cela permet d'extraire les champs Odoo definis comme `name = fields.Char(string="Name")`.

4. **ast.literal_eval est le seul eval securise** : Pour extraire des valeurs de keyword arguments (comme `string="Name"` ou `required=True`), `ast.literal_eval()` evalue uniquement les litteraux Python (strings, numbers, bools, dicts, lists). Aucun risque d'execution de code arbitraire contrairement a `eval()`.

5. **Le module ast preserve les numeros de lignes** : Chaque noeud a `node.lineno` et `node.col_offset`. Cela permet de generer des references precises vers le code source : "champ `partner_id` defini ligne 42 de sale/models/sale_order.py". Utile pour le debugging et les references dans les reponses de l'assistant.

## Comment ca s'applique a OdooAI

1. **Extraction des champs Odoo depuis le code source** : Le Code Analyst utilise deja l'AST pour parser les modules Odoo. En visitant les `ast.ClassDef` qui heritent de `models.Model`, on extrait tous les `fields.*` assignes dans le corps. Les keyword arguments (`string`, `required`, `compute`, `related`) deviennent les metadata du KG.

2. **Detection des compute methods et depends** : Les decorateurs `@api.depends('field1', 'field2')` sur les methodes compute sont des `ast.Call` dans `decorator_list`. L'AST permet d'extraire les dependances exactes sans regex fragiles. Cela alimente le graphe de dependances entre champs.

3. **Analyse statique de securite** : Avant d'executer du code genere par le LLM (si on ajoute cette feature), l'AST permet de verifier qu'il ne contient pas d'appels dangereux (`os.system`, `eval`, `exec`, `__import__`). Le Security Guardian peut utiliser un `NodeVisitor` qui rejette les patterns interdits.

## Ce que je recommande

1. **Sprint 6** : Creer des tests unitaires pour le parser AST existant dans le Code Analyst. Couvrir les cas limites : champs definis dans des boucles, heritage multiple, classes imbriquees, meta-programmation avec `type()`.

2. **Sprint 7** : Ajouter l'extraction des `_sql_constraints` et des `_check` constraints depuis l'AST. Ces donnees manquent dans les KG actuels mais sont critiques pour comprendre les regles metier des modules Odoo.

3. **Sprint 8** : Implementer un `SecurityASTVisitor` dans `odooai/security/ast_checker.py` qui valide le code Python avant execution. Whitelist de modules et fonctions autorises, rejet de tout le reste.

## Sources

1. Python Documentation, "ast — Abstract Syntax Trees" — docs.python.org/3/library/ast.html (2025)
2. Green Tree Snakes, "The Missing Python AST docs" — greentreesnakes.readthedocs.io (2024)
3. Leandro Lima, "Python AST for Code Analysis" — Real Python (2024)
