"""
Module: rnd/seo-content-generator/generate.py
Role: Generate SEO blog articles from OdooAI Knowledge Graphs.
Dependencies: odooai.knowledge.storage, pathlib, argparse, json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Add project root to path so we can import odooai
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from odooai.knowledge.storage import load_module_kg

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
ODOO_VERSION = "17.0"


@dataclass(frozen=True)
class FieldInfo:
    """Extracted field information for article generation."""

    name: str
    field_type: str
    string: str
    required: bool
    compute: str | None
    help_text: str
    relation: str | None


@dataclass(frozen=True)
class ModelInfo:
    """Extracted model information for article generation."""

    name: str
    description: str
    is_extension: bool
    fields: list[FieldInfo]
    order: str


@dataclass(frozen=True)
class ArticleSpec:
    """Specification for a single SEO article."""

    slug: str
    title: str
    short_answer: str
    details_generator: str  # key to select which detail section to generate
    activation_steps: list[str]
    models_used: list[str]


def extract_models(kg_data: dict[str, Any]) -> dict[str, ModelInfo]:
    """Extract model information from a Knowledge Graph dict."""
    models: dict[str, ModelInfo] = {}
    for model_data in kg_data.get("models", []):
        fields = []
        for fname, fdata in model_data.get("fields", {}).items():
            fields.append(
                FieldInfo(
                    name=fdata.get("name", fname),
                    field_type=fdata.get("type", ""),
                    string=fdata.get("string", ""),
                    required=fdata.get("required", False),
                    compute=fdata.get("compute"),
                    help_text=fdata.get("help", ""),
                    relation=fdata.get("relation"),
                )
            )
        models[model_data["name"]] = ModelInfo(
            name=model_data["name"],
            description=model_data.get("description", ""),
            is_extension=model_data.get("is_extension", False),
            fields=fields,
            order=model_data.get("order", ""),
        )
    return models


def get_field_by_name(
    model: ModelInfo, field_name: str
) -> FieldInfo | None:
    """Find a field by its technical name."""
    for f in model.fields:
        if f.name == field_name:
            return f
    return None


def format_field_ref(field: FieldInfo) -> str:
    """Format a field reference for article text."""
    label = field.string if field.string else field.name
    computed = " (calcule automatiquement)" if field.compute else ""
    required = " **obligatoire**" if field.required else ""
    return f"- `{field.name}` ({field.field_type}) — {label}{required}{computed}"


def generate_article_1(models: dict[str, ModelInfo]) -> str:
    """Article: Comment automatiser mes devis dans Odoo ?"""
    so = models.get("sale.order")
    if not so:
        return ""

    validity = get_field_by_name(so, "validity_date")
    require_sig = get_field_by_name(so, "require_signature")
    require_pay = get_field_by_name(so, "require_payment")
    prepayment = get_field_by_name(so, "prepayment_percent")
    state = get_field_by_name(so, "state")
    note = get_field_by_name(so, "note")

    key_fields = [
        f for f in [validity, require_sig, require_pay, prepayment, state, note]
        if f is not None
    ]

    return f"""# Comment automatiser mes devis dans Odoo ?

## Reponse courte
Odoo permet d'automatiser la creation et le suivi des devis grace au modele `sale.order`. Les devis peuvent etre envoyes automatiquement par email, signer en ligne et convertis en commande de vente en un clic. Le champ `state` gere le cycle de vie complet (brouillon, envoye, confirme, annule).

## Details
Le modele **sale.order** (Odoo 17) gere l'ensemble du processus devis-commande. Voici les champs cles pour l'automatisation :

{chr(10).join(format_field_ref(f) for f in key_fields)}

### Signature et paiement en ligne
Le champ `require_signature` ({require_sig.field_type if require_sig else 'boolean'}) permet d'exiger une signature electronique du client avant confirmation. Il est calcule via `_compute_require_signature` et peut etre active par defaut dans les parametres.

