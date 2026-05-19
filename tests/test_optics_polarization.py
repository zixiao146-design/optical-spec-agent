"""Polarization Jones preview calculator tests."""

from __future__ import annotations

import math

from optical_spec_agent.optics.polarization import (
    jones_linear_polarizer,
    jones_waveplate,
    linear_polarization,
    summarize_polarization_state,
)


def test_linear_polarization_jones_vector_sanity():
    horizontal = linear_polarization(0.0)
    assert horizontal.result["output_jones"][0]["real"] == 1.0
    assert horizontal.result["output_jones"][1]["real"] == 0.0
    assert horizontal.result["intensity"] == 1.0
    assert horizontal.quality.production_grade_validation_claimed is False


def test_linear_polarizer_output_intensity_is_bounded():
    state = linear_polarization(0.0)
    crossed = jones_linear_polarizer(state.result["output_jones"], 90.0)
    parallel = jones_linear_polarizer(state.result["output_jones"], 0.0)
    assert 0.0 <= crossed.result["intensity"] <= 1.0
    assert 0.0 <= parallel.result["intensity"] <= 1.0
    assert crossed.result["intensity"] < 1e-24
    assert parallel.result["intensity"] == 1.0


def test_waveplate_changes_state_and_preserves_intensity():
    state = linear_polarization(0.0)
    waveplate = jones_waveplate(state.result["output_jones"], math.pi, 45.0)
    assert waveplate.result["intensity"] == 1.0
    assert abs(waveplate.result["normalized_state"][1]["imag"]) > 0.9
    assert waveplate.assumptions
    assert waveplate.diagnostics
    assert waveplate.quality.quality_level == "sanity_checked_preview"
    assert waveplate.quality.formal_convergence_proof_claimed is False


def test_polarization_state_summary_accepts_complex_pair_format():
    summary = summarize_polarization_state([[1.0, 0.0], [0.0, 1.0]])
    assert summary.result["intensity"] == 2.0
    assert summary.result["relative_phase_rad"] is not None
    assert "Jones-vector state summary only." in summary.assumptions
