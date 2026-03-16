"""
Module: _cli_display.py
Role: Display helpers for the CLI (print formatted output).
Dependencies: knowledge schemas
"""

from __future__ import annotations


def print_module_summary(kg: object) -> None:
    """Print a human-readable summary of a Knowledge Graph."""
    from odooai.knowledge.schemas.index import ModuleKnowledgeGraph

    if not isinstance(kg, ModuleKnowledgeGraph):
        return

    print(f"Module:      {kg.manifest.name} ({kg.manifest.technical_name})")
    print(f"Version:     {kg.manifest.version}")
    print(f"Category:    {kg.manifest.category}")
    print(f"Depends:     {', '.join(kg.manifest.depends)}")
    print(f"Models:      {len(kg.models)}")
    total_fields = sum(len(m.fields) for m in kg.models)
    print(f"Fields:      {total_fields}")
    print(f"Actions:     {len(kg.action_methods)}")
    print(f"Constraints: {len(kg.sql_constraints)} SQL, {len(kg.python_constraints)} Python")
    print(f"Views:       {len(kg.views)}")
    print(f"ACLs:        {len(kg.access_rights)}")
    print(f"Menus:       {len(kg.menus)}")

    if kg.models:
        print("\nModels:")
        for m in kg.models:
            ext = " [EXT]" if m.is_extension else ""
            trans = " [WIZARD]" if m.is_transient else ""
            print(f"  {m.name}{ext}{trans} — {len(m.fields)} fields")


def print_model_detail(model: object) -> None:
    """Print detailed model information."""
    from odooai.knowledge.schemas.models import ModelDefinition

    if not isinstance(model, ModelDefinition):
        return

    print(f"Model:       {model.name}")
    print(f"Description: {model.description}")
    if model.inherit:
        print(f"Inherits:    {', '.join(model.inherit)}")
    if model.inherits:
        print(f"Delegates:   {model.inherits}")
    if model.is_extension:
        print("Type:        Extension (no _name)")
    if model.is_transient:
        print("Type:        TransientModel (wizard)")
    print(f"Fields ({len(model.fields)}):")
    for fname, f in sorted(model.fields.items()):
        extras: list[str] = []
        if f.required:
            extras.append("required")
        if f.readonly:
            extras.append("readonly")
        if f.compute:
            extras.append(f"compute={f.compute}")
        if f.related:
            extras.append(f"related={f.related}")
        if f.relation:
            extras.append(f"-> {f.relation}")
        if not f.store:
            extras.append("not stored")
        info = f" ({', '.join(extras)})" if extras else ""
        print(f"  {fname}: {f.type}{info}")


def print_field_detail(field: object) -> None:
    """Print detailed field information."""
    from odooai.knowledge.schemas.models import FieldDefinition

    if not isinstance(field, FieldDefinition):
        return

    print(f"Field:    {field.name}")
    print(f"Type:     {field.type}")
    if field.string:
        print(f"Label:    {field.string}")
    print(f"Required: {field.required}")
    print(f"Readonly: {field.readonly}")
    print(f"Stored:   {field.store}")
    if field.compute:
        print(f"Compute:  {field.compute}")
    if field.depends:
        print(f"Depends:  {', '.join(field.depends)}")
    if field.related:
        print(f"Related:  {field.related}")
    if field.relation:
        print(f"Relation: {field.relation}")
    if field.selection:
        if isinstance(field.selection, str):
            print(f"Selection: {field.selection} (method)")
        else:
            print("Selection:")
            for item in field.selection:
                print(f"  {item[0]}: {item[1]}" if len(item) >= 2 else f"  {item}")
    if field.default:
        print(f"Default:  {field.default}")
    if field.help:
        print(f"Help:     {field.help}")