Le champ `require_payment` ({require_pay.field_type if require_pay else 'boolean'}) exige un prepaiement en ligne. Le pourcentage est controle par `prepayment_percent` (calcule via `_compute_prepayment_percent`).

### Date d'expiration automatique
Le champ `validity_date` ({validity.field_type if validity else 'date'}) est calcule automatiquement via `_compute_validity_date` a partir des parametres de la societe. Le champ `is_expired` (boolean, compute `_compute_is_expired`) indique si le devis a expire.

### Conditions et notes
Le champ `note` (html) contient les conditions generales, calculees automatiquement via `_compute_note` depuis les parametres de la societe (`terms_type` est un related sur `company_id.terms_type`).

## Comment activer
1. Aller dans **Ventes > Configuration > Parametres**
2. Activer **Signature en ligne** pour exiger la signature client
3. Activer **Paiement en ligne** et definir le pourcentage de prepaiement
4. Definir la **duree de validite par defaut** des devis
5. Configurer les **conditions generales** dans les parametres de la societe
6. Creer un devis via **Ventes > Commandes > Devis > Nouveau**

## Modeles Odoo concernes
| Modele | Description | Role |
|--------|-------------|------|
| `sale.order` | Sales Order | Modele principal des devis et commandes |
| `res.partner` | Contact | Client du devis (`partner_id`, required) |
| `product.pricelist` | Pricelist | Liste de prix applicable (`pricelist_id`, compute) |
| `res.company` | Societe | Source des parametres par defaut (validite, conditions) |
"""


def generate_article_2(models: dict[str, ModelInfo]) -> str:
    """Article: Comment suivre mes commandes de vente ?"""
    so = models.get("sale.order")
    if not so:
        return ""

    state = get_field_by_name(so, "state")
    invoice_status = get_field_by_name(so, "invoice_status")
    invoice_count = get_field_by_name(so, "invoice_count")
    amount_to_invoice = get_field_by_name(so, "amount_to_invoice")
    amount_invoiced = get_field_by_name(so, "amount_invoiced")
    date_order = get_field_by_name(so, "date_order")

    sol = models.get("sale.order.line")
    qty_delivered = get_field_by_name(sol, "qty_delivered") if sol else None
    qty_invoiced = get_field_by_name(sol, "qty_invoiced") if sol else None
    qty_to_invoice = get_field_by_name(sol, "qty_to_invoice") if sol else None

    return f"""# Comment suivre mes commandes de vente ?

## Reponse courte
Odoo offre un suivi complet des commandes de vente via le modele `sale.order`. Le champ `state` indique l'etat (brouillon, confirme, annule), tandis que `invoice_status` suit l'avancement de la facturation. Les quantites livrees et facturees sont tracees ligne par ligne dans `sale.order.line`.

## Details
### Suivi de l'etat de la commande
Le champ `state` (selection, default `draft`) controle le cycle de vie de la commande. Il est en lecture seule (`readonly=True`) et change via les actions du workflow :
- **draft** : Brouillon / Devis
- **sent** : Devis envoye au client
- **sale** : Commande confirmee
- **cancel** : Annulee

Le tri par defaut est `date_order desc, id desc`, ce qui affiche les commandes les plus recentes en premier.

### Suivi de la facturation
{format_field_ref(invoice_status) if invoice_status else ''}
{format_field_ref(invoice_count) if invoice_count else ''}
{format_field_ref(amount_to_invoice) if amount_to_invoice else ''}
{format_field_ref(amount_invoiced) if amount_invoiced else ''}

Le champ `invoice_status` est calcule via `_compute_invoice_status` et peut prendre les valeurs : a facturer, facture, rien a facturer.

### Suivi par ligne de commande (`sale.order.line`)
Chaque ligne suit individuellement :
{format_field_ref(qty_delivered) if qty_delivered else ''}
{format_field_ref(qty_invoiced) if qty_invoiced else ''}
{format_field_ref(qty_to_invoice) if qty_to_invoice else ''}

