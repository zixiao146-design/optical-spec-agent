"""Recorded Optiland manual validation evidence checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "validation" / "optiland" / "optiland_validation_pilot_2026-05-14.md"


def test_optiland_manual_validation_report_bounds_level3_claims():
    assert REPORT.exists()
    text = REPORT.read_text(encoding="utf-8")
    assert "Project version: 0.9.0rc5.dev0" in text
    assert "Adapter family: optiland" in text
    assert "Backend name: Optiland" in text
    assert "Backend version: 0.6.0" in text
    assert "Python executable:" in text
    assert "Command run:" in text
    assert "Pass/fail:" in text
    assert "pass" in text
    assert "Production-grade validation supported:" in text
    assert "no" in text
    assert "Formal convergence proof supported:" in text
    assert "This is not production-grade optical validation" in text
    assert "This is not a formal convergence proof" in text
    assert "This does not make Optiland a default dependency" in text


def test_optiland_report_and_maturity_model_are_consistent():
    maturity = (ROOT / "docs" / "adapter_maturity_model.md").read_text(encoding="utf-8")
    readiness = (ROOT / "docs" / "optiland_level3_readiness.md").read_text(
        encoding="utf-8"
    )
    assert "| Optiland | Level 3" in maturity
    assert "validation/optiland/optiland_validation_pilot_2026-05-14.md" in maturity
    assert "Optiland current maturity: Level 3" in readiness
    assert "Level 3 achieved: yes" in readiness
    assert "Default pytest does not run Optiland" in readiness
    assert "This evidence does not claim production-grade optical validation" in readiness
    assert "This evidence does not claim a formal convergence proof" in readiness
