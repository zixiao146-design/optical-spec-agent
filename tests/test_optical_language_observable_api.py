"""API tests for observable diagnostics and adapter-native mapping."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_observable_diagnostics_api_returns_safe_preview_metadata():
    client = TestClient(app)
    response = client.post(
        "/api/optical-language/observables/diagnose",
        json={
            "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
            "template_id": "nanoparticle_plasmonics",
            "language": "zh-CN",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    assert body["production_grade_validation_claimed"] is False
    assert body["formal_convergence_proof_claimed"] is False
    assert body["source_model"]["source_type"] == "plane_wave"
    assert body["monitor_model"]["monitor_type"] == "scattering_spectrum"
    assert {"scattering_spectrum", "extinction_spectrum"}.issubset(
        {item["observable_kind"] for item in body["observable_diagnostics"]}
    )


def test_adapter_mapping_api_returns_adapter_native_preview_metadata():
    client = TestClient(app)
    response = client.post(
        "/api/optical-language/adapter-mapping",
        json={
            "adapter_name": "meep",
            "goal": "silver nanoparticle scattering preview",
            "template_id": "nanoparticle_plasmonics",
            "language": "en",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    mapping = body["adapter_source_monitor_mapping"]
    assert mapping["adapter_name"] == "meep"
    assert mapping["preview_only"] is True
    assert mapping["external_solver_executed"] is False
    assert "scattering_spectrum" in mapping["supported_observables"]


def test_observable_api_errors_are_stable():
    client = TestClient(app)
    empty = client.post(
        "/api/optical-language/observables/diagnose",
        json={"goal": "   "},
    )
    assert empty.status_code == 400
    assert empty.json()["error_code"] == "invalid_workflow_request"

    invalid_language = client.post(
        "/api/optical-language/adapter-mapping",
        json={"adapter_name": "meep", "goal": "nanoparticle", "language": "fr"},
    )
    assert invalid_language.status_code == 400
    assert invalid_language.json()["error_code"] == "invalid_workflow_request"
