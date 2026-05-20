"""Optional solver micro-benchmark manifest tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_solver_validation_micro_benchmark_manifest_is_conservative():
    path = ROOT / "validation" / "solver_validation_micro_benchmarks.json"
    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["default_runs_solver"] is False
    assert payload["opt_in_required"] is True
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False
    solvers = {item["solver_name"]: item for item in payload["solvers"]}
    assert set(solvers) == {"gmsh", "meep", "mpb", "optiland", "elmer"}
    for name, item in solvers.items():
        assert item["default_runs_solver"] is False, name
        assert item["missing_solver_non_blocking"] is True, name
        assert item["production_grade_validation_claimed"] is False, name
        assert item["formal_convergence_proof_claimed"] is False, name
        assert item["optional_script"].startswith("scripts/run_optional_")
        assert item["opt_in_env_var"].startswith("OSA_RUN_OPTIONAL_")
        assert item["approval_required"] is True, name
        assert "I approve running the optional" in item["approval_phrase"], name
        assert item["expected_runtime_environment"], name
        assert item["expected_artifact_paths"], name
        assert item["cleanup_required"] is True, name
        assert item["default_in_quality_gates"] is False, name
        assert item["default_in_release_gates"] is False, name
        assert item["pypi_publication_related"] is False, name
        assert item["tag_release_related"] is False, name
        assert item["readiness_status"], name
    assert solvers["elmer"]["status"] == "deferred"
    assert solvers["elmer"]["readiness_status"] == "deferred_until_maintainable_install_route"
    assert "Level-3-ready" in solvers["elmer"]["current_maturity"]
