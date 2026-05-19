"""Docs for fiber and polarization preview calculators."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_fiber_and_polarization_docs_exist_and_bound_claims():
    docs = [
        ROOT / "docs" / "fiber_coupling_preview_calculator.md",
        ROOT / "docs" / "fiber_coupling_preview_calculator.zh-CN.md",
        ROOT / "docs" / "polarization_preview_calculator.md",
        ROOT / "docs" / "polarization_preview_calculator.zh-CN.md",
    ]
    for path in docs:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8").lower()
        assert "preview" in text or "预览" in text
        assert "no external solver" in text or "不执行外部求解器" in text
        assert "production-grade physical validation" in text or "生产级物理验证" in text
        assert "formal convergence proof" in text or "形式化收敛证明" in text
