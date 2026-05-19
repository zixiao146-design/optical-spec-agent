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
        (
            "/api/optics/thin-film-spectrum",
            {
                "incident_n": 1.0,
                "substrate_n": 1.5,
                "wavelength_start_nm": 450.0,
                "wavelength_stop_nm": 700.0,
                "points": 6,
                "layers": [{"n": 1.38, "thickness_nm": 100.0}],
            },
        ),
        ("/api/optics/quarter-wave-ar", {"incident_n": 1.0, "substrate_n": 1.5, "target_wavelength_nm": 550.0}),
        ("/api/optics/paraxial-lens", {"focal_length_mm": 50.0, "object_distance_mm": 200.0}),
        (
            "/api/optics/paraxial-system",
            {"elements": [{"type": "free_space", "distance_mm": 25.0}, {"type": "thin_lens", "focal_length_mm": 50.0}]},
        ),
        (
            "/api/optics/two-lens-relay",
            {"f1_mm": 50.0, "f2_mm": 100.0, "separation_mm": 150.0, "object_distance_mm": 100.0},
        ),
        ("/api/optics/gaussian-beam", {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_mm": 5.0}),
        (
            "/api/optics/gaussian-beam-series",
            {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_start_mm": 0.0, "z_stop_mm": 10.0, "points": 5},
        ),
        (
            "/api/optics/gaussian-beam-focus",
            {"wavelength_nm": 1064.0, "input_waist_um": 1000.0, "focal_length_mm": 50.0},
        ),
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
        (
            "/api/optics/waveguide-estimate",
            {"core_n": 3.48, "cladding_n": 1.44, "core_thickness_um": 0.22, "wavelength_nm": 1550.0},
        ),
        (
            "/api/optics/waveguide-sweep",
            {
                "core_n": 2.0,
                "cladding_n": 1.44,
                "wavelength_nm": 1550.0,
                "thickness_start_um": 0.1,
                "thickness_stop_um": 0.6,
                "points": 6,
            },
        ),
        ("/api/optics/waveguide-single-mode-range", {"core_n": 2.0, "cladding_n": 1.44, "wavelength_nm": 1550.0}),
    ]
    for endpoint, payload in cases:
        response = client.post(endpoint, json=payload)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert body["status"] == "ok"
        assert body["result"]
        assert body["assumptions"]
        assert "warnings" in body
        assert body["quality"]["quality_level"] == "sanity_checked_preview"
        assert body["quality"]["production_grade_validation_claimed"] is False
        assert body["quality"]["formal_convergence_proof_claimed"] is False
        assert body["external_solver_executed"] is False
        assert body["external_llm_required"] is False
        assert body["production_grade_validation_claimed"] is False
        assert body["formal_convergence_proof_claimed"] is False
