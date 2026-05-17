"""Optical calculator API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_optical_calculator_api_endpoints_return_safe_preview_results():
    client = TestClient(app)
    cases = [
        (
            "/api/optics/thin-film",
            {"incident_n": 1.0, "substrate_n": 1.5, "wavelength_nm": 550.0, "layers": [{"n": 1.22, "thickness_nm": 112.7}]},
        ),
        ("/api/optics/paraxial-lens", {"focal_length_mm": 50.0, "object_distance_mm": 200.0}),
        ("/api/optics/gaussian-beam", {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_mm": 5.0}),
        (
            "/api/optics/waveguide-estimate",
            {"core_n": 3.48, "cladding_n": 1.44, "core_thickness_um": 0.22, "wavelength_nm": 1550.0},
        ),
    ]
    for endpoint, payload in cases:
        response = client.post(endpoint, json=payload)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert body["status"] == "ok"
        assert body["result"]
        assert body["assumptions"]
        assert body["external_solver_executed"] is False
        assert body["external_llm_required"] is False
        assert body["production_grade_validation_claimed"] is False
        assert body["formal_convergence_proof_claimed"] is False

