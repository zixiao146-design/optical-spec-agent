"""Design requirement documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_design_requirement_docs_exist_and_document_mapping():
    for filename in [
        "design_requirement_templates.md",
        "design_requirement_templates.zh-CN.md",
        "natural_language_to_optical_language.md",
        "natural_language_to_optical_language.zh-CN.md",
    ]:
        path = ROOT / "docs" / filename
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "natural language" in text.lower() or "自然语言" in text
        assert "optical language" in text.lower() or "光学语言" in text
        assert "external LLM" in text or "外部 LLM" in text
        assert "production-grade" in text or "生产级" in text
        assert "formal convergence proof" in text or "形式化收敛证明" in text

