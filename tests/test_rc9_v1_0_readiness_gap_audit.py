"""rc9 v1.0 readiness gap audit checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc9_v1_0_readiness_gap_audit_records_current_state_and_blockers():
    path = ROOT / "docs" / "rc9_v1_0_readiness_gap_audit.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Current public prerelease: v0.9.0rc8" in text
    assert "Current main development version: 0.9.0rc9.dev0" in text
    assert "v1.0 public contract freeze: approved" in text
    assert "Explicit v1.0.0 release approval is not granted" in text
    assert "PyPI publication decision is not granted" in text
    assert "Final v1.0.0 release verification has not been run" in text


def test_rc9_v1_0_readiness_gap_audit_keeps_deferred_items_bounded():
    text = (ROOT / "docs" / "rc9_v1_0_readiness_gap_audit.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "Elmer remains deferred and not Level 3",
        "No production-grade physical validation is claimed",
        "No production-grade solver validation is claimed",
        "No formal convergence proof is claimed",
        "No optical correctness claim is made",
        "PyPI publication remains separately gated",
    ]:
        assert phrase in text
