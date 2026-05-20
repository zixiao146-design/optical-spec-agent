"""Backend evidence review decision documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backend_evidence_review_decision_records_rc7_bounds():
    path = ROOT / "docs" / "backend_evidence_review_decision.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "sufficient to prepare v0.9.0rc7 release draft" in text
    assert "v0.9.0rc7 tag creation approval at decision time: not granted" in text
    assert "GitHub release approval at decision time: not granted" in text
    assert "PyPI publication approval: not granted" in text
    assert "v1.0.0 release approval: not granted" in text
    assert "v0.9.0rc7 is now the current public prerelease" in text
    assert "main has moved to 0.9.0rc8 development" in text

    for phrase in [
        "sub-agent audit",
        "backend capability report",
        "backend evidence review pack",
        "tool-call ledger",
        "design case cross-checks",
        "design requirement templates",
        "natural-language to optical-language matching",
        "source/monitor diagnostics",
        "observable diagnostics",
        "adapter-native source/monitor mapping",
        "adapter-native golden coverage metadata checks",
        "optical calculator reference sanity cases",
        "blocked external actions",
    ]:
        assert phrase in text

    assert "does not prove production-grade physical validation" in text
    assert "does not prove formal convergence" in text
    assert "does not prove real external solver results" in text
    assert "does not prove Elmer Level 3 validation" in text
    assert "does not authorize PyPI publication" in text
    assert "does not authorize v0.9.0rc8 tag/release creation" in text

    assert "No production-grade physical validation is claimed" in text
    assert "No formal convergence proof is claimed" in text
    assert "Elmer Level 3 remains deferred" in text
