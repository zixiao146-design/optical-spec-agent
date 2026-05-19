"""Ambiguous requirement matching documentation tests."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ambiguous_requirement_docs_exist_and_document_questions():
    for path in [
        ROOT / "docs" / "ambiguous_requirement_matching.md",
        ROOT / "docs" / "ambiguous_requirement_matching.zh-CN.md",
    ]:
        text = path.read_text(encoding="utf-8").lower()
        assert "confidence" in text or "置信度" in text
        assert "candidate" in text
        assert "questions" in text or "问题" in text
        assert "external llm" in text or "外部 llm" in text
