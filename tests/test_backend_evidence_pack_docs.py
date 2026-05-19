"""Backend evidence review pack documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backend_evidence_pack_docs_exist_and_document_limits():
    for filename in [
        "backend_evidence_review_pack.md",
        "backend_evidence_review_pack.zh-CN.md",
    ]:
        path = ROOT / "docs" / filename
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "generate_backend_evidence_pack.py" in text
        assert "smoke_backend_evidence_pack.sh" in text
        assert "preview/design-assist" in text
        assert "production-grade" in text
        assert "solver" in text.lower() or "求解器" in text
        assert "LLM" in text
        assert "tag" in text
        assert "release" in text
