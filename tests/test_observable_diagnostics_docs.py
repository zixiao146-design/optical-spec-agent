"""Observable diagnostics documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_observable_diagnostics_docs_exist_and_document_taxonomy():
    for doc_name in ["observable_diagnostics.md", "observable_diagnostics.zh-CN.md"]:
        path = ROOT / "docs" / doc_name
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        for phrase in [
            "scattering",
            "reflectance",
            "near",
            "far",
            "band",
            "focal",
            "mode",
            "phase",
            "mesh",
        ]:
            assert phrase in text.lower()
        assert "required input" in text.lower() or "必需输入" in text
        assert "preview" in text.lower() or "预览" in text
        assert "No production-grade physical validation" in text or "不声明生产级物理验证" in text
