"""Backend evidence summary API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_backend_evidence_summary_api_returns_safe_review_sections():
    client = TestClient(app)
    response = client.get("/api/backend-evidence-summary")
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["evidence_pack_available"] is True
    assert body["preview_design_assist_only"] is True
    assert body["package_and_release_status"]["current_public_prerelease"] == "v0.9.0rc7"
    assert body["package_and_release_status"]["main_development_version"] == "0.9.0rc8.dev0"
    assert body["package_and_release_status"]["pypi_published"] is False
    assert len(body["sub_agent_reality"]) == 8
    assert body["tool_call_reality"]["internal_tools_executed"]
    assert {item["calculator_name"] for item in body["optical_calculators"]} == {
        "thin_film",
        "paraxial",
        "gaussian_beam",
        "waveguide",
        "fiber_coupling",
        "polarization",
    }
    calculators = {
        item["calculator_name"]: item for item in body["optical_calculators"]
    }
    assert (
        "fiber_gaussian_offset_loss"
        in calculators["fiber_coupling"]["sanity_reference_cases"]
    )
    assert (
        "jones_quarter_waveplate_phase_preview"
        in calculators["polarization"]["sanity_reference_cases"]
    )
    assert body["design_case_cross_checks"]
    assert body["source_monitor_observable_diagnostics"]["observable_taxonomy_available"] is True
    assert body["adapter_native_golden_coverage"]["status"] == "ok"
    assert body["application_domain_benchmarks"]["scenario_count"] >= 19
    assert body["application_domain_benchmarks"]["fail_count"] == 0
    assert body["application_domain_benchmarks"]["warn_count"] == 0
    assert body["application_domain_benchmarks"]["unsupported_requests_blocked_or_deferred"] is True
    assert body["validation_maturity_summary"]["summary"]["record_count"] >= 17
    assert (
        body["validation_maturity_summary"]["summary"]["application_domain_maturity_level"]
        == "benchmark_checked_preview"
    )
    assert body["validation_claim_audit_available"] is True
    assert body["optional_solver_micro_benchmarks"]["default_runs_solver"] is False
    assert body["optional_solver_micro_benchmarks"]["optional_solver_readiness_available"] is True
    assert body["optional_solver_micro_benchmarks"]["optional_solver_approval_matrix_available"] is True
    assert body["optional_solver_micro_benchmarks"]["optional_solver_environment_profiles_available"] is True
    assert body["optional_solver_micro_benchmarks"]["optional_solver_execution_approval_packet_available"] is True
    assert body["optional_solver_micro_benchmarks"]["optional_solver_approval_records_present"] is True
    assert body["optional_solver_micro_benchmarks"]["meep_decision_packet_available"] is True
    assert (
        body["optional_solver_micro_benchmarks"]["meep_decision_packet_path"]
        == "docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md"
    )
    assert body["optional_solver_micro_benchmarks"]["mpb_decision_packet_available"] is True
    assert (
        body["optional_solver_micro_benchmarks"]["mpb_decision_packet_path"]
        == "docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md"
    )
    assert body["optional_solver_micro_benchmarks"]["solver_python_env_var"] == "OSA_SOLVER_PYTHON"
    assert body["optional_solver_micro_benchmarks"]["optional_solver_execution_default"] is False
    assert body["optional_solver_micro_benchmarks"]["explicit_approval_required"] is True
    assert body["optional_solver_micro_benchmarks"]["all_optional_solver_execution_authorized"] is False
    assert body["optional_solver_micro_benchmarks"]["manual_opt_in_only"] is True
    gmsh = next(
        item
        for item in body["optional_solver_micro_benchmarks"]["solvers"]
        if item["solver_name"] == "gmsh"
    )
    assert gmsh["approval_status"] == "approved_executed"
    assert gmsh["last_execution_status"] == "passed"
    assert gmsh["review_record_path"].endswith(
        "gmsh_micro_benchmark_review_2026-05-20.md"
    )
    assert gmsh["next_candidate_solver"] == "mpb_after_osa_solver_python"
    assert gmsh["next_candidate_approved"] is False
    optiland = next(
        item
        for item in body["optional_solver_micro_benchmarks"]["solvers"]
        if item["solver_name"] == "optiland"
    )
    assert optiland["approval_status"] == "approved_executed"
    assert optiland["last_execution_status"] == "passed"
    assert optiland["last_execution_evidence"] == (
        "validation/optiland/optiland_micro_benchmark_2026-05-20.md"
    )
    assert optiland["review_record_path"].endswith(
        "optiland_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        optiland["review_status"]
        == "accepted_as_optional_manual_ray_path_smoke_evidence"
    )
    meep = next(
        item
        for item in body["optional_solver_micro_benchmarks"]["solvers"]
        if item["solver_name"] == "meep"
    )
    assert meep["approval_status"] == "approved_executed"
    assert meep["execution_authorized"] is False
    assert meep["last_execution_status"] == "passed"
    assert meep["last_execution_evidence"] == (
        "validation/meep/meep_micro_benchmark_2026-05-20.md"
    )
    assert meep["decision_packet_path"].endswith(
        "meep_micro_benchmark_decision_packet.md"
    )
    assert meep["review_record_path"].endswith(
        "meep_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        meep["review_status"]
        == "accepted_as_optional_manual_pymeep_fdtd_smoke_evidence"
    )
    mpb = next(
        item
        for item in body["optional_solver_micro_benchmarks"]["solvers"]
        if item["solver_name"] == "mpb"
    )
    assert mpb["decision_packet_path"].endswith("mpb_micro_benchmark_decision_packet.md")
    assert mpb["approval_status"] == "pending"
    assert mpb["last_execution_status"] == "not_run"
    assert body["optional_solver_micro_benchmarks"]["elmer_deferred"] is True
    assert "PyPI publication would not imply" in body["preview_boundary_summary"]["pypi"]
    assert all(
        case["metadata_match"] and case["fragment_match"] and case["safety_match"]
        for case in body["adapter_native_golden_coverage"]["cases"]
    )
    assert all(
        item["executed"] is False
        for item in body["blocked_or_deferred_capabilities"]
    )
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    assert body["production_grade_validation_claimed"] is False
    assert body["formal_convergence_proof_claimed"] is False
