"""MPB Level 3 readiness documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mpb_level3_readiness_records_optional_boundaries():
    text = (ROOT / "docs" / "mpb_level3_readiness.md").read_text(encoding="utf-8")
    assert "MPB current maturity: Level 3" in text
    assert "Level 3 achieved: yes" in text
    assert "MPB CLI is not required" in text
    assert "Default pytest does not run MPB" in text
    assert "validation/mpb/mpb_validation_pilot_2026-05-14.md" in text
    assert "This evidence does not claim production-grade physical validation" in text
    assert "This evidence does not claim a formal convergence proof" in text
