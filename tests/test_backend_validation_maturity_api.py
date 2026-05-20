"""Backend validation maturity API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_backend_validation_maturity_api_returns_safe_summary():
    client = TestClient(app)
    response = client.get("/api/backend-validation-maturity")
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["status"] == "ok"
    assert body["summary"]["record_count"] >= 17
    assert body["summary"]["calculator_maturity_level"] == "sanity_checked_preview"
    assert body["summary"]["application_domain_maturity_level"] == "benchmark_checked_preview"
    assert body["summary"]["adapter_source_monitor_maturity_level"] == "fixture_guarded_preview"
    assert body["summary"]["material_maturity_level"] == "documented_preview_user_must_verify"
    assert body["summary"]["optional_solver_micro_benchmark_default"] == "no_solver_execution"
    assert body["summary"]["optional_solver_micro_benchmarks_opt_in_required"] is True
    assert body["summary"]["optional_solver_readiness_available"] is True
    assert body["summary"]["optional_solver_approval_matrix_available"] is True
    assert body["summary"]["optional_solver_environment_profiles_available"] is True
    assert body["summary"]["optional_solver_execution_approval_packet_available"] is True
    assert body["summary"]["optional_solver_approval_records_present"] is True
    assert body["summary"]["optional_solver_execution_default"] is False
    assert body["summary"]["explicit_solver_approval_required"] is True
    assert body["summary"]["all_optional_solver_execution_authorized"] is False
    assert body["summary"]["gmsh_optional_micro_benchmark_status"] == "passed_2026-05-20"
    assert (
        body["summary"]["gmsh_optional_micro_benchmark_review_status"]
        == "accepted_as_optional_manual_mesh_generation_smoke_evidence"
    )
    assert body["summary"]["optiland_optional_micro_benchmark_status"] == "passed_2026-05-20"
    assert (
        body["summary"]["optiland_optional_micro_benchmark_review_status"]
        == "accepted_as_optional_manual_ray_path_smoke_evidence"
    )
    assert body["summary"]["meep_optional_micro_benchmark_decision_packet_available"] is True
    assert body["summary"]["meep_optional_micro_benchmark_status"] == "pending_not_run"
    assert (
        body["summary"]["next_optional_solver_candidate"]
        == "meep_requires_osa_solver_python_not_approved"
    )
    assert body["summary"]["elmer_micro_benchmark_status"] == "deferred"
    component_ids = {record["component_id"] for record in body["records"]}
    assert "fiber_coupling_calculator" in component_ids
    assert "polarization_calculator" in component_ids
    assert "adapter_golden_coverage" in component_ids
    assert "gmsh_optional_solver_micro_benchmark" in component_ids
    assert "elmer_optional_solver_micro_benchmark" in component_ids
    assert "tool_call_ledger" in component_ids
    assert "not a production-grade optical constants database" in body["preview_boundary_summary"]["materials"]
    assert "OSA_SOLVER_PYTHON" in body["preview_boundary_summary"]["optional_solver_micro_benchmarks"]
    assert "one-solver-at-a-time" in body["preview_boundary_summary"]["optional_solver_micro_benchmarks"]
    assert "reviewed ray/path smoke evidence" in body["preview_boundary_summary"]["optional_solver_micro_benchmarks"]
    assert "Meep-specific decision packet" in body["preview_boundary_summary"]["optional_solver_micro_benchmarks"]
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    assert body["production_grade_validation_claimed"] is False
    assert body["formal_convergence_proof_claimed"] is False
