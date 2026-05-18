"""Reference sanity cases for thin-film preview calculators."""

from __future__ import annotations

import pytest

from optical_spec_agent.optics.thin_film import (
    calculate_thin_film_stack,
    design_quarter_wave_ar_coating,
)


def test_single_interface_air_to_glass_matches_fresnel_reference():
    response = calculate_thin_film_stack(
        [],
        550.0,
        incident_n=1.0,
        substrate_n=1.5,
    )
    expected_reflectance = ((1.0 - 1.5) / (1.0 + 1.5)) ** 2
    assert response.result["reflectance"] == pytest.approx(expected_reflectance, abs=1e-12)
    assert response.result["transmittance"] == pytest.approx(1.0 - expected_reflectance, abs=1e-12)
    assert response.result["absorptance_estimate"] == pytest.approx(0.0, abs=1e-12)
    assert response.quality.reference_case == "single_interface_air_glass_normal_incidence"
    assert response.quality.quality_level == "sanity_checked_preview"


def test_quarter_wave_ar_has_low_target_reflectance_for_ideal_index():
    response = design_quarter_wave_ar_coating(
        incident_n=1.0,
        substrate_n=1.5,
        target_wavelength_nm=550.0,
    )
    assert response.result["selected_coating_n"] == pytest.approx(1.5**0.5)
    assert response.result["quarter_wave_thickness_nm"] == pytest.approx(
        550.0 / (4.0 * (1.5**0.5))
    )
    assert response.result["estimated_target_reflectance"] < 1e-6
    assert response.quality.reference_case == "quarter_wave_ar_normal_incidence"


def test_lossless_thin_film_energy_is_bounded_near_unity():
    response = calculate_thin_film_stack(
        [{"n": 1.38, "thickness_nm": 100.0}],
        550.0,
        incident_n=1.0,
        substrate_n=1.5,
    )
    total = response.result["reflectance"] + response.result["transmittance"]
    assert total == pytest.approx(1.0, abs=1e-9)
    assert response.result["absorptance_estimate"] == pytest.approx(0.0, abs=1e-9)
