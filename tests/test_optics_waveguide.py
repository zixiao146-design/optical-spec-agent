"""Waveguide preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.waveguide import (
    single_mode_estimate,
    slab_waveguide_sweep,
    slab_waveguide_v_number,
    suggest_single_mode_thickness_range,
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


def test_waveguide_sweep_sample_count():
    response = slab_waveguide_sweep(
        core_n=2.0,
        cladding_n=1.44,
        wavelength_nm=1550.0,
        thickness_start_um=0.1,
        thickness_stop_um=0.6,
        points=6,
    )
    assert response.result["sample_count"] == 6
    assert len(response.result["samples"]) == 6
    assert response.result["samples"][0]["v_number"] < response.result["samples"][-1]["v_number"]


def test_single_mode_thickness_range_deterministic():
    response = suggest_single_mode_thickness_range(
        core_n=2.0,
        cladding_n=1.44,
        wavelength_nm=1550.0,
    )
    assert response.result["suggested_max_thickness_um"] > response.result["suggested_min_thickness_um"]
    assert response.result["cutoff_v_number"] > 3.0
    assert response.diagnostics
