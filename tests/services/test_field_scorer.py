"""Tests for field_scorer service."""

from odooai.services.field_scorer import score_field, select_top_fields


class TestScoreField:
    """Test individual field scoring."""

    def test_excluded_binary(self) -> None:
        assert score_field("image", {"type": "binary"}) == -1

    def test_excluded_html(self) -> None:
        assert score_field("body", {"type": "html"}) == -1

    def test_excluded_one2many(self) -> None:
        assert score_field("line_ids", {"type": "one2many"}) == -1

    def test_excluded_noise_prefix(self) -> None:
        assert score_field("message_ids", {"type": "one2many"}) == -1
        assert score_field("activity_date", {"type": "date"}) == -1

    def test_essential_field(self) -> None:
        assert score_field("id", {"type": "integer"}) == 1000
        assert score_field("name", {"type": "char"}) == 1000

    def test_required_bonus(self) -> None:
        score = score_field("partner_id", {"type": "many2one", "required": True})
        assert score >= 500  # required bonus + type + business

    def test_business_pattern_bonus(self) -> None:
        score = score_field("state", {"type": "selection"})
        assert score > score_field("random_field", {"type": "selection"})


class TestSelectTopFields:
    """Test top N field selection."""

    def test_basic_selection(self) -> None:
        fields_meta = {
            "id": {"type": "integer"},
            "name": {"type": "char"},
            "partner_id": {"type": "many2one", "required": True},
            "image": {"type": "binary"},
            "note": {"type": "text"},
        }
        result = select_top_fields(fields_meta, top_n=3)
        assert "id" in result
        assert "name" in result
        assert "image" not in result
        assert len(result) <= 4  # top_n + id if not already included

    def test_id_always_included(self) -> None:
        fields_meta = {f"field_{i}": {"type": "char", "required": True} for i in range(20)}
        result = select_top_fields(fields_meta, top_n=5)
        assert "id" in result

    def test_empty_fields(self) -> None:
        result = select_top_fields({}, top_n=15)
        assert result == ["id"]
