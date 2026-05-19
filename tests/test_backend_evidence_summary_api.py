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
    assert body["design_case_cross_checks"]
    assert body["source_monitor_observable_diagnostics"]["observable_taxonomy_available"] is True
    assert body["adapter_native_golden_coverage"]["status"] == "ok"
    assert body["application_domain_benchmarks"]["scenario_count"] >= 19
    assert body["application_domain_benchmarks"]["fail_count"] == 0
    assert body["application_domain_benchmarks"]["warn_count"] == 0
    assert body["application_domain_benchmarks"]["unsupported_requests_blocked_or_deferred"] is True
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
