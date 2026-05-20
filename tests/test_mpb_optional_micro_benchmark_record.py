"""Recorded MPB optional micro-benchmark evidence tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mpb_optional_micro_benchmark_record_documents_scope_and_non_claims():
    approval = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "mpb_micro_benchmark_approval_2026-05-20.md"
    )
    evidence = ROOT / "validation" / "mpb" / "mpb_micro_benchmark_2026-05-20.md"
    assert approval.exists()
    assert evidence.exists()

    approval_text = approval.read_text(encoding="utf-8")
    evidence_text = evidence.read_text(encoding="utf-8")

    assert "Approval status: approved for this MPB run" in approval_text
    assert "Execution authorized: yes, MPB only" in approval_text
    assert (
        "OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python"
        in approval_text
    )
    assert "Meep benchmark authorized: no" in approval_text
    assert "Gmsh authorized: no" in approval_text
    assert "Optiland authorized: no" in approval_text
    assert "Elmer authorized: no" in approval_text
    assert "PyPI/TestPyPI/tag/release authorized: no" in approval_text

    assert "solver: MPB / `meep.mpb`" in evidence_text
    assert "passed: true" in evidence_text
    assert "external solver/package executed: yes, MPB / `meep.mpb` only" in evidence_text
    assert "Meep FDTD benchmark executed: no" in evidence_text
    assert "Gmsh executed: no" in evidence_text
    assert "Optiland executed: no" in evidence_text
    assert "Elmer executed: no" in evidence_text
    assert (
        "OSA_SOLVER_PYTHON`: `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python"
        in evidence_text
    )
    assert "PyPI/TestPyPI upload actions: no" in evidence_text
    assert "tag/release actions: no" in evidence_text
    assert "no production-grade physical validation" in evidence_text
    assert "no production-grade MPB validation" in evidence_text
    assert "no production band-structure validation" in evidence_text
    assert "no formal convergence proof" in evidence_text
    assert "no optical correctness claim" in evidence_text
