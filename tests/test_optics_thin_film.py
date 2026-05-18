"""Thin-film preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.thin_film import (
    calculate_thin_film_spectrum,
    calculate_thin_film_stack,
    design_quarter_wave_ar_coating,
    summarize_thin_film_result,
)


def test_thin_film_stack_returns_bounded_preview_values():
    response = calculate_thin_film_stack(
        [{"n": 1.22, "k": 0.0, "thickness_nm": 112.7}],
        550.0,
        incident_n=1.0,
        substrate_n=1.5,
    )
    result = response.result
    assert 0 <= result["reflectance"] <= 1
    assert 0 <= result["transmittance"] <= 1
    assert 0 <= result["absorptance_estimate"] <= 1
    assert response.production_grade_validation_claimed is False
    assert response.formal_convergence_proof_claimed is False
    assert response.assumptions
    assert response.limitations


def test_thin_film_spectrum_sample_count_and_summary():
    response = calculate_thin_film_spectrum(
        [{"n": 1.38, "k": 0.0, "thickness_nm": 100.0}],
        450.0,
        700.0,
        6,
        incident_n=1.0,
        substrate_n=1.5,
    )
    assert response.result["sample_count"] == 6
    assert len(response.result["samples"]) == 6
    for sample in response.result["samples"]:
        assert 0 <= sample["reflectance"] <= 1
        assert 0 <= sample["transmittance"] <= 1
        assert 0 <= sample["absorptance_estimate"] <= 1
    summary = summarize_thin_film_result(response)
    assert summary["sample_count"] == 6
    assert "minimum_reflectance" in summary


def test_quarter_wave_ar_returns_coating_preview():
    response = design_quarter_wave_ar_coating(
        substrate_n=1.5,
        target_wavelength_nm=550.0,
    )
    assert response.result["quarter_wave_thickness_nm"] > 0
    assert response.result["coating_layer"]["n"] > 0
    assert 0 <= response.result["estimated_target_reflectance"] <= 1
    assert response.production_grade_validation_claimed is False
    assert summarize_thin_film_result(response)["estimated_target_reflectance"] >= 0
