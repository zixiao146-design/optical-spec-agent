"""Recorded Gmsh manual validation evidence checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "validation" / "gmsh" / "gmsh_validation_pilot_2026-05-14.md"


def test_gmsh_manual_validation_report_bounds_level3_claims():
    assert REPORT.exists()
    text = REPORT.read_text(encoding="utf-8")
    assert "Project version: 0.9.0rc5.dev0" in text
    assert "Adapter family: gmsh" in text
    assert "Solver name: Gmsh" in text
    assert "Solver version: 4.15.2-git" in text
    assert "Command run:" in text
    assert "OSA_RUN_OPTIONAL_GMSH_VALIDATION" not in text
    assert "opt-in" in text.lower() or "optional manual validation" in text.lower()
    assert "Pass/fail: pass" in text
    assert "Production-grade validation supported: no" in text
    assert "Formal convergence proof supported: no" in text
    assert "This is not production-grade physical validation" in text
    assert "This is not a formal convergence proof" in text
    assert "This does not make Gmsh a default dependency" in text


def test_gmsh_report_and_maturity_model_are_consistent():
    maturity = (ROOT / "docs" / "adapter_maturity_model.md").read_text(encoding="utf-8")
    readiness = (ROOT / "docs" / "gmsh_level3_readiness.md").read_text(encoding="utf-8")
    assert "| Gmsh | Level 3" in maturity
    assert "validation/gmsh/gmsh_validation_pilot_2026-05-14.md" in maturity
    assert "Current maturity: Level 3" in readiness
    assert "Level 3 achieved: yes" in readiness
    assert "Default pytest does not run Gmsh" in readiness
    assert "This evidence does not claim production-grade physical validation" in readiness
    assert "This evidence does not claim a formal convergence proof" in readiness
