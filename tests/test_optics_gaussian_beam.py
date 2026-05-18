"""Gaussian beam preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.gaussian_beam import (
    focus_gaussian_beam_thin_lens,
    gaussian_beam_parameters,
    propagate_gaussian_beam,
    propagate_gaussian_beam_series,
)


def test_gaussian_beam_rayleigh_range_positive():
    response = gaussian_beam_parameters(wavelength_nm=1064.0, waist_um=10.0)
    assert response.result["rayleigh_range_mm"] > 0
    assert response.result["divergence_half_angle_rad"] > 0


def test_gaussian_beam_radius_increases_with_z():
    at_waist = propagate_gaussian_beam(wavelength_nm=1064.0, waist_um=10.0, z_mm=0.0)
    propagated = propagate_gaussian_beam(wavelength_nm=1064.0, waist_um=10.0, z_mm=5.0)
    assert propagated.result["beam_radius_um"] > at_waist.result["beam_radius_um"]
    assert propagated.external_solver_executed is False
    assert propagated.external_llm_required is False


def test_gaussian_beam_series_sample_count():
    response = propagate_gaussian_beam_series(
        wavelength_nm=1064.0,
        waist_um=10.0,
        z_start_mm=0.0,
        z_stop_mm=10.0,
        points=5,
    )
    assert response.result["sample_count"] == 5
    assert len(response.result["samples"]) == 5
    assert response.result["samples"][-1]["beam_radius_um"] > response.result["samples"][0]["beam_radius_um"]


def test_gaussian_beam_focus_output_sane():
    response = focus_gaussian_beam_thin_lens(
        wavelength_nm=1064.0,
        input_waist_um=1000.0,
        focal_length_mm=50.0,
    )
    assert response.result["approx_focused_waist_um"] > 0
    assert response.result["focused_rayleigh_range_mm"] > 0
    assert response.assumptions
