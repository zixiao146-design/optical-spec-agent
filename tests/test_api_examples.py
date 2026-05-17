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
    assert manifest["current_public_prerelease"] == "v0.9.0rc6"
    assert manifest["current_main_development_version"] == "0.9.0rc7.dev0"
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
    assert "agent_trace_response_nanoparticle.json" in response_files
    assert "examples_response.json" in response_files
    assert "example_detail_nanoparticle_response.json" in response_files
    assert "example_agent_trace_nanoparticle_response.json" in response_files
    assert "agent_session_response_nanoparticle.json" in response_files
    assert "agent_session_tool_ledger_response.json" in response_files
    assert "agent_session_error_empty_goal_response.json" in response_files
    assert "tool_capabilities_response.json" in response_files
    assert "thin_film_response.json" in response_files
    assert "paraxial_lens_response.json" in response_files
    assert "gaussian_beam_response.json" in response_files
    assert "waveguide_estimate_response.json" in response_files
    assert "parse_request_heuristic.json" in request_files
    assert "material_suggestion_request.json" in request_files
    assert "agent_trace_request_nanoparticle.json" in request_files
    assert "agent_session_request_nanoparticle.json" in request_files
    assert "thin_film_request.json" in request_files
    assert "paraxial_lens_request.json" in request_files
    assert "gaussian_beam_request.json" in request_files
    assert "waveguide_estimate_request.json" in request_files


def test_api_version_and_readiness_fixtures_track_publication_state():
    version = _load_json(API_EXAMPLES / "version_response.json")
    assert version["package_version"] == "0.9.0rc7.dev0"
    assert version["current_public_prerelease"] == "v0.9.0rc6"
    assert version["pypi_published"] is False
    _assert_no_claim_expansion(version)

    readiness = _load_json(API_EXAMPLES / "readiness_response.json")
    assert readiness["main_development_version"] == "0.9.0rc7.dev0"
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
