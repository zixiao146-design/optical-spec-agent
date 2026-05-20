"""Maintainer review decision guards for the Gmsh micro-benchmark."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gmsh_micro_benchmark_review_decision_is_recorded():
    review = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "gmsh_micro_benchmark_review_2026-05-20.md"
    )
    assert review.exists()
    text = review.read_text(encoding="utf-8")
    assert "accepted as optional manual mesh-generation smoke evidence" in text
    assert "Production-grade physical validation claimed: no" in text
    assert "Formal convergence proof claimed: no" in text
    assert "Optical correctness claimed: no" in text
    assert "Other solvers executed: no" in text
    assert "PyPI/TestPyPI upload: no" in text
    assert "Tag/release action: no" in text
    assert "does not authorize any further solver execution" in text
    assert "Optiland may be considered next, but requires separate explicit approval" in text
    assert "Meep / MPB require explicit `OSA_SOLVER_PYTHON` profile" in text
    assert "Elmer remains deferred" in text
