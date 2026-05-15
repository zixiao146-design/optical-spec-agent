"""Elmer install-deferred evidence checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_elmer_install_deferred_record_is_not_level3_evidence():
    record = ROOT / "validation" / "elmer" / "elmer_install_deferred_2026-05-15.md"
    assert record.exists()
    text = record.read_text(encoding="utf-8")
    required = [
        "Current status: install deferred",
        "`ElmerSolver` available: no",
        "Optional validation enabled: no",
        "Elmer executed: no",
        "Level 3 achieved: no",
        "Completed manual validation report recorded: no",
        "not Level 3 validation evidence",
        "does not make Elmer a default dependency",
        "not production-grade physical validation",
        "not a formal convergence proof",
    ]
    for phrase in required:
        assert phrase in text


def test_elmer_has_no_completed_manual_validation_report_yet():
    reports = list((ROOT / "validation" / "elmer").glob("elmer_validation_pilot_*.md"))
    assert reports == []
    maturity = (ROOT / "docs" / "adapter_maturity_model.md").read_text(
        encoding="utf-8"
    )
    assert "| Elmer | Level 2" in maturity
    assert "Level 3 is not achieved" in maturity
