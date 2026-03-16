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
from odooai._cli_display import print_field_detail, print_model_detail, print_module_summary


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

    # generate-ba: generate a BA Profile for a domain
    p_ba = sub.add_parser("generate-ba", help="Generate a BA Profile for a functional domain")
    p_ba.add_argument("domain", help="Domain ID (e.g. sales_crm, supply_chain)")
    p_ba.add_argument("--version-tag", default="17.0", help="Odoo version (default: 17.0)")
    p_ba.add_argument("--model", default="claude-sonnet-4-20250514", help="LLM model")
    p_ba.add_argument("--save", action="store_true", help="Save BA Profile to knowledge_store/")

    # chat: interactive chat with OdooAI
    p_chat = sub.add_parser("chat", help="Chat with OdooAI (ask questions about Odoo)")
    p_chat.add_argument("--url", default="", help="Odoo instance URL for live connection")
    p_chat.add_argument("--db", default="", help="Odoo database name")
    p_chat.add_argument("--version-tag", default="17.0", help="Odoo version (default: 17.0)")
    p_chat.add_argument("--model", default="claude-sonnet-4-20250514", help="LLM model")
    p_chat.add_argument(
        "--max-tools", type=int, default=10, help="Max tool calls per question (default: 10)"
    )

    # serve: run the API server
    sub.add_parser("serve", help="Run the OdooAI API server")

    args = parser.parse_args(argv)

    if args.command == "analyze":
        _cmd_analyze(args)
    elif args.command == "analyze-all":
        _cmd_analyze_all(args)
    elif args.command == "generate-ba":
        _cmd_generate_ba(args)
    elif args.command == "chat":
        _cmd_chat(args)
    elif args.command == "check-kg":
        _cmd_check_kg(args)
    elif args.command == "serve":
        _cmd_serve()
    else:
        parser.print_help()


def _cmd_chat(args: argparse.Namespace) -> None:
    """Interactive chat with OdooAI."""
    import asyncio

    from odooai.agents.orchestrator import detect_domain, handle_question
    from odooai.config import get_settings
    from odooai.knowledge.ba_factory import DOMAIN_NAMES

    settings = get_settings()
    api_key = settings.anthropic_api_key
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    # Optional live Odoo connection
    odoo_client = None
    odoo_uid = 0
    odoo_api_key = ""
    live_mode = bool(args.url and args.db)

    if live_mode:
        from odooai._cli_odoo import connect_odoo

        odoo_client, odoo_uid, odoo_api_key = connect_odoo(args.url, args.db)

    print("=" * 60)
    print("  OdooAI — Votre Odoo peut faire plus.")
    mode = "live" if live_mode else "BA Profiles"
    print(f"  Mode : {mode}")
    print("=" * 60)
    print("\nPosez vos questions sur Odoo. Tapez 'quit' pour quitter.\n")

    while True:
        try:
            question = input("Vous > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Au revoir !")
            break

        domain = detect_domain(question)
        tag = DOMAIN_NAMES.get(domain, "general") if domain else "general"
        live_tag = " | live" if live_mode else ""
        print(f"[{tag}{live_tag}]")

        try:
            response = asyncio.run(
                handle_question(
                    question,
                    api_key,
                    args.version_tag,
                    args.model,
                    odoo_client=odoo_client,
                    odoo_uid=odoo_uid,
                    odoo_api_key=odoo_api_key,
                    max_tools=args.max_tools,
                ),
            )
            print(f"\n{response.answer}")
            print(f"\n[Tokens: {response.tokens_used} | Sources: {', '.join(response.sources)}]\n")
        except Exception as exc:
            err_type = type(exc).__name__
            print(f"\nErreur ({err_type}): impossible de generer la reponse.\n", file=sys.stderr)


def _cmd_generate_ba(args: argparse.Namespace) -> None:
    """Generate a BA Profile for a functional domain."""
    import asyncio

    from odooai.config import get_settings
    from odooai.knowledge.ba_factory import DOMAINS, generate_ba_profile
    from odooai.knowledge.storage import load_module_kg

    if args.domain not in DOMAINS:
        print(f"Unknown domain: {args.domain}. Available: {list(DOMAINS.keys())}", file=sys.stderr)
        sys.exit(1)

    settings = get_settings()
    api_key = settings.anthropic_api_key
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    # Load KGs for the domain's modules
    modules = DOMAINS[args.domain]
    kgs = []
    for mod in modules:
        kg = load_module_kg(mod, args.version_tag)
        if kg:
            kgs.append(kg)
            print(f"Loaded KG: {mod} ({len(kg.models)} models)")

    if not kgs:
        print(f"No KGs found for domain {args.domain}. Run 'odooai analyze --save' first.")
        sys.exit(1)

    print(f"\nGenerating BA Profile for '{args.domain}' using {args.model}...")
    profile = asyncio.run(
        generate_ba_profile(args.domain, kgs, api_key, model=args.model),
    )

    print(f"\nBA Profile: {profile.domain_name} | {profile.summary[:100]}")
    print(
        f"Capabilities: {len(profile.capabilities)} | Features: {len(profile.feature_discoveries)}"
    )
    print(f"Gotchas: {len(profile.gotchas)} | Tokens: {profile.token_count}")

    if args.save:
        from pathlib import Path

        store = Path("knowledge_store") / args.version_tag / "_ba_profiles"
        store.mkdir(parents=True, exist_ok=True)
        out = store / f"{args.domain}.json"
        out.write_text(profile.model_dump_json(indent=2), encoding="utf-8")
        print(f"\nSaved to: {out}")


def _cmd_analyze(args: argparse.Namespace) -> None:
    """Analyze a single Odoo module."""
    from odooai.knowledge.code_analyst.analyzer import analyze_module
    from odooai.knowledge.storage import save_module_kg

    path = args.path.resolve()
    if not path.is_dir():
        print(f"Error: {path} is not a directory", file=sys.stderr)
        sys.exit(1)
    kg = analyze_module(path)
    if kg is None:
        print(f"Error: could not parse {path}", file=sys.stderr)
        sys.exit(1)
    if args.output_json:
        print(kg.model_dump_json(indent=2))
        return

    print_module_summary(kg)

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

    failed = [m for m in index.modules if not m.success]
    print(
        f"v{index.odoo_version}: {len(index.modules)} modules, "
        f"{index.total_models} models, {index.total_fields} fields, "
        f"{len(failed)} failed"
    )
    if failed:
        for m in failed:
            print(f"  FAIL: {m.technical_name}: {m.error}")
    top = sorted([m for m in index.modules if m.success], key=lambda m: -m.model_count)[:10]
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
        print_module_summary(kg)
        return

    model = next((m for m in kg.models if m.name == args.model), None)
    if model is None:
        print(f"Model '{args.model}' not found in {args.module}.")
        print(f"Available: {[m.name for m in kg.models]}")
        sys.exit(1)

    if not args.field:
        print_model_detail(model)
        return

    field = model.fields.get(args.field)
    if field is None:
        print(f"Field '{args.field}' not found in {args.model}.")
        print(f"Available: {sorted(model.fields.keys())}")
        sys.exit(1)

    print_field_detail(field)


def _cmd_serve() -> None:
    """Run the API server."""
    import uvicorn

    uvicorn.run("odooai.main:app", host="0.0.0.0", port=8000, reload=True)
