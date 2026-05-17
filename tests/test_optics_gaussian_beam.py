"""Gaussian beam preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.gaussian_beam import (
    gaussian_beam_parameters,
    propagate_gaussian_beam,
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

