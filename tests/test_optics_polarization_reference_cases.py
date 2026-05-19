"""Reference sanity cases for Jones-calculus polarization previews."""

from __future__ import annotations

import math

import pytest

from optical_spec_agent.optics.polarization import (
    jones_linear_polarizer,
    jones_waveplate,
    linear_polarization,
)


def _component(vector: list[dict[str, float]], index: int) -> complex:
    item = vector[index]
    return complex(item["real"], item["imag"])


def test_linear_polarization_zero_and_ninety_degree_reference_cases():
    horizontal = linear_polarization(0.0)
    vertical = linear_polarization(90.0)
    assert horizontal.quality.reference_case == "jones_linear_0deg"
    assert vertical.quality.reference_case == "jones_linear_90deg"
    assert _component(horizontal.result["output_jones"], 0) == pytest.approx(1.0 + 0j)
    assert abs(_component(horizontal.result["output_jones"], 1)) < 1e-12
    assert abs(_component(vertical.result["output_jones"], 0)) < 1e-12
    assert _component(vertical.result["output_jones"], 1) == pytest.approx(1.0 + 0j)
    assert horizontal.quality.production_grade_validation_claimed is False
    assert vertical.quality.formal_convergence_proof_claimed is False


def test_linear_polarizer_matches_malus_reference_case():
    input_state = linear_polarization(45.0)
    output = jones_linear_polarizer(input_state.result["output_jones"], 0.0)
    assert output.quality.reference_case == "jones_linear_polarizer_malus"
    assert output.result["input_intensity"] == pytest.approx(1.0)
    assert output.result["intensity"] == pytest.approx(0.5)
    assert 0.0 <= output.result["intensity"] <= 1.0
    assert output.quality.valid_input_range


def test_half_and_quarter_waveplate_reference_cases():
    horizontal = linear_polarization(0.0)
    half_wave = jones_waveplate(horizontal.result["output_jones"], math.pi, 45.0)
    assert half_wave.quality.reference_case == "jones_half_waveplate_preview"
    assert half_wave.result["intensity"] == pytest.approx(1.0)
    assert abs(_component(half_wave.result["normalized_state"], 1)) > 0.999

    diagonal = linear_polarization(45.0)
    quarter_wave = jones_waveplate(diagonal.result["output_jones"], math.pi / 2.0, 0.0)
    assert quarter_wave.quality.reference_case == "jones_quarter_waveplate_phase_preview"
    assert quarter_wave.result["intensity"] == pytest.approx(1.0)
    assert quarter_wave.result["relative_phase_rad"] == pytest.approx(math.pi / 2.0)
    assert abs(_component(quarter_wave.result["normalized_state"], 0)) == pytest.approx(
        1 / math.sqrt(2)
    )
    assert abs(_component(quarter_wave.result["normalized_state"], 1)) == pytest.approx(
        1 / math.sqrt(2)
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda: linear_polarization(float("nan")),
        lambda: jones_linear_polarizer([1.0], 0.0),
        lambda: jones_linear_polarizer([0.0, 0.0], 0.0),
        lambda: jones_linear_polarizer([1.0, 0.0], float("inf")),
        lambda: jones_waveplate([1.0, 0.0], float("nan"), 0.0),
        lambda: jones_waveplate([1.0, 0.0], math.pi, float("nan")),
    ],
)
def test_invalid_polarization_inputs_raise_stable_value_error(call):
    with pytest.raises(ValueError):
        call()
