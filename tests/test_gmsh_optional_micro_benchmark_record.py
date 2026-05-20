"""Recorded Gmsh optional micro-benchmark evidence guards."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gmsh_optional_micro_benchmark_evidence_is_recorded():
    approval = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "gmsh_micro_benchmark_approval_2026-05-20.md"
    )
    evidence = ROOT / "validation" / "gmsh" / "gmsh_micro_benchmark_2026-05-20.md"
    review = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "gmsh_micro_benchmark_review_2026-05-20.md"
    )
    assert approval.exists()
    assert evidence.exists()
    assert review.exists()
    approval_text = approval.read_text(encoding="utf-8")
    evidence_text = evidence.read_text(encoding="utf-8")
    combined = f"{approval_text}\n{evidence_text}"
    assert "Approval status: approved for this Gmsh run" in approval_text
    assert "Execution authorized: yes, Gmsh only" in approval_text
    assert "Solver execution performed: yes, Gmsh only" in approval_text
    assert "Passed: yes" in evidence_text
    assert "External solver executed: yes, Gmsh only." in evidence_text
    assert "Meep executed: no." in evidence_text
    assert "MPB executed: no." in evidence_text
    assert "Optiland executed: no." in evidence_text
    assert "Elmer executed: no." in evidence_text
    assert "PyPI upload or publication: no." in evidence_text
    assert "TestPyPI upload: no." in evidence_text
    assert "Git tag or GitHub release creation: no." in evidence_text
    assert "Production-grade physical validation claimed: no." in evidence_text
    assert "Formal convergence proof claimed: no." in evidence_text
    assert "Optical correctness claimed: no." in evidence_text
    assert "mesh generation evidence" in combined
