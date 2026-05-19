"""Optional solver micro-benchmark report schema tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_solver_micro_benchmark_report_schema_requires_safety_fields():
    path = (
        ROOT
        / "docs"
        / "manual_solver_validation_reports"
        / "solver_micro_benchmark_report_schema.json"
    )
    assert path.exists()
    schema = json.loads(path.read_text(encoding="utf-8"))
    required = set(schema["required"])
    for field in [
        "solver_name",
        "benchmark_id",
        "opt_in_env_var",
        "executed",
        "passed",
        "skipped_reason",
        "solver_version",
        "input_fixture",
        "output_artifacts",
        "production_grade_validation_claimed",
        "formal_convergence_proof_claimed",
        "external_solver_executed",
    ]:
        assert field in required
    assert schema["properties"]["production_grade_validation_claimed"]["const"] is False
    assert schema["properties"]["formal_convergence_proof_claimed"]["const"] is False

