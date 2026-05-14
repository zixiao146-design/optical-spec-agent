"""Optiland Level 3 readiness documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optiland_level3_readiness_tracks_non_default_boundary():
    text = (ROOT / "docs" / "optiland_level3_readiness.md").read_text(encoding="utf-8")
    assert "Optiland current maturity: Level 3" in text
    assert "Target maturity achieved: Level 3" in text
    assert "Default pytest does not run Optiland" in text
    assert "Default quality gates do not require Optiland execution" in text
    assert "validation/optiland/optiland_validation_pilot_2026-05-14.md" in text
    assert "Level 3 achieved: yes" in text
    assert "This evidence does not claim production-grade optical validation" in text
    assert "This evidence does not claim a formal convergence proof" in text
    assert "This evidence does not make Optiland a default dependency" in text
