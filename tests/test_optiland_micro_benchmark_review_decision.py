"""Optiland optional micro-benchmark maintainer review guards."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optiland_micro_benchmark_review_decision_is_recorded():
    review = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "optiland_micro_benchmark_review_2026-05-20.md"
    )
    assert review.exists()
    text = review.read_text(encoding="utf-8")

    assert "accepted as optional manual ray/path smoke evidence" in text
    assert "External solver/package executed: yes, Optiland only" in text
    assert "Gmsh rerun in this task: no" in text
    assert "Meep executed: no" in text
    assert "MPB executed: no" in text
    assert "Elmer executed: no" in text
    assert "PyPI/TestPyPI upload: no" in text
    assert "Tag/release action: no" in text
    assert "Production-grade physical validation claimed: no" in text
    assert "Formal convergence proof claimed: no" in text
    assert "Optical correctness claimed: no" in text
    assert "does not authorize PyPI publication" in text
    assert "does not authorize any further solver execution" in text
    assert "Meep may be considered next" in text
    assert "requires explicit OSA_SOLVER_PYTHON profile and separate approval" in text
    assert "MPB may be considered after Meep or separately" in text
    assert "Elmer remains deferred" in text
    assert "Gmsh and Optiland are already recorded; do not rerun" in text
