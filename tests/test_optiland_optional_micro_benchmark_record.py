"""Recorded Optiland optional micro-benchmark evidence guards."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optiland_optional_micro_benchmark_evidence_is_recorded():
    approval = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "optiland_micro_benchmark_approval_2026-05-20.md"
    )
    evidence = ROOT / "validation" / "optiland" / "optiland_micro_benchmark_2026-05-20.md"
    assert approval.exists()
    assert evidence.exists()

    approval_text = approval.read_text(encoding="utf-8")
    evidence_text = evidence.read_text(encoding="utf-8")
    combined = f"{approval_text}\n{evidence_text}"

    assert "Approval status: approved for this Optiland run" in approval_text
    assert "Execution authorized: yes, Optiland only" in approval_text
    assert "Other solvers authorized: no" in approval_text
    assert "PyPI/TestPyPI/tag/release authorized: no" in approval_text
    assert "I approve running the optional Optiland micro-benchmark" in approval_text
    assert "Passed: yes" in evidence_text
    assert "External solver/package executed: yes, Optiland only" in evidence_text
    assert "Gmsh executed in this task: no" in evidence_text
    assert "Meep executed in this task: no" in evidence_text
    assert "MPB executed in this task: no" in evidence_text
    assert "Elmer executed in this task: no" in evidence_text
    assert "PyPI/TestPyPI upload actions: no" in evidence_text
    assert "Tag/release actions: no" in evidence_text
    assert "Production-grade physical validation claimed: no" in evidence_text
    assert "Formal convergence proof claimed: no" in evidence_text
    assert "Optical correctness claimed: no" in evidence_text
    assert "ray/path smoke" in combined
    assert "evidence" in combined
