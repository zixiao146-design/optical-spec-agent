"""v0.9.0rc6 development plan checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc6_development_plan_tracks_dev_state_and_exit_criteria():
    path = ROOT / "docs" / "rc6_development_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Current public prerelease: v0.9.0rc5" in text
    assert "Current main development version: 0.9.0rc6.dev0" in text
    assert "v0.9.0rc6 tag: not created" in text
    assert "No PyPI upload and no repeat TestPyPI upload now" in text
    assert "Quality gates passed" in text
    assert "PyPI/TestPyPI decision explicit" in text
    assert "Elmer deferred or validated status explicit" in text
    assert "docs/v1_0_public_contract_freeze_checklist.md" in text
    assert "docs/publication_decision_record.md" in text