La methode de mise a jour de la quantite livree est controlee par `qty_delivered_method` (selection : `manual` ou `analytic`).

## Comment activer
1. Aller dans **Ventes > Commandes > Commandes** pour voir toutes les commandes confirmees
2. Utiliser les **filtres** par etat (`state`) ou statut de facturation (`invoice_status`)
3. Cliquer sur une commande pour voir le detail des lignes
4. L'onglet **Factures** montre les factures liees (`invoice_ids`, `invoice_count`)
5. Le bouton **Creer une facture** apparait quand `invoice_status = "to invoice"`

## Modeles Odoo concernes
| Modele | Description | Role |
|--------|-------------|------|
| `sale.order` | Sales Order | Commande principale avec etat et montants |
| `sale.order.line` | Sales Order Line | Lignes de detail avec quantites livrees/facturees |
| `account.move` | Facture | Factures liees via `invoice_ids` (many2many, compute `_get_invoiced`) |
| `crm.team` | Sales Team | Equipe commerciale (`team_id`, compute `_compute_team_id`) |
"""


def generate_article_3(models: dict[str, ModelInfo]) -> str:
    """Article: Quels champs sont importants dans une commande Odoo ?"""
    so = models.get("sale.order")
    sol = models.get("sale.order.line")
    if not so or not sol:
        return ""

    # Categorize sale.order fields
    required_fields = [f for f in so.fields if f.required]
    computed_fields = [f for f in so.fields if f.compute]
    monetary_fields = [f for f in so.fields if f.field_type == "monetary"]
    relation_fields = [f for f in so.fields if f.relation]

    # Key sale.order.line fields
    sol_required = [f for f in sol.fields if f.required]
    sol_monetary = [f for f in sol.fields if f.field_type == "monetary"]

    return f"""# Quels champs sont importants dans une commande Odoo ?

## Reponse courte
Une commande Odoo (`sale.order`) contient {len(so.fields)} champs dans le module sale. Les champs obligatoires sont `name`, `partner_id`, `date_order`, `partner_invoice_id` et `partner_shipping_id`. Les montants (`amount_untaxed`, `amount_tax`, `amount_total`) sont calcules automatiquement. Chaque ligne (`sale.order.line`) a {len(sol.fields)} champs dont `product_id`, `product_uom_qty`, `price_unit`.

## Details
### Champs obligatoires de `sale.order`
{chr(10).join(format_field_ref(f) for f in required_fields)}

### Champs monetaires (calcules automatiquement)
{chr(10).join(format_field_ref(f) for f in monetary_fields)}

### Champs relationnels cles
{chr(10).join(format_field_ref(f) for f in relation_fields if f.string)}

### Champs obligatoires de `sale.order.line`
{chr(10).join(format_field_ref(f) for f in sol_required)}

### Champs monetaires des lignes
{chr(10).join(format_field_ref(f) for f in sol_monetary)}

### Statistiques
- **sale.order** : {len(so.fields)} champs, dont {len(required_fields)} obligatoires, {len(computed_fields)} calcules, {len(monetary_fields)} monetaires
- **sale.order.line** : {len(sol.fields)} champs, dont {len(sol_required)} obligatoires, {len(sol_monetary)} monetaires

## Comment activer
1. Installer le module **Sales** (`sale`) via **Applications**
2. Aller dans **Ventes > Commandes > Devis > Nouveau**
3. Remplir le client (`partner_id`) — les adresses de facturation et livraison se calculent automatiquement
4. Ajouter des lignes de commande avec produit, quantite et prix
5. Les montants totaux se mettent a jour automatiquement

