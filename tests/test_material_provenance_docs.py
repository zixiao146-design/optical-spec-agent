"""Material provenance documentation tests."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_material_provenance_docs_exist_and_state_boundaries():
    for path in [
        ROOT / "docs" / "material_provenance_policy.md",
        ROOT / "docs" / "material_provenance_policy.zh-CN.md",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "preview" in text
        assert "production-grade" in text or "生产级" in text
        assert "no external" in text.lower() or "不会联网" in text
