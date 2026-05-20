"""Recorded Meep optional micro-benchmark evidence tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_meep_optional_micro_benchmark_record_exists_and_preserves_boundaries():
    approval = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "meep_micro_benchmark_approval_2026-05-20.md"
    )
    evidence = ROOT / "validation" / "meep" / "meep_micro_benchmark_2026-05-20.md"
    review = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "meep_micro_benchmark_review_2026-05-20.md"
    )
    assert approval.exists()
    assert evidence.exists()
    assert review.exists()

    approval_text = approval.read_text(encoding="utf-8")
    evidence_text = evidence.read_text(encoding="utf-8")
    review_text = review.read_text(encoding="utf-8")
    combined = approval_text + "\n" + evidence_text + "\n" + review_text

    assert "approved for this Meep run" in approval_text
    assert "Execution authorized: yes, Meep only" in approval_text
    assert (
        "OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python"
        in approval_text
    )
    assert "External solver/package executed: yes, Meep only" in evidence_text
    assert "MPB executed: no" in evidence_text
    assert "Gmsh executed in this task: no" in evidence_text
    assert "Optiland executed in this task: no" in evidence_text
    assert "Elmer executed: no" in evidence_text
    assert "Meep version: `1.33.0`" in evidence_text
    assert "Passed: yes" in evidence_text
    assert "PyPI/TestPyPI upload actions: no" in evidence_text
    assert "Tag/release actions: no" in evidence_text
    assert "Production-grade physical validation claimed: no" in combined
    assert "Production-grade FDTD validation claimed: no" in evidence_text
    assert "Formal convergence proof claimed: no" in combined
    assert "Optical correctness claimed: no" in evidence_text
    assert "accepted as optional manual PyMeep/FDTD smoke evidence" in review_text
    assert "Production-grade FDTD validation claimed: no" in review_text