## Modeles Odoo concernes
| Modele | Description | Nb champs | Obligatoires |
|--------|-------------|-----------|--------------|
| `sale.order` | Sales Order | {len(so.fields)} | {len(required_fields)} |
| `sale.order.line` | Sales Order Line | {len(sol.fields)} | {len(sol_required)} |
| `res.partner` | Contact | - | relation via `partner_id` |
| `product.product` | Produit | - | relation via `product_id` |
| `account.tax` | Taxes | - | relation via `tax_id` |
"""


def generate_article_4(models: dict[str, ModelInfo]) -> str:
    """Article: Comment Odoo calcule le montant total d'une commande ?"""
    so = models.get("sale.order")
    sol = models.get("sale.order.line")
    if not so or not sol:
        return ""

    amount_untaxed = get_field_by_name(so, "amount_untaxed")
    amount_tax = get_field_by_name(so, "amount_tax")
    amount_total = get_field_by_name(so, "amount_total")
    amount_undiscounted = get_field_by_name(so, "amount_undiscounted")
    currency_rate = get_field_by_name(so, "currency_rate")
    tax_totals = get_field_by_name(so, "tax_totals")

    price_unit = get_field_by_name(sol, "price_unit")
    qty = get_field_by_name(sol, "product_uom_qty")
    discount = get_field_by_name(sol, "discount")
    price_subtotal = get_field_by_name(sol, "price_subtotal")
    price_tax = get_field_by_name(sol, "price_tax")
    price_total = get_field_by_name(sol, "price_total")
    price_reduce_taxexcl = get_field_by_name(sol, "price_reduce_taxexcl")
    price_reduce_taxinc = get_field_by_name(sol, "price_reduce_taxinc")

    return f"""# Comment Odoo calcule le montant total d'une commande ?

## Reponse courte
Le montant total d'une commande Odoo est calcule automatiquement par la methode `_compute_amounts` du modele `sale.order`. Il additionne les sous-totaux de chaque ligne (`sale.order.line`), ou chaque ligne calcule `price_subtotal` et `price_tax` via sa propre methode `_compute_amount`. La formule de base est : `price_unit * product_uom_qty * (1 - discount/100)` + taxes.

## Details
### Niveau ligne (`sale.order.line`)
Chaque ligne de commande calcule ses montants via `_compute_amount` :

{format_field_ref(price_unit) if price_unit else ''}
{format_field_ref(qty) if qty else ''}
{format_field_ref(discount) if discount else ''}
{format_field_ref(price_subtotal) if price_subtotal else ''}
{format_field_ref(price_tax) if price_tax else ''}
{format_field_ref(price_total) if price_total else ''}

**Formule** :
```
subtotal = price_unit * product_uom_qty * (1 - discount / 100)
total = subtotal + taxes calculees via tax_id
```

Les prix reduits sont aussi disponibles :
{format_field_ref(price_reduce_taxexcl) if price_reduce_taxexcl else ''}
{format_field_ref(price_reduce_taxinc) if price_reduce_taxinc else ''}

### Niveau commande (`sale.order`)
Les montants de la commande sont agreges via `_compute_amounts` :

{format_field_ref(amount_untaxed) if amount_untaxed else ''}
{format_field_ref(amount_tax) if amount_tax else ''}
{format_field_ref(amount_total) if amount_total else ''}
{format_field_ref(amount_undiscounted) if amount_undiscounted else ''}

**Formule** :
```
amount_untaxed = SUM(order_line.price_subtotal)
amount_tax     = SUM(order_line.price_tax)
amount_total   = amount_untaxed + amount_tax
```

### Gestion multi-devises
Le champ `currency_id` (many2one vers `res.currency`) definit la devise de la commande. Le taux de change est stocke dans `currency_rate` (float, compute `_compute_currency_rate`). Les montants totaux detailles incluant les regroupements par taux de taxe sont dans `tax_totals` (binary, compute `_compute_tax_totals`).

### Methode d'arrondi
Le champ `tax_calculation_rounding_method` (selection, related `company_id.tax_calculation_rounding_method`) controle si les taxes sont arrondies ligne par ligne ou globalement.

## Comment activer
1. Les calculs sont **automatiques** — aucune configuration requise
2. Pour changer la devise : modifier `pricelist_id` ou `currency_id` sur la commande
3. Pour appliquer des remises : remplir le champ `discount` (%) sur chaque ligne
4. Les taxes sont definies dans **Comptabilite > Configuration > Taxes**
5. La position fiscale (`fiscal_position_id`) peut adapter les taxes automatiquement selon le client

## Modeles Odoo concernes
| Modele | Methode compute | Champs calcules |
|--------|-----------------|-----------------|
| `sale.order` | `_compute_amounts` | `amount_untaxed`, `amount_tax`, `amount_total` |
| `sale.order` | `_compute_amount_undiscounted` | `amount_undiscounted` |
| `sale.order` | `_compute_currency_rate` | `currency_rate` |
| `sale.order.line` | `_compute_amount` | `price_subtotal`, `price_tax`, `price_total` |
| `sale.order.line` | `_compute_price_reduce_taxexcl` | `price_reduce_taxexcl` |
| `sale.order.line` | `_compute_price_reduce_taxinc` | `price_reduce_taxinc` |
"""


