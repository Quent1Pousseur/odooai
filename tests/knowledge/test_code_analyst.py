"""Tests for the Code Analyst: manifest, Python, XML parsers + analyzer."""

from pathlib import Path

from odooai.knowledge.code_analyst.analyzer import analyze_module
from odooai.knowledge.code_analyst.manifest_parser import parse_manifest
from odooai.knowledge.code_analyst.python_parser import parse_python_file
from odooai.knowledge.code_analyst.xml_parser import parse_access_csv, parse_xml_file

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "test_sale"


class TestManifestParser:
    """Test __manifest__.py parsing."""

    def test_parse_valid_manifest(self) -> None:
        manifest = parse_manifest(FIXTURE_PATH)
        assert manifest is not None
        assert manifest.name == "Test Sales"
        assert manifest.technical_name == "test_sale"
        assert manifest.version == "17.0.1.0.0"
        assert manifest.category == "Sales"
        assert "base" in manifest.depends
        assert "product" in manifest.depends
        assert manifest.application is True
        assert manifest.license == "LGPL-3"

    def test_parse_missing_manifest(self, tmp_path: Path) -> None:
        result = parse_manifest(tmp_path)
        assert result is None

    def test_parse_invalid_manifest(self, tmp_path: Path) -> None:
        (tmp_path / "__manifest__.py").write_text("not a dict")
        result = parse_manifest(tmp_path)
        assert result is None


class TestPythonParser:
    """Test Python AST model parsing."""

    def test_parse_sale_order(self) -> None:
        models, actions, constraints, onchanges, sql_c = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        assert len(models) == 2  # SaleOrder + SaleOrderLine

    def test_sale_order_model(self) -> None:
        models, *_ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        so = next(m for m in models if m.name == "sale.order")

        assert so.description == "Sales Order"
        assert so.order == "date_order desc, id desc"
        assert "mail.thread" in so.inherit
        assert so.is_transient is False
        assert so.is_extension is False

    def test_sale_order_fields(self) -> None:
        models, *_ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        so = next(m for m in models if m.name == "sale.order")

        assert "name" in so.fields
        assert so.fields["name"].type == "char"
        assert so.fields["name"].required is True
        assert so.fields["name"].readonly is True

        assert "state" in so.fields
        assert so.fields["state"].type == "selection"
        assert len(so.fields["state"].selection) == 5

        assert "partner_id" in so.fields
        assert so.fields["partner_id"].type == "many2one"
        assert so.fields["partner_id"].relation == "res.partner"

    def test_computed_field_store(self) -> None:
        """Odoo Expert requirement #4: computed fields default to store=False."""
        models, *_ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        so = next(m for m in models if m.name == "sale.order")

        # amount_total has store=True explicitly
        assert so.fields["amount_total"].compute == "_compute_amounts"
        assert so.fields["amount_total"].store is True

    def test_related_field(self) -> None:
        """Odoo Expert requirement #2: related fields captured."""
        models, *_ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        so = next(m for m in models if m.name == "sale.order")

        assert so.fields["currency_id"].related == "company_id.currency_id"
        assert so.fields["currency_id"].store is True

    def test_action_methods(self) -> None:
        _, actions, *_ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        action_names = [a.name for a in actions]
        assert "action_confirm" in action_names
        assert "button_cancel" in action_names

    def test_python_constraints(self) -> None:
        _, _, constraints, *_ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        assert len(constraints) == 1
        assert constraints[0].method_name == "_check_date_order"
        assert "date_order" in constraints[0].fields

    def test_onchange_methods(self) -> None:
        _, _, _, onchanges, _ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        assert len(onchanges) == 1
        assert onchanges[0].method_name == "_onchange_partner_id"
        assert "partner_id" in onchanges[0].fields

    def test_sql_constraints(self) -> None:
        _, _, _, _, sql_c = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        assert len(sql_c) == 1
        assert sql_c[0].name == "name_uniq"
        assert "unique" in sql_c[0].sql

    def test_sale_order_line(self) -> None:
        models, *_ = parse_python_file(
            FIXTURE_PATH / "models" / "sale_order.py",
            "test_sale",
        )
        sol = next(m for m in models if m.name == "sale.order.line")
        assert "product_id" in sol.fields
        assert sol.fields["product_id"].required is True

    def test_parse_syntax_error(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "bad.py"
        bad_file.write_text("def broken(:\n    pass")
        models, *_ = parse_python_file(bad_file, "test")
        assert models == []  # Best-effort: no crash


class TestXmlParser:
    """Test XML and CSV parsing."""

    def test_parse_access_csv(self) -> None:
        rights = parse_access_csv(FIXTURE_PATH / "security" / "ir.model.access.csv")
        assert len(rights) == 3
        user_right = next(r for r in rights if r.id == "access_sale_order_user")
        assert user_right.perm_read is True
        assert user_right.perm_unlink is False

    def test_parse_views_xml(self) -> None:
        views, rules, groups, menus = parse_xml_file(
            FIXTURE_PATH / "views" / "sale_order_views.xml",
        )
        assert len(views) == 2  # form + tree
        form = next(v for v in views if "form" in v.id)
        assert form.model == "sale.order"
        assert form.type == "form"
        assert any(f.name == "partner_id" for f in form.fields)

    def test_parse_menus(self) -> None:
        _, _, _, menus = parse_xml_file(
            FIXTURE_PATH / "views" / "sale_order_views.xml",
        )
        assert len(menus) == 2
        root = next(m for m in menus if m.id == "menu_sale_root")
        assert root.name == "Sales"

    def test_parse_missing_file(self, tmp_path: Path) -> None:
        rights = parse_access_csv(tmp_path / "nonexistent.csv")
        assert rights == []


class TestAnalyzer:
    """Test full module analysis."""

    def test_analyze_test_sale(self) -> None:
        kg = analyze_module(FIXTURE_PATH)
        assert kg is not None
        assert kg.manifest.name == "Test Sales"
        assert len(kg.models) == 2
        assert len(kg.action_methods) >= 2
        assert len(kg.sql_constraints) == 1
        assert len(kg.access_rights) == 3
        assert len(kg.views) == 2
        assert len(kg.menus) == 2

    def test_analyze_nonexistent(self, tmp_path: Path) -> None:
        result = analyze_module(tmp_path)
        assert result is None  # No manifest

    def test_analyze_serializable(self) -> None:
        """Knowledge Graph must be JSON-serializable."""
        kg = analyze_module(FIXTURE_PATH)
        assert kg is not None
        json_str = kg.model_dump_json()
        assert len(json_str) > 100
        assert "sale.order" in json_str


class TestStorage:
    """Test Knowledge Graph persistence."""

    def test_save_and_load(self, tmp_path: Path) -> None:
        from odooai.knowledge.storage import load_module_kg, save_module_kg

        kg = analyze_module(FIXTURE_PATH)
        assert kg is not None

        save_module_kg(kg, "17.0", store_path=tmp_path)
        loaded = load_module_kg("test_sale", "17.0", store_path=tmp_path)

        assert loaded is not None
        assert loaded.manifest.name == kg.manifest.name
        assert len(loaded.models) == len(kg.models)

    def test_load_nonexistent(self, tmp_path: Path) -> None:
        from odooai.knowledge.storage import load_module_kg

        result = load_module_kg("fake", "17.0", store_path=tmp_path)
        assert result is None
