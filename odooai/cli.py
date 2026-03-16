"""
Module: cli.py
Role: Command-line interface for OdooAI.
      Provides commands for analyzing Odoo modules, checking KG quality,
      and running the server.
Dependencies: argparse (stdlib)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from odooai import __version__


def main(argv: list[str] | None = None) -> None:
    """OdooAI CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="odooai",
        description="OdooAI — AI Business Analyst for Odoo",
    )
    parser.add_argument("--version", action="version", version=f"odooai {__version__}")

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # analyze: parse a single module
    p_analyze = sub.add_parser("analyze", help="Analyze an Odoo module")
    p_analyze.add_argument("path", type=Path, help="Path to Odoo module directory")
    p_analyze.add_argument("--version-tag", default="17.0", help="Odoo version (default: 17.0)")
    p_analyze.add_argument("--save", action="store_true", help="Save KG to knowledge_store/")
    p_analyze.add_argument(
        "--json", action="store_true", dest="output_json", help="Output raw JSON"
    )

    # analyze-all: parse all modules in a version directory
    p_all = sub.add_parser("analyze-all", help="Analyze all modules in an Odoo addons directory")
    p_all.add_argument("path", type=Path, help="Path to Odoo addons directory")
    p_all.add_argument("--version-tag", default="17.0", help="Odoo version (default: 17.0)")
    p_all.add_argument("--save", action="store_true", help="Save all KGs to knowledge_store/")

    # check-kg: inspect a field or model in a KG
    p_check = sub.add_parser("check-kg", help="Inspect a model or field in a Knowledge Graph")
    p_check.add_argument("module", help="Module technical name (e.g. sale)")
    p_check.add_argument("model", nargs="?", help="Model name (e.g. sale.order)")
    p_check.add_argument("field", nargs="?", help="Field name (e.g. amount_total)")
    p_check.add_argument("--version-tag", default="17.0", help="Odoo version (default: 17.0)")

    # serve: run the API server
    sub.add_parser("serve", help="Run the OdooAI API server")

    args = parser.parse_args(argv)

    if args.command == "analyze":
        _cmd_analyze(args)
    elif args.command == "analyze-all":
        _cmd_analyze_all(args)
    elif args.command == "check-kg":
        _cmd_check_kg(args)
    elif args.command == "serve":
        _cmd_serve()
    else:
        parser.print_help()


def _cmd_analyze(args: argparse.Namespace) -> None:
    """Analyze a single Odoo module."""
    from odooai.knowledge.code_analyst.analyzer import analyze_module
    from odooai.knowledge.storage import save_module_kg

    module_path = args.path.resolve()
    if not module_path.is_dir():
        print(f"Error: {module_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    kg = analyze_module(module_path)
    if kg is None:
        print(f"Error: could not parse {module_path} (no __manifest__.py?)", file=sys.stderr)
        sys.exit(1)

    if args.output_json:
        print(kg.model_dump_json(indent=2))
        return

    _print_module_summary(kg)

    if args.save:
        path = save_module_kg(kg, args.version_tag)
        print(f"\nSaved to: {path}")


def _cmd_analyze_all(args: argparse.Namespace) -> None:
    """Analyze all modules in a directory."""
    from odooai.knowledge.code_analyst.analyzer import analyze_module, analyze_version
    from odooai.knowledge.storage import save_index, save_module_kg

    version_path = args.path.resolve()
    if not version_path.is_dir():
        print(f"Error: {version_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    index = analyze_version(version_path, args.version_tag)

    print(f"Version:  {index.odoo_version}")
    print(f"Modules:  {len(index.modules)}")
    print(f"Models:   {index.total_models}")
    print(f"Fields:   {index.total_fields}")

    failed = [m for m in index.modules if not m.success]
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for m in failed:
            print(f"  {m.technical_name}: {m.error}")

    top = sorted(
        [m for m in index.modules if m.success],
        key=lambda m: m.model_count,
        reverse=True,
    )[:10]
    print("\nTop 10 modules:")
    for m in top:
        print(f"  {m.technical_name}: {m.model_count} models, {m.field_count} fields")

    if args.save:
        save_index(index)
        # Save each module KG
        count = 0
        for module_dir in sorted(version_path.iterdir()):
            if not module_dir.is_dir():
                continue
            if not (module_dir / "__manifest__.py").exists():
                continue
            kg = analyze_module(module_dir)
            if kg:
                save_module_kg(kg, args.version_tag)
                count += 1
        print(f"\nSaved {count} Knowledge Graphs to knowledge_store/{args.version_tag}/")


def _cmd_check_kg(args: argparse.Namespace) -> None:
    """Inspect a model or field in a stored Knowledge Graph."""
    from odooai.knowledge.storage import load_module_kg

    kg = load_module_kg(args.module, args.version_tag)
    if kg is None:
        print(
            f"Error: no KG found for {args.module} v{args.version_tag}. "
            f"Run 'odooai analyze --save' first.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.model:
        _print_module_summary(kg)
        return

    model = next((m for m in kg.models if m.name == args.model), None)
    if model is None:
        print(f"Model '{args.model}' not found in {args.module}.")
        print(f"Available: {[m.name for m in kg.models]}")
        sys.exit(1)

    if not args.field:
        _print_model_detail(model)
        return

    field = model.fields.get(args.field)
    if field is None:
        print(f"Field '{args.field}' not found in {args.model}.")
        print(f"Available: {sorted(model.fields.keys())}")
        sys.exit(1)

    _print_field_detail(field)


def _cmd_serve() -> None:
    """Run the API server."""
    import uvicorn

    uvicorn.run("odooai.main:app", host="0.0.0.0", port=8000, reload=True)


def _print_module_summary(kg: object) -> None:
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


def _print_model_detail(model: object) -> None:
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


def _print_field_detail(field: object) -> None:
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