def generate_article_5(models: dict[str, ModelInfo]) -> str:
    """Article: Comment gerer les conditions de paiement ?"""
    so = models.get("sale.order")
    if not so:
        return ""

    payment_term = get_field_by_name(so, "payment_term_id")
    fiscal_pos = get_field_by_name(so, "fiscal_position_id")
    reference = get_field_by_name(so, "reference")
    transaction_ids = get_field_by_name(so, "transaction_ids")
    amount_paid = get_field_by_name(so, "amount_paid")

    # payment.provider extension
    pp = models.get("payment.provider")
    so_ref_type = None
    if pp:
        so_ref_type = get_field_by_name(pp, "so_reference_type")

    return f"""# Comment gerer les conditions de paiement ?

## Reponse courte
Les conditions de paiement dans Odoo sont gerees via le champ `payment_term_id` du modele `sale.order`, qui reference le modele `account.payment.term`. Ce champ est calcule automatiquement a partir du client (`_compute_payment_term_id`) mais peut etre modifie manuellement. Les transactions de paiement en ligne sont tracees via `transaction_ids`.

## Details
### Conditions de paiement sur la commande
{format_field_ref(payment_term) if payment_term else ''}

Le champ `payment_term_id` est un **many2one** vers `account.payment.term`. Il est calcule automatiquement via `_compute_payment_term_id` qui recupere les conditions de paiement par defaut du client (`partner_id`). Ce champ controle :
- Les echeances de facturation
- Les dates d'echeance sur les factures generees
- Le calcul des paiements partiels

### Position fiscale
{format_field_ref(fiscal_pos) if fiscal_pos else ''}

La position fiscale adapte automatiquement les taxes et comptes comptables selon le client ou le pays. Son help text dans le code source Odoo : *"{fiscal_pos.help_text}"*

### Paiement en ligne
{format_field_ref(transaction_ids) if transaction_ids else ''}
{format_field_ref(amount_paid) if amount_paid else ''}
{format_field_ref(reference) if reference else ''}

Les transactions de paiement (`payment.transaction`) sont liees a la commande via `transaction_ids` (many2many, readonly). Le montant deja paye est calcule par `_compute_amount_paid`.

### Configuration du fournisseur de paiement
Le module sale etend le modele `payment.provider` avec le champ :
{format_field_ref(so_ref_type) if so_ref_type else ''}

Ce champ definit la communication sur le paiement : soit basee sur la reference du document (`so_name`), soit sur l'ID client (`partner`). Valeur par defaut : `so_name`.

### Prepaiement
Le champ `require_payment` (boolean) exige un paiement en ligne avant confirmation. Le pourcentage minimum est controle par `prepayment_percent` (float, compute `_compute_prepayment_percent`).

## Comment activer
1. Aller dans **Comptabilite > Configuration > Conditions de paiement**
2. Creer ou modifier les conditions (ex: 30 jours, 50% a la commande + 50% a 30 jours)
3. Assigner les conditions par defaut sur la fiche client (**Contacts > onglet Ventes**)
4. Sur chaque commande, le champ **Conditions de paiement** est rempli automatiquement
5. Pour le paiement en ligne : **Ventes > Configuration > Parametres > Paiement en ligne**
6. Configurer les fournisseurs de paiement dans **Comptabilite > Configuration > Fournisseurs de paiement**

## Modeles Odoo concernes
| Modele | Description | Role |
|--------|-------------|------|
| `sale.order` | Sales Order | Porte `payment_term_id` et `transaction_ids` |
| `account.payment.term` | Conditions de paiement | Definit les echeances et modalites |
| `account.fiscal.position` | Position fiscale | Adapte taxes selon le client (`fiscal_position_id`) |
| `payment.transaction` | Transaction de paiement | Paiements en ligne lies a la commande |
| `payment.provider` | Fournisseur de paiement | Etendu avec `so_reference_type` pour la communication |
"""


