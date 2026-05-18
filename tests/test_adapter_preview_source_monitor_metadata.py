"""Adapter preview source/monitor metadata tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_adapter_preview_includes_source_monitor_observable_and_mapping_metadata():
    client = TestClient(app)
    response = client.post(
        "/api/adapter-preview",
        json={"path": "examples/specs/minimal_nanoparticle.json", "tool": "meep"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    assert body["source_model"]["source_type"] in {"plane_wave", "unknown"}
    assert body["monitor_model"]["monitor_type"] in {
        "scattering_spectrum",
        "unknown",
    }
    assert body["observable_diagnostics"]
    assert body["adapter_source_monitor_mapping"]["adapter_name"] == "meep"
    assert body["adapter_source_monitor_mapping"]["external_solver_executed"] is False
    assert body["preview_only"] is True
    assert "adapter_source_monitor_mapping" in body["artifact_summary"]
    assert "No real solver monitor result was produced." in body["diagnostics"]["limitations"]
