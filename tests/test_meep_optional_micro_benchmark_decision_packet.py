"""Meep optional micro-benchmark decision packet tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_meep_optional_micro_benchmark_decision_packet_records_approved_run_and_boundaries():
    path = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "meep_micro_benchmark_decision_packet.md"
    )
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Meep micro-benchmark approval: approved for the 2026-05-20 Meep-only run" in text
    assert "Meep execution authorized: yes, for the 2026-05-20 Meep-only run only" in text
    assert "Meep executed: yes, passed on 2026-05-20" in text
    assert "Meep review status: accepted as optional manual PyMeep/FDTD smoke evidence" in text
    assert "meep_micro_benchmark_review_2026-05-20.md" in text
    assert "MPB executed: no" in text
    assert "Gmsh executed in this task: no" in text
    assert "Optiland executed in this task: no" in text
    assert "Elmer executed: no" in text
    assert "OSA_SOLVER_PYTHON" in text
    assert "OSA_SOLVER_READINESS_PROFILE=osa-solvers" in text
    assert (
        "I approve running the optional Meep micro-benchmark for optical-spec-agent "
        "using OSA_SOLVER_PYTHON=<path>."
    ) in text
    assert "Do not rerun without fresh approval" in text
    assert "OSA_RUN_OPTIONAL_MEEP_VALIDATION=1" in text
    assert "PyPI publication: not approved" in text
    assert "TestPyPI upload: not approved" in text
    assert "tag/release creation: not approved" in text
    assert "`v1.0.0` release: not approved" in text
    assert "no production-grade FDTD validation" in text
    assert "no formal convergence proof" in text
    assert "no optical correctness claim" in text
    assert "no default solver dependency" in text
    assert "no release gate behavior" in text