def generate_articles(module_name: str) -> list[tuple[str, str]]:
    """
    Generate all SEO articles for a given module.

    Returns:
        List of (filename, markdown_content) tuples.
    """
    # Load KG using the project's storage module
    kg = load_module_kg(module_name, ODOO_VERSION)
    if kg is None:
        # Fallback: load directly from JSON
        kg_path = PROJECT_ROOT / "knowledge_store" / ODOO_VERSION / module_name / "knowledge.json"
        if not kg_path.exists():
            print(f"ERROR: Knowledge Graph not found for module '{module_name}'")
            print(f"  Looked in: {kg_path}")
            sys.exit(1)
        kg_data = json.loads(kg_path.read_text(encoding="utf-8"))
    else:
        kg_data = json.loads(kg.model_dump_json())

    models = extract_models(kg_data)
    manifest = kg_data.get("manifest", {})

    print(f"Module: {manifest.get('name', module_name)} ({module_name})")
    print(f"Models loaded: {len(models)}")
    print(f"  Non-extension: {sum(1 for m in models.values() if not m.is_extension)}")
    print(f"  Extensions: {sum(1 for m in models.values() if m.is_extension)}")
    print()

    generators = [
        ("01-automatiser-devis-odoo.md", generate_article_1),
        ("02-suivre-commandes-vente.md", generate_article_2),
        ("03-champs-importants-commande.md", generate_article_3),
        ("04-calcul-montant-total.md", generate_article_4),
        ("05-conditions-paiement.md", generate_article_5),
    ]

    articles: list[tuple[str, str]] = []
    for filename, gen_func in generators:
        content = gen_func(models)
        if content:
            articles.append((filename, content.strip() + "\n"))
            print(f"  Generated: {filename}")
        else:
            print(f"  SKIPPED: {filename} (missing required models)")

    return articles


def write_articles(articles: list[tuple[str, str]]) -> None:
    """Write generated articles to the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, content in articles:
        output_path = OUTPUT_DIR / filename
        output_path.write_text(content, encoding="utf-8")
    print(f"\n{len(articles)} articles written to {OUTPUT_DIR}/")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate SEO blog articles from OdooAI Knowledge Graphs"
    )
    parser.add_argument(
        "--module",
        default="sale",
        help="Odoo module name (default: sale)",
    )
    parser.add_argument(
        "--questions",
        type=int,
        default=5,
        help="Number of articles to generate (default: 5)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print articles to stdout instead of writing files",
    )
    args = parser.parse_args()

    articles = generate_articles(args.module)

    # Limit to requested number
    articles = articles[: args.questions]

    if args.dry_run:
        for filename, content in articles:
            print(f"\n{'='*60}")
            print(f"FILE: {filename}")
            print(f"{'='*60}")
            print(content)
    else:
        write_articles(articles)


if __name__ == "__main__":
    main()
