"""Docs tests for optical calculator case integration."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optical_calculator_case_integration_docs_exist_and_are_safe():
    docs = [
        ROOT / "docs" / "optical_calculator_case_integration.md",
        ROOT / "docs" / "optical_calculator_case_integration.zh-CN.md",
    ]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "thin_film_coating" in text
        assert "waveguide_mode" in text
        assert "lens_raytrace_preview" in text
        assert "tool_call_ledger" in text
        assert "No production-grade physical validation is claimed" in text or "不声明生产级物理验证" in text
        assert "No external solver is executed" in text or "默认不执行外部求解器" in text
