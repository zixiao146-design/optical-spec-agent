"""Backend capability report API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_backend_capability_report_api_returns_expected_sections():
    client = TestClient(app)
    response = client.get("/api/backend-capability-report")
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["evidence_pack_available"] is True
    assert body["maintainer_review_recommended"] is True
    assert "Adapter-native golden coverage" in body["evidence_pack_sections"]
    assert body["package"]["package_version"] == "0.9.0rc8.dev0"
    assert {item["role_name"] for item in body["sub_agents"]} >= {"SpecAgent", "SafetyAgent"}
    assert {item["tool_name"] for item in body["internal_tools"]} >= {
        "material_catalog",
        "material_suitability_diagnostics",
        "example_registry",
        "ambiguous_requirement_matching",
        "application_domain_registry",
        "material_template_cross_checks",
        "application_domain_benchmarks",
        "source_monitor_inference",
        "missing_input_diagnostics",
        "observable_diagnostics",
        "adapter_native_mapping",
        "adapter_native_golden_coverage",
        "validation_maturity_summary",
        "optical_calculators",
    }
    assert {item["calculator_name"] for item in body["optical_calculators"]} == {
        "thin_film",
        "paraxial",
        "gaussian_beam",
        "waveguide",
        "fiber_coupling",
        "polarization",
    }
    calculators = {item["calculator_name"]: item for item in body["optical_calculators"]}
    assert "fiber_gaussian_offset_loss" in calculators["fiber_coupling"]["reference_cases"]
    assert (
        "jones_quarter_waveplate_phase_preview"
        in calculators["polarization"]["reference_cases"]
    )
    assert len(body["requirements_templates"]) == 7
    assert body["material_provenance_coverage"]["material_count"] >= 10
    assert body["material_provenance_coverage"]["production_grade_optical_constants_claimed"] is False
    assert body["ambiguous_requirement_matching"]["available"] is True
    assert body["ambiguous_requirement_matching"]["no_external_llm_used"] is True
    assert body["missing_input_diagnostics"]["safe_to_run_solver_default"] is False
    assert body["application_domain_coverage"]["domain_count"] == 10
    assert body["application_domain_coverage"]["failed_domains"] == []
    assert body["material_template_cross_checks"]["total"] == 10
    assert body["material_template_cross_checks"]["fail_count"] == 0
    assert body["application_domain_benchmarks"]["scenario_count"] >= 19
    assert body["application_domain_benchmarks"]["fail_count"] == 0
    assert body["application_domain_benchmarks"]["warn_count"] == 0
    assert body["validation_maturity_summary"]["summary"]["record_count"] >= 17
    assert (
        body["validation_maturity_summary"]["summary"]["calculator_maturity_level"]
        == "sanity_checked_preview"
    )
    assert body["validation_claim_audit_available"] is True
    assert "materials" in body["preview_boundary_summary"]
    assert body["optional_solver_micro_benchmarks"]["manifest_exists"] is True
    assert body["optional_solver_micro_benchmarks"]["readiness_available"] is True
    assert body["optional_solver_micro_benchmarks"]["approval_matrix_available"] is True
    assert (
        body["optional_solver_micro_benchmarks"]["execution_approval_packet_available"]
        is True
    )
    assert body["optional_solver_micro_benchmarks"]["approval_records_present"] is True
    assert body["optional_solver_micro_benchmarks"]["environment_profiles_available"] is True
    assert (
        body["optional_solver_micro_benchmarks"]["environment_profiles_path"]
        == "validation/solver_environment_profiles.json"
    )
    assert body["optional_solver_micro_benchmarks"]["solver_python_env_var"] == "OSA_SOLVER_PYTHON"
    assert body["optional_solver_micro_benchmarks"]["profile_env_var"] == "OSA_SOLVER_READINESS_PROFILE"
    assert body["optional_solver_micro_benchmarks"]["default_runs_solver"] is False
    assert body["optional_solver_micro_benchmarks"]["execution_default"] is False
    assert body["optional_solver_micro_benchmarks"]["opt_in_required"] is True
    assert body["optional_solver_micro_benchmarks"]["explicit_approval_required"] is True
    assert (
        body["optional_solver_micro_benchmarks"][
            "all_optional_solver_execution_authorized"
        ]
        is False
    )
    assert body["optional_solver_micro_benchmarks"]["elmer_deferred"] is True
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
    assert gmsh["next_candidate_solver"] == "meep_or_mpb_after_osa_solver_python"
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
    assert body["adapter_native_golden_coverage"]["status"] == "ok"
    assert set(body["adapter_native_golden_coverage"]["adapters_covered"]) == {
        "meep",
        "mpb",
        "gmsh",
        "elmer",
        "optiland",
    }
    assert body["adapter_native_golden_coverage"]["missing_adapters"] == []
    assert all(item["matched_by_heuristic"] for item in body["requirements_templates"])
    assert body["design_case_cross_checks"]
    assert all(action["executed"] is False for action in body["blocked_external_actions"])
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False


def test_backend_evidence_summary_api_is_linked_to_capability_report():
    client = TestClient(app)
    report = client.get("/api/backend-capability-report").json()
    response = client.get("/api/backend-evidence-summary")
    assert response.status_code == 200
    body = response.json()
    assert report["evidence_pack_available"] is True
    assert body["evidence_pack_available"] is True
    assert body["adapter_native_golden_coverage"]["status"] == "ok"
    assert body["material_provenance_coverage"]["production_grade_optical_constants_database"] is False
    assert body["ambiguous_requirement_matching"]["ambiguous_goals_generate_questions"] is True
    assert body["application_domain_coverage"]["domain_count"] == 10
    assert body["material_template_cross_checks"]["fail_count"] == 0
    assert body["application_domain_benchmarks"]["fail_count"] == 0
    assert body["application_domain_benchmarks"]["warn_count"] == 0
    assert body["validation_maturity_summary"]["summary"]["record_count"] >= 17
    assert body["validation_claim_audit_available"] is True
    assert body["optional_solver_micro_benchmarks"]["default_runs_solver"] is False
    assert body["optional_solver_micro_benchmarks"]["opt_in_required"] is True
    assert body["optional_solver_micro_benchmarks"]["optional_solver_readiness_available"] is True
    assert body["optional_solver_micro_benchmarks"]["optional_solver_approval_matrix_available"] is True
    assert body["optional_solver_micro_benchmarks"]["optional_solver_environment_profiles_available"] is True
    assert body["optional_solver_micro_benchmarks"]["solver_python_env_var"] == "OSA_SOLVER_PYTHON"
    assert body["optional_solver_micro_benchmarks"]["explicit_approval_required"] is True
    gmsh = next(
        item
        for item in body["optional_solver_micro_benchmarks"]["solvers"]
        if item["solver_name"] == "gmsh"
    )
    assert gmsh["review_record_path"].endswith(
        "gmsh_micro_benchmark_review_2026-05-20.md"
    )
    assert body["external_solver_executed"] is False


def test_design_case_cross_checks_api_returns_safe_results():
    client = TestClient(app)
    response = client.get("/api/design-case-cross-checks")
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["summary"]["total"] == 6
    assert body["summary"]["fail"] == 0
    assert body["summary"]["requirement_templates_total"] == 7
    assert body["summary"]["requirement_templates_fail"] == 0
    assert body["requirement_template_checks"]
    assert all(check["status"] == "pass" for check in body["cross_checks"])
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
