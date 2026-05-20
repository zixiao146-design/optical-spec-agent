"""MPB optional micro-benchmark review decision tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mpb_micro_benchmark_review_decision_records_acceptance_and_boundaries():
    path = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "mpb_micro_benchmark_review_2026-05-20.md"
    )
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "accepted as optional manual MPB / band-structure smoke evidence" in text
    assert "MPB / PyMeep version: 1.33.0" in text
    assert (
        "/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python"
        in text
    )
    assert "MPB CLI required: no" in text
    assert "Execution path: `meep.mpb` through solver Python profile" in text
    assert "Production-grade physical validation claimed: no" in text
    assert "Production-grade MPB validation claimed: no" in text
    assert "Production band-structure validation claimed: no" in text
    assert "Formal convergence proof claimed: no" in text
    assert "Optical correctness claimed: no" in text
    assert "Meep FDTD benchmark executed: no" in text
    assert "Gmsh rerun in this task: no" in text
    assert "Optiland rerun in this task: no" in text
    assert "Elmer executed: no" in text
    assert "PyPI/TestPyPI upload: no" in text
    assert "Tag/release action: no" in text
    assert "This evidence does not authorize any further solver execution." in text
    assert "This evidence does not authorize Elmer execution." in text
    assert "Elmer remains deferred until a maintainable install route exists." in text
    for solver in ["Gmsh", "Optiland", "Meep", "MPB"]:
        assert f"{solver}: executed, passed, reviewed / accepted" in text
    assert "Elmer: deferred, not Level 3" in text
