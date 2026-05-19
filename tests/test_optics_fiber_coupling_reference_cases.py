"""Reference sanity cases for fiber-coupling preview calculators."""

from __future__ import annotations

import math

import pytest

from optical_spec_agent.optics.fiber_coupling import gaussian_mode_overlap


def test_perfect_gaussian_match_reference_case_is_near_one():
    result = gaussian_mode_overlap(
        waist_input_um=5.2,
        waist_fiber_um=5.2,
        lateral_offset_um=0.0,
        angular_tilt_mrad=0.0,
        wavelength_nm=1550.0,
    )
    assert result.quality.reference_case == "fiber_gaussian_perfect_overlap"
    assert result.quality.quality_level == "sanity_checked_preview"
    assert math.isclose(result.result["coupling_efficiency_estimate"], 1.0)
    assert result.result["mode_mismatch_factor"] == 1.0
    assert result.result["offset_factor"] == 1.0
    assert result.result["tilt_factor"] == 1.0
    assert result.quality.production_grade_validation_claimed is False
    assert result.quality.formal_convergence_proof_claimed is False


def test_waist_mismatch_offset_and_tilt_reduce_efficiency():
    perfect = gaussian_mode_overlap(waist_input_um=5.2, waist_fiber_um=5.2)
    mismatch = gaussian_mode_overlap(waist_input_um=4.0, waist_fiber_um=5.2)
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
    perfect_eta = perfect.result["coupling_efficiency_estimate"]
    assert mismatch.quality.reference_case == "fiber_gaussian_waist_mismatch"
    assert offset.quality.reference_case == "fiber_gaussian_offset_loss"
    assert tilted.quality.reference_case == "fiber_gaussian_tilt_loss"
    assert mismatch.result["coupling_efficiency_estimate"] < perfect_eta
    assert offset.result["coupling_efficiency_estimate"] < perfect_eta
    assert tilted.result["coupling_efficiency_estimate"] < perfect_eta
    for item in (perfect, mismatch, offset, tilted):
        assert 0.0 <= item.result["coupling_efficiency_estimate"] <= 1.0
        assert item.assumptions
        assert item.diagnostics
        assert item.warnings
        assert item.quality.valid_input_range


@pytest.mark.parametrize(
    "kwargs",
    [
        {"waist_input_um": -1.0, "waist_fiber_um": 5.2},
        {"waist_input_um": 5.2, "waist_fiber_um": 0.0},
        {"waist_input_um": 5.2, "waist_fiber_um": 5.2, "wavelength_nm": 0.0},
        {"waist_input_um": 5.2, "waist_fiber_um": 5.2, "lateral_offset_um": -0.1},
        {"waist_input_um": float("nan"), "waist_fiber_um": 5.2},
        {"waist_input_um": 5.2, "waist_fiber_um": 5.2, "angular_tilt_mrad": float("inf")},
    ],
)
def test_invalid_fiber_coupling_inputs_raise_stable_value_error(kwargs):
    with pytest.raises(ValueError):
        gaussian_mode_overlap(**kwargs)
