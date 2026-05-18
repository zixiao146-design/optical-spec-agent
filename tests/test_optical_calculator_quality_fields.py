"""Quality-field contract tests for optical calculator API responses."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app
from optical_spec_agent.optics.models import CalculatorQuality, CalculatorResult


def test_calculator_quality_defaults_are_conservative():
    quality = CalculatorQuality()
    assert quality.quality_level == "sanity_checked_preview"
    assert quality.production_grade_validation_claimed is False
    assert quality.formal_convergence_proof_claimed is False
    assert "Not production-grade physical validation." in quality.limitations

    result = CalculatorResult(result={"example": True})
    assert result.quality.quality_level == "sanity_checked_preview"
    assert result.production_grade_validation_claimed is False
    assert result.formal_convergence_proof_claimed is False


def test_calculator_api_response_exposes_quality_warnings_and_limitations():
    client = TestClient(app)
    response = client.post(
        "/api/optics/thin-film",
        json={
            "incident_n": 1.0,
            "substrate_n": 1.5,
            "wavelength_nm": 550.0,
            "layers": [],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["quality"]["quality_level"] == "sanity_checked_preview"
    assert body["quality"]["reference_case"] == "single_interface_air_glass_normal_incidence"
    assert body["quality"]["production_grade_validation_claimed"] is False
    assert body["quality"]["formal_convergence_proof_claimed"] is False
    assert "warnings" in body
    assert "limitations" in body
    assert body["assumptions"]
