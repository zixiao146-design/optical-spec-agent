"""MPB optional micro-benchmark decision packet tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mpb_optional_micro_benchmark_decision_packet_records_pending_boundaries():
    path = (
        ROOT
        / "docs"
        / "optional_solver_approval_records"
        / "mpb_micro_benchmark_decision_packet.md"
    )
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "MPB micro-benchmark approval: pending" in text
    assert "MPB execution authorized: no" in text
    assert "MPB executed: no" in text
    assert "Meep executed in this task: no" in text
    assert "Gmsh executed in this task: no" in text
    assert "Optiland executed in this task: no" in text
    assert "Elmer executed: no" in text
    assert "OSA_SOLVER_PYTHON" in text
    assert "OSA_SOLVER_READINESS_PROFILE=osa-solvers" in text
    assert "from meep import mpb" in text
    assert "MPB CLI is not required" in text
    assert (
        "I approve running the optional MPB micro-benchmark for optical-spec-agent "
        "using OSA_SOLVER_PYTHON=<path>."
    ) in text
    assert "DO NOT RUN WITHOUT APPROVAL" in text
    assert "OSA_RUN_OPTIONAL_MPB_VALIDATION=1" in text
    assert "OSA_MPB_VALIDATION_REPORT=/tmp/osa-mpb-micro-benchmark-report.json" in text
    assert "OSA_MPB_OUTPUT_DIR=/tmp/osa-mpb-micro-benchmark-output" in text
    assert "PyPI publication: not approved" in text
    assert "TestPyPI upload: not approved" in text
    assert "tag/release creation: not approved" in text
    assert "`v1.0.0` release: not approved" in text
    assert "no production-grade MPB validation" in text
    assert "no production-grade physical validation" in text
    assert "no formal convergence proof" in text
    assert "no optical correctness claim" in text
    assert "no default solver dependency" in text
    assert "no release gate behavior" in text
