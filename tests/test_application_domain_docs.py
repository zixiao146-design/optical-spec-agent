"""Application-domain documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_application_domain_docs_exist_and_document_preview_boundaries():
    for rel in [
        "docs/application_domain_registry.md",
        "docs/application_domain_registry.zh-CN.md",
        "docs/material_template_cross_checks.md",
        "docs/material_template_cross_checks.zh-CN.md",
    ]:
        path = ROOT / rel
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "preview" in text.lower()
        assert "production" in text.lower() or "生产级" in text
        assert "solver" in text.lower() or "求解器" in text

