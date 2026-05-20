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
    assert payload["optional_solver_evidence_summary_path"] == (
        "docs/optional_solver_evidence_summary.md"
    )
    assert payload["rc8_backend_readiness_review_path"] == (
        "docs/rc8_backend_readiness_review.md"
    )
    assert payload["solver_evidence_validation_maturity_mapping_path"] == (
        "docs/solver_evidence_validation_maturity_mapping.md"
    )
    assert payload["optional_solver_evidence_review_complete"] is True
    assert payload["solver_evidence_closed_for"] == ["gmsh", "optiland", "meep", "mpb"]
    assert payload["solver_evidence_deferred_for"] == ["elmer"]
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
    assert solvers["gmsh"]["next_candidate_solver"] == "elmer_deferred"
    assert solvers["gmsh"]["next_candidate_approved"] is False
    assert solvers["gmsh"]["no_further_solver_authorized"] is True
    assert "gmsh_micro_benchmark_approval_2026-05-20.md" in solvers["gmsh"]["approval_record_path"]
    assert solvers["gmsh"]["pending_approval_template_path"].endswith(
        "gmsh_micro_benchmark_approval_pending.md"
    )
    assert "meep" in solvers["meep"]["module_names"]
    assert solvers["meep"]["execution_sequence_rank"] == 3
    assert solvers["meep"]["solver_python_required"] is True
    assert solvers["meep"]["approval_status"] == "approved_executed"
    assert solvers["meep"]["execution_authorized"] is False
    assert solvers["meep"]["last_execution_status"] == "passed"
    assert solvers["meep"]["last_execution_date"] == "2026-05-20"
    assert solvers["meep"]["last_execution_evidence"] == (
        "validation/meep/meep_micro_benchmark_2026-05-20.md"
    )
    assert solvers["meep"]["review_record_path"] == (
        "docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        solvers["meep"]["review_status"]
        == "accepted_as_optional_manual_pymeep_fdtd_smoke_evidence"
    )
    assert solvers["meep"]["no_further_solver_authorized"] is True
    assert solvers["meep"]["next_candidate_solver"] == "elmer_deferred"
    assert solvers["meep"]["decision_packet_path"] == (
        "docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md"
    )
    assert solvers["meep"]["readiness_profile"] == "osa-solvers"
    assert solvers["meep"]["approval_phrase"] == (
        "I approve running the optional Meep micro-benchmark for optical-spec-agent "
        "using OSA_SOLVER_PYTHON=<path>."
    )
    assert "no future Meep rerun is authorized" in solvers["meep"][
        "recommended_next_action"
    ]
    assert "validation/meep/meep_micro_benchmark_2026-05-20.md" in solvers["meep"]["evidence_refs"]
    assert (
        "docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md"
        in solvers["meep"]["evidence_refs"]
    )
    assert "meep.mpb" in solvers["mpb"]["module_names"]
    assert solvers["mpb"]["execution_sequence_rank"] == 4
    assert solvers["mpb"]["solver_python_required"] is True
    assert solvers["mpb"]["approval_status"] == "approved_executed"
    assert solvers["mpb"]["execution_authorized"] is False
    assert solvers["mpb"]["last_execution_status"] == "passed"
    assert solvers["mpb"]["last_execution_date"] == "2026-05-20"
    assert solvers["mpb"]["last_execution_evidence"] == (
        "validation/mpb/mpb_micro_benchmark_2026-05-20.md"
    )
    assert solvers["mpb"]["review_record_path"] == (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        solvers["mpb"]["review_status"]
        == "accepted_as_optional_manual_mpb_band_structure_smoke_evidence"
    )
    assert solvers["mpb"]["review_decision_date"] == "2026-05-20"
    assert solvers["mpb"]["next_candidate_solver"] == "elmer_deferred"
    assert solvers["mpb"]["next_candidate_approved"] is False
    assert solvers["mpb"]["no_further_solver_authorized"] is True
    assert solvers["mpb"]["approval_record_path"] == (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md"
    )
    assert solvers["mpb"]["decision_packet_path"] == (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md"
    )
    assert solvers["mpb"]["readiness_profile"] == "osa-solvers"
    assert solvers["mpb"]["cli_required"] is False
    assert solvers["mpb"]["approval_phrase"] == (
        "I approve running the optional MPB micro-benchmark for optical-spec-agent "
        "using OSA_SOLVER_PYTHON=<path>."
    )
    assert "MPB evidence is reviewed and accepted" in solvers["mpb"]["recommended_next_action"]
    assert "No future MPB rerun" in solvers["mpb"]["recommended_next_action"]
    assert "validation/mpb/mpb_micro_benchmark_2026-05-20.md" in solvers["mpb"]["evidence_refs"]
    assert (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md"
        in solvers["mpb"]["evidence_refs"]
    )
    assert (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_review_2026-05-20.md"
        in solvers["mpb"]["evidence_refs"]
    )
    assert (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md"
        in solvers["mpb"]["evidence_refs"]
    )
    assert (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_approval_pending.md"
        in solvers["mpb"]["evidence_refs"]
    )
    assert "/tmp/osa-mpb-micro-benchmark-report.json" in solvers["mpb"]["expected_artifact_paths"]
    assert "optiland" in solvers["optiland"]["module_names"]
    assert solvers["optiland"]["execution_sequence_rank"] == 2
    assert solvers["optiland"]["approval_status"] == "approved_executed"
    assert solvers["optiland"]["execution_authorized"] is False
    assert solvers["optiland"]["last_execution_status"] == "passed"
    assert solvers["optiland"]["last_execution_date"] == "2026-05-20"
    assert solvers["optiland"]["last_execution_evidence"] == (
        "validation/optiland/optiland_micro_benchmark_2026-05-20.md"
    )
    assert solvers["optiland"]["review_record_path"] == (
        "docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        solvers["optiland"]["review_status"]
        == "accepted_as_optional_manual_ray_path_smoke_evidence"
    )
    assert "optiland_micro_benchmark_approval_2026-05-20.md" in solvers["optiland"]["approval_record_path"]
    assert solvers["optiland"]["next_candidate_solver"] == "elmer_deferred"
    assert solvers["optiland"]["next_candidate_approved"] is False
    assert solvers["optiland"]["no_further_solver_authorized"] is True
    assert solvers["elmer"]["command_names"] == ["ElmerSolver"]
    assert solvers["elmer"]["execution_sequence_rank"] == 99
    assert solvers["elmer"]["approval_status"] == "deferred"
    assert solvers["elmer"]["status"] == "deferred"
    assert solvers["elmer"]["readiness_status"] == "deferred_until_maintainable_install_route"
    assert "Level-3-ready" in solvers["elmer"]["current_maturity"]
