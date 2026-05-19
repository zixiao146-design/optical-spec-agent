"""v1.0 readiness scorecard checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_readiness_scorecard_exists_and_tracks_current_status():
    path = ROOT / "docs" / "v1_0_readiness_scorecard.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Current public prerelease: v0.9.0rc6" in text
    assert "Current main release draft: `0.9.0rc7`" in text
    assert "v1.0.0 not released" in text
    assert "PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0" in text
    assert "v1.0 readiness gap audit" in text
    assert "v0.9.0rc7 release draft readiness" in text
    assert "v1.0 decision matrix" in text
    assert "v1.0 public contract freeze checklist" in text
    assert "v1.0 public contract freeze confirmation package" in text
    assert "v1.0 public contract freeze status" in text
    assert "v1.0 contract frozen surface" in text
    assert "v1.0 contract non-goals" in text
    assert "v1.0 breaking change policy" in text
    assert "v1.0.0 release criteria" in text
    assert "v1.0.0 release plan" in text
    assert "RC to v1.0.0 transition path" in text
    assert "v1.0 PyPI decision gate" in text
    assert "v1.0.0 post-release verification plan" in text
    assert "Agent Studio frontend roadmap" in text
    assert "Agent Studio frontend MVP planning docs" in text
    assert "Agent Studio frontend MVP implementation under `frontend/`" in text
    assert "Agent Studio frontend MVP runbook" in text
    assert "docs/frontend_mvp_qa_checklist.md" in text
    assert "scripts/smoke_frontend_mvp.sh" in text
    assert "docs/frontend_mvp_product_spec.md" in text
    assert "docs/frontend_mvp_implementation_plan.md" in text
    assert "docs/frontend_mvp_runbook.md" in text
    assert "not a v1.0.0 blocker" in text
    assert "Publication decision record" in text
    assert "PyPI publication readiness checklist" in text
    assert "PyPI post-publication verification plan" in text
    assert "No production-grade physical validation" in text
    assert "No formal convergence proof" in text
    assert "TestPyPI upload approval for 0.9.0rc7: pending" in text
    assert "Quality gates" in text
    assert "TestPyPI upload exercised for 0.9.0rc6.dev0 through manual Trusted" in text
    assert "TestPyPI upload for 0.9.0rc7 is not performed and remains pending" in text
    assert "TestPyPI status record for 0.9.0rc6.dev0" in text
    assert "Publication decision record keeps PyPI publication not granted" in text
    assert "CI, quality gates, build, twine check" in text
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
    assert "v1.0 public contract freeze is approved for the documented surface" in text
    assert "PyPI publication remains a hard strategic decision" in text
    assert "not production-grade physical validation" in text
    assert "not production-grade optical validation" in text
    assert "docs/backend_evidence_review_decision.md" in text
    assert "backend evidence is sufficient to" in text
    assert "not approved" in text
