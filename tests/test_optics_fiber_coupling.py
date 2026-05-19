"""Fiber-coupling preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.fiber_coupling import (
    gaussian_mode_overlap,
    suggest_fiber_coupling_inputs,
)


def test_gaussian_mode_overlap_is_bounded_and_perfect_match_near_one():
    result = gaussian_mode_overlap(waist_input_um=5.2, waist_fiber_um=5.2)
    efficiency = result.result["coupling_efficiency_estimate"]
    assert 0.0 <= efficiency <= 1.0
    assert efficiency == 1.0
    assert result.result["mode_mismatch_factor"] == 1.0
    assert result.quality.quality_level == "sanity_checked_preview"
    assert result.quality.production_grade_validation_claimed is False
    assert result.quality.formal_convergence_proof_claimed is False


def test_gaussian_mode_overlap_offset_and_tilt_lower_efficiency():
    perfect = gaussian_mode_overlap(waist_input_um=5.2, waist_fiber_um=5.2)
    offset = gaussian_mode_overlap(
        waist_input_um=5.2,
        waist_fiber_um=5.2,
        lateral_offset_um=2.0,
    )
    tilted = gaussian_mode_overlap(
        waist_input_um=5.2,
        waist_fiber_um=5.2,
        angular_tilt_mrad=10.0,
    )
    assert offset.result["coupling_efficiency_estimate"] < perfect.result["coupling_efficiency_estimate"]
    assert tilted.result["coupling_efficiency_estimate"] < perfect.result["coupling_efficiency_estimate"]
    assert offset.result["offset_factor"] < 1.0
    assert tilted.result["tilt_factor"] < 1.0


def test_fiber_coupling_inputs_and_diagnostics_are_present():
    inputs = suggest_fiber_coupling_inputs()
    assert "wavelength_nm" in inputs["required_inputs"]
    assert "fiber_mode_field_diameter_or_waist_um" in inputs["required_inputs"]
    result = gaussian_mode_overlap(waist_input_um=4.0, waist_fiber_um=5.0)
    assert result.assumptions
    assert result.diagnostics
    assert result.warnings
    assert "Not production-grade physical validation." in result.quality.limitations
