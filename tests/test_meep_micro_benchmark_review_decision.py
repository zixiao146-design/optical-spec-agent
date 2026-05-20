"""Maintainer review decision guards for the Meep micro-benchmark."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_meep_micro_benchmark_review_decision_is_recorded():
    review = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "meep_micro_benchmark_review_2026-05-20.md"
    )
    assert review.exists()
    text = review.read_text(encoding="utf-8")

    assert "accepted as optional manual PyMeep/FDTD smoke evidence" in text
    assert "Meep / PyMeep version: 1.33.0" in text
    assert (
        "OSA_SOLVER_PYTHON: /opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python"
        in text
    )
    assert "External solver/package executed: yes, Meep only" in text
    assert "MPB executed: no" in text
    assert "Gmsh rerun in this task: no" in text
    assert "Optiland rerun in this task: no" in text
    assert "Elmer executed: no" in text
    assert "PyPI/TestPyPI upload: no" in text
    assert "Tag/release action: no" in text
    assert "Production-grade physical validation claimed: no" in text
    assert "Production-grade FDTD validation claimed: no" in text
    assert "Formal convergence proof claimed: no" in text
    assert "Optical correctness claimed: no" in text
    assert "does not authorize PyPI publication" in text
    assert "does not authorize any further solver execution" in text
    assert "does not authorize MPB execution" in text
    assert "MPB may be considered next" in text
    assert "requires explicit OSA_SOLVER_PYTHON profile and separate approval" in text
    assert "MPB approval must remain separate from Meep" in text
    assert "Elmer remains deferred" in text
    assert "Gmsh, Optiland, and Meep are already recorded; do not rerun" in text
