"""Waveguide preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.waveguide import (
    single_mode_estimate,
    slab_waveguide_v_number,
)


def test_waveguide_v_number_positive_and_deterministic():
    response = slab_waveguide_v_number(
        core_n=3.48,
        cladding_n=1.44,
        core_thickness_um=0.22,
        wavelength_nm=1550.0,
    )
    assert response.result["v_number"] > 0
    assert response.result["single_mode_likely"] == single_mode_estimate(response.result["v_number"])
    assert response.production_grade_validation_claimed is False
    assert response.diagnostics

