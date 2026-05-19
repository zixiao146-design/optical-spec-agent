"""API tests for fiber-coupling and polarization preview calculators."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_fiber_coupling_and_polarization_api_are_safe_preview_endpoints():
    client = TestClient(app)
    cases = [
        (
            "/api/optics/fiber-coupling",
            {
                "waist_input_um": 5.2,
                "waist_fiber_um": 5.2,
                "lateral_offset_um": 0.5,
                "angular_tilt_mrad": 0.2,
                "wavelength_nm": 1550.0,
            },
        ),
        (
            "/api/optics/polarization-jones",
            {
                "input_angle_deg": 0.0,
                "element_type": "waveplate",
                "retardance_rad": 3.141592653589793,
                "fast_axis_deg": 45.0,
            },
        ),
    ]
    for endpoint, payload in cases:
        response = client.post(endpoint, json=payload)
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["status"] == "ok"
        assert body["result"]
        assert body["assumptions"]
        assert body["quality"]["quality_level"] == "sanity_checked_preview"
        assert body["external_solver_executed"] is False
        assert body["external_llm_required"] is False
        assert body["production_grade_validation_claimed"] is False
        assert body["formal_convergence_proof_claimed"] is False
