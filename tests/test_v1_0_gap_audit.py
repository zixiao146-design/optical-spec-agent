"""v1.0 readiness gap audit checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_gap_audit_tracks_current_baseline_and_blockers():
    path = ROOT / "docs" / "v1_0_gap_audit.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Current public prerelease: v0.9.0rc5" in text
    assert "Current main development version: 0.9.0rc6.dev0" in text
    assert "PyPI: not published" in text
    assert "TestPyPI: not uploaded" in text
    assert "Elmer Level 3 validation deferred" in text
    assert "Production-grade physical validation not claimed" in text
    assert "Formal convergence proof not claimed" in text
    assert "Public contract freeze" in text
    assert "Hard blocker for v1.0" in text
    assert "TestPyPI upload not exercised" in text
    assert "PyPI publication not approved" in text
    assert "docs/v1_0_public_contract_freeze_checklist.md" in text
    assert "docs/publication_decision_record.md" in text
