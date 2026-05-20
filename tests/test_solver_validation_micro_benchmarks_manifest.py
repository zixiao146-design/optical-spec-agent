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
        assert item["python_probe_supported"] in {True, False}, name
        assert item["cli_probe_supported"] in {True, False}, name
        assert item["profile_sensitive"] in {True, False}, name
        assert item["recommended_profile"], name
        assert isinstance(item["module_names"], list), name
        assert isinstance(item["command_names"], list), name
        assert item["solver_python_env_var"] == "OSA_SOLVER_PYTHON", name
        assert isinstance(item["execution_sequence_rank"], int), name
        assert item["approval_record_path"].startswith(
            "docs/optional_solver_approval_records/"
        ), name
        assert item["approval_status"] in {"pending", "deferred", "approved_executed"}, name
        assert item["execution_authorized"] is False, name
        assert item["last_execution_status"] in {"not_run", "passed"}, name
        assert item["recommended_next_action"], name
        assert item["environment_profile_required"], name
        assert item["solver_python_required"] in {True, False}, name
    assert solvers["gmsh"]["command_names"] == ["gmsh"]
    assert solvers["gmsh"]["execution_sequence_rank"] == 1
    assert solvers["gmsh"]["approval_status"] == "approved_executed"
    assert solvers["gmsh"]["last_execution_status"] == "passed"
    assert solvers["gmsh"]["last_execution_date"] == "2026-05-20"
    assert solvers["gmsh"]["last_execution_evidence"] == (
        "validation/gmsh/gmsh_micro_benchmark_2026-05-20.md"
    )
    assert solvers["gmsh"]["review_record_path"] == (
        "docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        solvers["gmsh"]["review_status"]
        == "accepted_as_optional_manual_mesh_generation_smoke_evidence"
    )
    assert solvers["gmsh"]["next_candidate_solver"] == "optiland"
    assert solvers["gmsh"]["next_candidate_approved"] is False
    assert solvers["gmsh"]["no_further_solver_authorized"] is True
    assert "gmsh_micro_benchmark_approval_2026-05-20.md" in solvers["gmsh"]["approval_record_path"]
    assert solvers["gmsh"]["pending_approval_template_path"].endswith(
        "gmsh_micro_benchmark_approval_pending.md"
    )
    assert "meep" in solvers["meep"]["module_names"]
    assert solvers["meep"]["execution_sequence_rank"] == 3
    assert solvers["meep"]["solver_python_required"] is True
    assert "meep.mpb" in solvers["mpb"]["module_names"]
    assert solvers["mpb"]["execution_sequence_rank"] == 4
    assert solvers["mpb"]["solver_python_required"] is True
    assert "optiland" in solvers["optiland"]["module_names"]
    assert solvers["optiland"]["execution_sequence_rank"] == 2
    assert solvers["optiland"]["approval_status"] == "pending"
    assert solvers["optiland"]["execution_authorized"] is False
    assert solvers["elmer"]["command_names"] == ["ElmerSolver"]
    assert solvers["elmer"]["execution_sequence_rank"] == 99
    assert solvers["elmer"]["approval_status"] == "deferred"
    assert solvers["elmer"]["status"] == "deferred"
    assert solvers["elmer"]["readiness_status"] == "deferred_until_maintainable_install_route"
    assert "Level-3-ready" in solvers["elmer"]["current_maturity"]
