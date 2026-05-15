"""Elmer Level 3 readiness documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_elmer_level3_readiness_tracks_pending_non_default_boundary():
    text = (ROOT / "docs" / "elmer_level3_readiness.md").read_text(encoding="utf-8")
    assert "Elmer current maturity: Level 2" in text
    assert "Target next maturity: Level 3" in text
    assert "ElmerSolver is not installed locally" in text
    assert "2026-05-15 install attempt: deferred" in text
    assert "Default tests do not require Elmer" in text
    assert "Default quality gates do not require Elmer execution" in text
    assert "Optional manual validation script: yes" in text
    assert "Actual Elmer execution recorded: no" in text
    assert "Manual validation report filled: no" in text
    assert "Level 3 achieved: no" in text
    assert "validation/elmer/elmer_install_deferred_2026-05-15.md" in text
    assert "does not make Elmer a default dependency" in text
    assert "does not claim production-grade physical validation" in text
    assert "does not claim a formal convergence proof" in text


def test_elmer_readiness_and_maturity_model_remain_level2_until_report_exists():
    maturity = (ROOT / "docs" / "adapter_maturity_model.md").read_text(encoding="utf-8")
    validation_dir = (ROOT / "validation" / "elmer" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "| Elmer | Level 2" in maturity
    assert "Level-3-ready" in maturity
    assert "Level 3 is not achieved" in maturity
    assert "2026-05-15 package-manager install" in maturity
    assert "scripts/run_optional_elmer_validation.sh" in maturity
    assert "No completed Elmer validation report is recorded" in validation_dir
    assert "elmer_install_deferred_2026-05-15.md" in validation_dir
