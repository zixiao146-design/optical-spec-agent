"""Reference sanity cases for Gaussian beam preview calculators."""

from __future__ import annotations

import math

import pytest

from optical_spec_agent.optics.gaussian_beam import (
    gaussian_beam_parameters,
    propagate_gaussian_beam,
)


def test_gaussian_rayleigh_range_matches_formula():
    response = gaussian_beam_parameters(wavelength_nm=1000.0, waist_um=10.0)
    expected_mm = math.pi * 10.0**2 / 1.0 / 1000.0
    assert response.result["rayleigh_range_mm"] == pytest.approx(expected_mm)
    assert response.quality.reference_case == "gaussian_rayleigh_range_formula"


def test_gaussian_radius_at_waist_equals_waist():
    response = propagate_gaussian_beam(wavelength_nm=1000.0, waist_um=10.0, z_mm=0.0)
    assert response.result["beam_radius_um"] == pytest.approx(10.0)
    assert response.quality.reference_case == "gaussian_beam_radius_at_waist"


def test_gaussian_radius_at_rayleigh_range_is_sqrt_two_waist():
    params = gaussian_beam_parameters(wavelength_nm=1000.0, waist_um=10.0)
    z_rayleigh_mm = params.result["rayleigh_range_mm"]
    response = propagate_gaussian_beam(
        wavelength_nm=1000.0,
        waist_um=10.0,
        z_mm=z_rayleigh_mm,
    )
    assert response.result["beam_radius_um"] == pytest.approx(10.0 * math.sqrt(2.0))
    assert response.quality.reference_case == "gaussian_beam_radius_at_rayleigh_range"
