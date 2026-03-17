"""
Module: knowledge/code_analyst/analyzer.py
Role: Orchestrate the parsing of a complete Odoo module into a Knowledge Graph.
      Best-effort: logs errors, skips broken files, continues.
Dependencies: manifest_parser, python_parser, xml_parser
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import structlog

from odooai.knowledge.code_analyst.manifest_parser import parse_manifest
from odooai.knowledge.code_analyst.method_analyzer import (
    analyze_file_methods,
    resolve_selection_constants,
)
from odooai.knowledge.code_analyst.python_parser import parse_python_file
from odooai.knowledge.code_analyst.xml_parser import parse_access_csv, parse_xml_file
from odooai.knowledge.schemas.actions import ActionMethod, MethodActionFlow, MethodEffect
from odooai.knowledge.schemas.constraints import OnchangeMethod, PythonConstraint, SqlConstraint
from odooai.knowledge.schemas.index import KnowledgeIndex, ModuleEntry, ModuleKnowledgeGraph
from odooai.knowledge.schemas.menus import MenuItem
from odooai.knowledge.schemas.models import ModelDefinition
from odooai.knowledge.schemas.security import AccessRight, RecordRule, SecurityGroup
from odooai.knowledge.schemas.views import ViewDefinition

logger = structlog.get_logger(__name__)


def analyze_module(module_path: Path) -> ModuleKnowledgeGraph | None:
    """
    Analyze a single Odoo module and produce its Knowledge Graph.

    Best-effort: if a file fails to parse, it's skipped and logged.

    Args:
        module_path: Path to the Odoo module root directory.

    Returns:
        ModuleKnowledgeGraph or None if manifest parsing fails.
    """
    manifest = parse_manifest(module_path)
    if not manifest:
        logger.error("Cannot analyze module without manifest", path=str(module_path))
        return None

    module_name = manifest.technical_name

    # Parse Python files
    models: list[ModelDefinition] = []
    actions: list[ActionMethod] = []
    py_constraints: list[PythonConstraint] = []
    onchanges: list[OnchangeMethod] = []
    sql_constraints: list[SqlConstraint] = []

    for py_file in _find_python_files(module_path):
        try:
            m, a, c, o, s = parse_python_file(py_file, module_name)
            models.extend(m)
            actions.extend(a)
            py_constraints.extend(c)
            onchanges.extend(o)
            sql_constraints.extend(s)
        except Exception as exc:
            logger.warning(
                "Failed to parse Python file (skipping)",
                path=str(py_file),
                error=str(exc),
            )

    # Phase 2: Resolve selection constants + analyze method bodies
    all_constants: dict[str, list[list[str]]] = {}
    for py_file in _find_python_files(module_path):
        try:
            constants = resolve_selection_constants(py_file)
            all_constants.update(constants)
        except Exception:
            pass

    # Resolve selection fields that reference constants
    for model in models:
        for _fname, fdef in model.fields.items():
            if (
                fdef.type == "selection"
                and isinstance(fdef.selection, str)
                and fdef.selection in all_constants
            ):
                # Replace constant reference with actual values
                resolved = all_constants[fdef.selection]
                # Create new field with resolved selection
                model.fields[_fname] = fdef.model_copy(
                    update={"selection": resolved},
                )

    # Analyze method bodies for action flows
    action_flows: list[MethodActionFlow] = []
    for py_file in _find_python_files(module_path):
        try:
            primary_model = module_name
            for mdl in models:
                if not mdl.is_extension:
                    primary_model = mdl.name
                    break
            method_results = analyze_file_methods(py_file, primary_model)
            for mr in method_results:
                action_flows.append(
                    MethodActionFlow(
                        method_name=mr.name,
                        model=mr.model,
                        effects=[
                            MethodEffect(
                                type=e.type,
                                target_model=e.target_model,
                                field=e.field,
                                value=e.value,
                                via_method=e.via_method,
                            )
                            for e in mr.effects
                        ],
                        calls=mr.calls,
                        env_refs=mr.env_refs,
                    )
                )
        except Exception:
            pass

    # Parse XML files
    views: list[ViewDefinition] = []
    rules: list[RecordRule] = []
    groups: list[SecurityGroup] = []
    menus: list[MenuItem] = []

    for xml_file in _find_xml_files(module_path):
        try:
            v, r, g, mn = parse_xml_file(xml_file)
            views.extend(v)
            rules.extend(r)
            groups.extend(g)
            menus.extend(mn)
        except Exception as exc:
            logger.warning(
                "Failed to parse XML file (skipping)",
                path=str(xml_file),
                error=str(exc),
            )

    # Parse access rights CSV
    access_rights: list[AccessRight] = []
    for csv_file in module_path.rglob("ir.model.access.csv"):
        try:
            access_rights.extend(parse_access_csv(csv_file))
        except Exception as exc:
            logger.warning("Failed to parse access CSV (skipping)", error=str(exc))

    logger.info(
        "Module analyzed",
        module=module_name,
        models=len(models),
        fields=sum(len(m.fields) for m in models),
        views=len(views),
        actions=len(actions),
    )

    return ModuleKnowledgeGraph(
        manifest=manifest,
        models=models,
        sql_constraints=sql_constraints,
        python_constraints=py_constraints,
        onchange_methods=onchanges,
        action_methods=actions,
        action_flows=action_flows,
        access_rights=access_rights,
        record_rules=rules,
        security_groups=groups,
        views=views,
        menus=menus,
    )


def analyze_version(version_path: Path, odoo_version: str) -> KnowledgeIndex:
    """
    Analyze all modules in an Odoo version directory.

    Best-effort: modules that fail are logged with error and skipped.

    Args:
        version_path: Path containing Odoo module directories.
        odoo_version: Version string (e.g. '17.0').

    Returns:
        KnowledgeIndex with entries for all analyzed modules.
    """
    entries: list[ModuleEntry] = []
    total_models = 0
    total_fields = 0

    for module_dir in sorted(version_path.iterdir()):
        if not module_dir.is_dir():
            continue
        if not (module_dir / "__manifest__.py").exists():
            continue

        try:
            kg = analyze_module(module_dir)
            if kg:
                model_count = len(kg.models)
                field_count = sum(len(m.fields) for m in kg.models)
                total_models += model_count
                total_fields += field_count
                entries.append(
                    ModuleEntry(
                        technical_name=kg.manifest.technical_name,
                        path=str(module_dir),
                        analyzed_at=datetime.now(UTC).isoformat(),
                        model_count=model_count,
                        field_count=field_count,
                        success=True,
                    )
                )
            else:
                entries.append(
                    ModuleEntry(
                        technical_name=module_dir.name,
                        path=str(module_dir),
                        analyzed_at=datetime.now(UTC).isoformat(),
                        success=False,
                        error="Manifest parsing failed",
                    )
                )
        except Exception as exc:
            logger.error("Module analysis failed", module=module_dir.name, error=str(exc))
            entries.append(
                ModuleEntry(
                    technical_name=module_dir.name,
                    path=str(module_dir),
                    analyzed_at=datetime.now(UTC).isoformat(),
                    success=False,
                    error=str(exc),
                )
            )

    return KnowledgeIndex(
        odoo_version=odoo_version,
        generated_at=datetime.now(UTC).isoformat(),
        modules=entries,
        total_models=total_models,
        total_fields=total_fields,
    )


def _find_python_files(module_path: Path) -> list[Path]:
    """Find all Python files in a module (models/, wizards/, etc.)."""
    files: list[Path] = []
    for subdir in ("models", "wizards", "wizard", "controllers"):
        d = module_path / subdir
        if d.is_dir():
            files.extend(sorted(d.rglob("*.py")))
    # Also check root-level .py files (some modules define models there)
    for f in sorted(module_path.glob("*.py")):
        if f.name not in ("__init__.py", "__manifest__.py", "__openerp__.py"):
            files.append(f)
    return files


def _find_xml_files(module_path: Path) -> list[Path]:
    """Find all XML data files in a module."""
    files: list[Path] = []
    for subdir in ("views", "security", "data", "report", "wizard", "wizards"):
        d = module_path / subdir
        if d.is_dir():
            files.extend(sorted(d.rglob("*.xml")))
    return files
