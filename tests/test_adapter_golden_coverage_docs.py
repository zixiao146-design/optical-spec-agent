"""Adapter golden coverage documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adapter_golden_coverage_docs_exist_and_document_matrix():
    for relative in [
        "docs/adapter_native_golden_coverage_matrix.md",
        "docs/adapter_native_golden_coverage_matrix.zh-CN.md",
    ]:
        path = ROOT / relative
        assert path.exists(), relative
        text = path.read_text(encoding="utf-8")
        for phrase in [
            "Meep",
            "MPB",
            "Gmsh",
            "Elmer",
            "Optiland",
            "preview",
            "python scripts/check_adapter_native_golden.py",
        ]:
            assert phrase in text
        assert "GET /api/adapter-native-golden-coverage" in text
        assert (
            "does not execute" in text
            or "不执行" in text
        )
        assert (
            "production-grade physical validation" in text
            or "生产级物理验证" in text
        )
