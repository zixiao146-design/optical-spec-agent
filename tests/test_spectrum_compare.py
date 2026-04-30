"""Tests for local/manual spectrum comparison utilities."""

from __future__ import annotations

import pytest

from optical_spec_agent.analysis import analyze_flux_signal, compare_spectra, load_scattering_csv


def _write_csv(path, rows):
    lines = ["wavelength_nm,particle_induced_flux_relative"]
    lines.extend(f"{wavelength},{flux}" for wavelength, flux in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_load_scattering_csv_reads_valid_csv(tmp_path):
    csv_path = tmp_path / "scattering_spectrum.csv"
    _write_csv(csv_path, [(400, 1.0), (500, 2.0)])

    data = load_scattering_csv(csv_path)
    assert data.wavelength_nm == [400.0, 500.0]
    assert data.flux == [1.0, 2.0]


def test_load_scattering_csv_rejects_nan_inf(tmp_path):
    nan_path = tmp_path / "nan.csv"
    _write_csv(nan_path, [(400, "nan")])
    with pytest.raises(ValueError, match="NaN"):
        load_scattering_csv(nan_path)

    inf_path = tmp_path / "inf.csv"
    _write_csv(inf_path, [(400, "inf")])
    with pytest.raises(ValueError, match="Inf"):
        load_scattering_csv(inf_path)


def test_compare_spectra_identical_is_near_zero(tmp_path):
    csv_path = tmp_path / "baseline.csv"
    _write_csv(csv_path, [(400, 0.0), (500, 1.0), (600, 0.0)])
    baseline = load_scattering_csv(csv_path)
    candidate = load_scattering_csv(csv_path)

    comparison = compare_spectra(baseline, candidate)
    assert comparison.peak_shift_nm == 0.0
    assert comparison.normalized_l2_difference == pytest.approx(0.0)
    assert comparison.normalized_max_difference == pytest.approx(0.0)
    assert comparison.integrated_flux_relative_difference == pytest.approx(0.0)


def test_compare_spectra_shifted_peak_has_nonzero_peak_shift(tmp_path):
    baseline_path = tmp_path / "baseline.csv"
    candidate_path = tmp_path / "candidate.csv"
    _write_csv(baseline_path, [(400, 0.0), (500, 1.0), (600, 0.0)])
    _write_csv(candidate_path, [(400, 0.0), (500, 0.0), (600, 1.0)])

    comparison = compare_spectra(
        load_scattering_csv(baseline_path),
        load_scattering_csv(candidate_path),
    )
    assert comparison.peak_shift_nm == 100.0
    assert comparison.normalized_l2_difference > 0


def test_analyze_flux_signal_detects_near_zero_signal(tmp_path):
    csv_path = tmp_path / "near_zero.csv"
    _write_csv(csv_path, [(400, 1e-24), (500, -1e-24), (600, 1e-24)])

    metrics = analyze_flux_signal(load_scattering_csv(csv_path))

    assert metrics["near_zero_signal"] is True
    assert metrics["max_abs_flux"] == pytest.approx(1e-24)


def test_analyze_flux_signal_detects_nonzero_signal(tmp_path):
    csv_path = tmp_path / "nonzero.csv"
    _write_csv(csv_path, [(400, 0.0), (500, 1.0), (600, 0.25)])

    metrics = analyze_flux_signal(load_scattering_csv(csv_path))

    assert metrics["near_zero_signal"] is False
    assert metrics["integrated_abs_flux"] > 0
