"""Reference sanity cases for waveguide preview calculators."""

from __future__ import annotations

import math

import pytest

from optical_spec_agent.optics.waveguide import slab_waveguide_sweep, slab_waveguide_v_number


def test_slab_waveguide_v_number_matches_formula():
    response = slab_waveguide_v_number(
        core_n=2.0,
        cladding_n=1.5,
        core_thickness_um=0.3,
        wavelength_nm=1550.0,
    )
    expected = (2.0 * math.pi / 1.55) * 0.3 * math.sqrt(2.0**2 - 1.5**2)
    assert response.result["v_number"] == pytest.approx(expected)
    assert response.quality.reference_case == "slab_waveguide_v_number_formula"


def test_waveguide_sweep_is_monotonic_with_thickness():
    response = slab_waveguide_sweep(
        core_n=2.0,
        cladding_n=1.5,
        wavelength_nm=1550.0,
        thickness_start_um=0.1,
        thickness_stop_um=0.5,
        points=5,
    )
    v_numbers = [sample["v_number"] for sample in response.result["samples"]]
    assert v_numbers == sorted(v_numbers)
    assert v_numbers[0] < v_numbers[-1]
