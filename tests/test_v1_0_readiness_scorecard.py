"""v1.0 readiness scorecard checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_readiness_scorecard_exists_and_tracks_current_status():
    path = ROOT / "docs" / "v1_0_readiness_scorecard.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Current public prerelease: v0.9.0rc5" in text
    assert "Current main development version: `0.9.0rc6.dev0`" in text
    assert "v1.0.0 not released" in text
    assert "PyPI/TestPyPI: not published / not uploaded" in text
    assert "v1.0 readiness gap audit" in text
    assert "v0.9.0rc6 development plan" in text
    assert "v1.0 decision matrix" in text
    assert "v1.0 public contract freeze checklist" in text
    assert "Publication decision record" in text
    assert "No production-grade physical validation" in text
    assert "No formal convergence proof" in text
    assert "TestPyPI upload approval: granted for 0.9.0rc6.dev0 only" in text
    assert "Quality gates" in text
    assert "TestPyPI upload not approved/exercised" in text
    assert "Publication decision record keeps TestPyPI pending" in text
    assert "Optional open-source solver availability preflight" in text
    assert "Open-source solver preflight detects availability only" in text
    assert "Adapter maturity model" in text
    assert "Gmsh optional validation pilot" in text
    assert "Gmsh Level 3 optional manual validation evidence" in text
    assert "Meep optional validation pilot" in text
    assert "Meep Level 3 optional manual validation evidence" in text
    assert "MPB optional validation pilot" in text
    assert "MPB Level 3 optional manual validation evidence" in text
    assert "MPB CLI is not required" in text
    assert "Optiland optional validation pilot" in text
    assert "Optiland Level 3 optional manual validation evidence" in text
    assert "Elmer Level-3-ready optional validation path" in text
    assert "Elmer remains Level 2 pending ElmerSolver installation" in text
    assert "v1.0 public contract freeze remains a hard blocker" in text
    assert "not production-grade physical validation" in text
    assert "not production-grade optical validation" in text
