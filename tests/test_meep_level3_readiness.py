"""Meep Level 3 readiness documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_meep_level3_readiness_tracks_opt_in_boundaries():
    text = (ROOT / "docs" / "meep_level3_readiness.md").read_text(encoding="utf-8")
    assert "Meep current maturity: Level 3" in text
    assert "validation/meep/meep_validation_pilot_2026-05-14.md" in text
    assert "Actual Meep execution recorded: yes" in text
    assert "Level 3 achieved: yes" in text
    assert "Default pytest does not run Meep" in text
    assert "Default smoke does not run Meep" in text
    assert "Default quality gates do not execute Meep" in text
    assert "This evidence does not claim production-grade physical validation" in text
    assert "This evidence does not claim a formal convergence proof" in text
