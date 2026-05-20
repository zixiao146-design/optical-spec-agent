"""Local Agent API frontend fixture tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_EXAMPLES = ROOT / "examples" / "api"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _assert_no_claim_expansion(payload: dict) -> None:
    assert payload["api_contract_version"] == "0.1"
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["proprietary_solver_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False


def test_api_examples_readme_and_manifest_exist():
    assert (API_EXAMPLES / "README.md").exists()
    manifest_path = API_EXAMPLES / "frontend_fixture_manifest.json"
    assert manifest_path.exists()
    manifest = _load_json(manifest_path)
    assert manifest["current_public_prerelease"] == "v0.9.0rc7"
    assert manifest["current_main_development_version"] == "0.9.0rc8"
    assert manifest["api_contract_version"] == "0.1"
    assert manifest["frontend_implementation"] == "mvp implemented under frontend/"
    assert "not live validation" in manifest["demo_mode"]


def test_api_frontend_fixture_manifest_points_to_existing_files_and_safe_defaults():
    manifest = _load_json(API_EXAMPLES / "frontend_fixture_manifest.json")
    for entry in manifest["fixtures"]:
        if entry["request_file"] is not None:
            assert (API_EXAMPLES / entry["request_file"]).exists()
        response_path = API_EXAMPLES / entry["response_file"]
        assert response_path.exists()
        assert entry["no_network"] is True
        assert entry["external_solver_executed"] is False
        assert entry["external_llm_required"] is False
        assert entry["proprietary_solver_required"] is False
        assert entry["production_grade_validation_claimed"] is False
        assert entry["formal_convergence_proof_claimed"] is False
        _assert_no_claim_expansion(_load_json(response_path))
    response_files = {entry["response_file"] for entry in manifest["fixtures"]}
    request_files = {
        entry["request_file"]
        for entry in manifest["fixtures"]
        if entry["request_file"] is not None
    }
    assert "schema_response.json" in response_files
    assert "parse_response_heuristic.json" in response_files
    assert "materials_response.json" in response_files
    assert "material_detail_sio2_response.json" in response_files
    assert "material_suggestion_response.json" in response_files
    assert "material_diagnose_ag_plasmonics_response.json" in response_files
    assert "agent_trace_response_nanoparticle.json" in response_files
    assert "examples_response.json" in response_files
    assert "example_detail_nanoparticle_response.json" in response_files
    assert "example_agent_trace_nanoparticle_response.json" in response_files
    assert "agent_session_response_nanoparticle.json" in response_files
    assert "agent_session_tool_ledger_response.json" in response_files
    assert "agent_session_error_empty_goal_response.json" in response_files
    assert "tool_capabilities_response.json" in response_files
    assert "backend_capability_report_response.json" in response_files
    assert "backend_capability_report_with_golden_coverage_response.json" in response_files
    assert "backend_evidence_summary_response.json" in response_files
    assert "backend_validation_maturity_response.json" in response_files
    assert "design_case_cross_checks_response.json" in response_files
    assert "adapter_native_golden_coverage_response.json" in response_files
    assert "design_requirements_response.json" in response_files
    assert "design_requirement_thin_film_response.json" in response_files
    assert "design_requirement_match_thin_film_response.json" in response_files
    assert "design_requirement_match_nanoparticle_zh_response.json" in response_files
    assert "design_requirement_match_ambiguous_response.json" in response_files
    assert "design_requirement_match_unknown_response.json" in response_files
    assert "optical_language_infer_nanoparticle_response.json" in response_files
    assert "optical_language_diagnose_nanoparticle_response.json" in response_files
    assert "observable_diagnostics_nanoparticle_response.json" in response_files
    assert "adapter_mapping_meep_nanoparticle_response.json" in response_files
    assert "adapter_mapping_gmsh_mesh_response.json" in response_files
    assert "adapter_mapping_mpb_photonic_crystal_response.json" in response_files
    assert "adapter_native_golden_meep_response.json" in response_files
    assert "adapter_native_golden_mpb_response.json" in response_files
    assert "adapter_native_golden_gmsh_response.json" in response_files
    assert "adapter_native_golden_elmer_response.json" in response_files
    assert "adapter_native_golden_optiland_response.json" in response_files
    assert "adapter_preview_meep_source_monitor_response.json" in response_files
    assert "agent_session_adapter_mapping_nanoparticle_response.json" in response_files
    assert "agent_session_source_monitor_nanoparticle_response.json" in response_files
    assert "agent_session_ambiguous_goal_response.json" in response_files
    assert "application_domains_response.json" in response_files
    assert "application_domain_nanoparticle_response.json" in response_files
    assert "application_domain_match_waveguide_response.json" in response_files
    assert "application_domain_cross_check_thin_film_response.json" in response_files
    assert "application_domain_cross_checks_response.json" in response_files
    assert "application_domain_benchmarks_response.json" in response_files
    assert "application_domain_benchmark_nanoparticle_response.json" in response_files
    assert "application_domain_benchmark_eval_nanoparticle_response.json" in response_files
    assert "application_domain_benchmark_eval_ambiguous_response.json" in response_files
    assert "application_domain_benchmark_results_response.json" in response_files
    assert "agent_session_domain_nanoparticle_response.json" in response_files
    assert "thin_film_response.json" in response_files
    assert "thin_film_spectrum_response.json" in response_files
    assert "quarter_wave_ar_response.json" in response_files
    assert "paraxial_lens_response.json" in response_files
    assert "paraxial_system_response.json" in response_files
    assert "two_lens_relay_response.json" in response_files
    assert "gaussian_beam_response.json" in response_files
    assert "gaussian_beam_series_response.json" in response_files
    assert "gaussian_beam_focus_response.json" in response_files
    assert "waveguide_estimate_response.json" in response_files
    assert "waveguide_sweep_response.json" in response_files
    assert "waveguide_single_mode_range_response.json" in response_files
    assert "fiber_coupling_response.json" in response_files
    assert "fiber_coupling_perfect_match_response.json" in response_files
    assert "fiber_coupling_offset_response.json" in response_files
    assert "polarization_jones_response.json" in response_files
    assert "polarization_linear_polarizer_response.json" in response_files
    assert "polarization_waveplate_response.json" in response_files
    assert "agent_session_fiber_coupling_response.json" in response_files
    assert "agent_session_polarization_response.json" in response_files
    assert "parse_request_heuristic.json" in request_files
    assert "material_suggestion_request.json" in request_files
    assert "material_diagnose_ag_plasmonics_request.json" in request_files
    assert "agent_trace_request_nanoparticle.json" in request_files
    assert "agent_session_request_nanoparticle.json" in request_files
    assert "design_requirement_match_thin_film_request.json" in request_files
    assert "design_requirement_match_nanoparticle_zh_request.json" in request_files
    assert "design_requirement_match_ambiguous_request.json" in request_files
    assert "design_requirement_match_unknown_request.json" in request_files
    assert "agent_session_ambiguous_goal_request.json" in request_files
    assert "application_domain_match_waveguide_request.json" in request_files
    assert "agent_session_domain_nanoparticle_request.json" in request_files
    assert "optical_language_infer_nanoparticle_request.json" in request_files
    assert "optical_language_diagnose_nanoparticle_request.json" in request_files
    assert "observable_diagnostics_nanoparticle_request.json" in request_files
    assert "adapter_mapping_meep_nanoparticle_request.json" in request_files
    assert "adapter_mapping_gmsh_mesh_request.json" in request_files
    assert "adapter_mapping_mpb_photonic_crystal_request.json" in request_files
    assert "adapter_native_golden_meep_request.json" in request_files
    assert "adapter_native_golden_mpb_request.json" in request_files
    assert "adapter_native_golden_gmsh_request.json" in request_files
    assert "adapter_native_golden_elmer_request.json" in request_files
    assert "adapter_native_golden_optiland_request.json" in request_files
    assert "adapter_preview_meep_request.json" in request_files
    assert "thin_film_request.json" in request_files
    assert "thin_film_spectrum_request.json" in request_files
    assert "quarter_wave_ar_request.json" in request_files
    assert "paraxial_lens_request.json" in request_files
    assert "paraxial_system_request.json" in request_files
    assert "two_lens_relay_request.json" in request_files
    assert "gaussian_beam_request.json" in request_files
    assert "gaussian_beam_series_request.json" in request_files
    assert "gaussian_beam_focus_request.json" in request_files
    assert "waveguide_estimate_request.json" in request_files
    assert "waveguide_sweep_request.json" in request_files
    assert "waveguide_single_mode_range_request.json" in request_files
    assert "fiber_coupling_request.json" in request_files
    assert "fiber_coupling_perfect_match_request.json" in request_files
    assert "fiber_coupling_offset_request.json" in request_files
    assert "polarization_jones_request.json" in request_files
    assert "polarization_linear_polarizer_request.json" in request_files
    assert "polarization_waveplate_request.json" in request_files
    assert "agent_session_fiber_coupling_request.json" in request_files
    assert "agent_session_polarization_request.json" in request_files
    for calculator_response in [
        "thin_film_response.json",
        "thin_film_spectrum_response.json",
        "quarter_wave_ar_response.json",
        "paraxial_lens_response.json",
        "paraxial_system_response.json",
        "two_lens_relay_response.json",
        "gaussian_beam_response.json",
        "gaussian_beam_series_response.json",
        "gaussian_beam_focus_response.json",
        "waveguide_estimate_response.json",
        "waveguide_sweep_response.json",
        "waveguide_single_mode_range_response.json",
        "fiber_coupling_response.json",
        "fiber_coupling_perfect_match_response.json",
        "fiber_coupling_offset_response.json",
        "polarization_jones_response.json",
        "polarization_linear_polarizer_response.json",
        "polarization_waveplate_response.json",
        "backend_capability_report_response.json",
        "backend_evidence_summary_response.json",
        "design_case_cross_checks_response.json",
        "design_requirements_response.json",
        "design_requirement_thin_film_response.json",
        "design_requirement_match_thin_film_response.json",
        "design_requirement_match_nanoparticle_zh_response.json",
        "design_requirement_match_ambiguous_response.json",
        "design_requirement_match_unknown_response.json",
        "material_diagnose_ag_plasmonics_response.json",
        "optical_language_infer_nanoparticle_response.json",
        "optical_language_diagnose_nanoparticle_response.json",
        "observable_diagnostics_nanoparticle_response.json",
        "adapter_mapping_meep_nanoparticle_response.json",
        "adapter_mapping_gmsh_mesh_response.json",
        "adapter_mapping_mpb_photonic_crystal_response.json",
        "adapter_native_golden_meep_response.json",
        "adapter_native_golden_mpb_response.json",
        "adapter_native_golden_gmsh_response.json",
        "adapter_native_golden_elmer_response.json",
        "adapter_native_golden_optiland_response.json",
        "adapter_native_golden_coverage_response.json",
        "backend_capability_report_with_golden_coverage_response.json",
        "adapter_preview_meep_source_monitor_response.json",
        "agent_session_adapter_mapping_nanoparticle_response.json",
        "agent_session_source_monitor_nanoparticle_response.json",
        "agent_session_ambiguous_goal_response.json",
        "application_domains_response.json",
        "application_domain_nanoparticle_response.json",
        "application_domain_match_waveguide_response.json",
        "application_domain_cross_check_thin_film_response.json",
        "application_domain_cross_checks_response.json",
        "application_domain_benchmarks_response.json",
        "application_domain_benchmark_nanoparticle_response.json",
        "application_domain_benchmark_eval_nanoparticle_response.json",
        "application_domain_benchmark_eval_ambiguous_response.json",
        "application_domain_benchmark_results_response.json",
        "agent_session_domain_nanoparticle_response.json",
        "agent_session_fiber_coupling_response.json",
        "agent_session_polarization_response.json",
    ]:
        payload = _load_json(API_EXAMPLES / calculator_response)
        if "quality" in payload:
            assert payload["quality"]["quality_level"] == "sanity_checked_preview"
            assert "warnings" in payload
            assert payload["quality"]["production_grade_validation_claimed"] is False
            assert payload["quality"]["formal_convergence_proof_claimed"] is False


def test_api_version_and_readiness_fixtures_track_publication_state():
    version = _load_json(API_EXAMPLES / "version_response.json")
    assert version["package_version"] == "0.9.0rc8"
    assert version["current_public_prerelease"] == "v0.9.0rc7"
    assert version["pypi_published"] is False
    _assert_no_claim_expansion(version)

    readiness = _load_json(API_EXAMPLES / "readiness_response.json")
    assert readiness["main_development_version"] == "0.9.0rc8"
    assert readiness["testpypi"]["uploaded_and_verified"] is True
    assert readiness["pypi"]["published"] is False
    assert readiness["v1_0_0_released"] is False
    _assert_no_claim_expansion(readiness)


def test_api_error_fixtures_are_manifested_and_keep_safe_error_shape():
    manifest = _load_json(API_EXAMPLES / "frontend_fixture_manifest.json")
    error_files = {
        "error_invalid_spec_response.json": "invalid_spec",
        "error_unsupported_adapter_response.json": "unsupported_adapter",
        "error_invalid_workflow_request_response.json": "invalid_workflow_request",
        "error_external_llm_not_enabled_response.json": "external_llm_not_enabled",
        "agent_session_error_empty_goal_response.json": "invalid_workflow_request",
    }
    manifested = {entry["response_file"] for entry in manifest["fixtures"]}
    assert set(error_files).issubset(manifested)
    for filename, error_code in error_files.items():
        payload = _load_json(API_EXAMPLES / filename)
        _assert_no_claim_expansion(payload)
        assert payload["status"] == "error"
        assert payload["error_code"] == error_code
        assert payload["message"]
        assert isinstance(payload["diagnostics"], dict)
        assert isinstance(payload["recommended_next_actions"], list)
