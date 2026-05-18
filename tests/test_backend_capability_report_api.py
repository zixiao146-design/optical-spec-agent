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
    assert body["package"]["package_version"] == "0.9.0rc7.dev0"
    assert {item["role_name"] for item in body["sub_agents"]} >= {"SpecAgent", "SafetyAgent"}
    assert {item["tool_name"] for item in body["internal_tools"]} >= {
        "material_catalog",
        "example_registry",
        "source_monitor_inference",
        "missing_input_diagnostics",
        "observable_diagnostics",
        "adapter_native_mapping",
        "optical_calculators",
    }
    assert {item["calculator_name"] for item in body["optical_calculators"]} == {
        "thin_film",
        "paraxial",
        "gaussian_beam",
        "waveguide",
    }
    assert len(body["requirements_templates"]) == 7
    assert all(item["matched_by_heuristic"] for item in body["requirements_templates"])
    assert body["design_case_cross_checks"]
    assert all(action["executed"] is False for action in body["blocked_external_actions"])
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False


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
