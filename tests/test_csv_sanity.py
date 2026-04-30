"""Tests for lightweight Meep CSV numeric sanity checks."""

from __future__ import annotations

from optical_spec_agent.execution import check_csv_numeric_sanity


def test_check_csv_numeric_sanity_accepts_valid_csv(tmp_path):
    csv_path = tmp_path / "scattering_spectrum.csv"
    csv_path.write_text(
        "wavelength_nm,particle_induced_flux_relative\n"
        "400.0,1.0\n"
        "500.0,-2.5\n",
        encoding="utf-8",
    )

    result = check_csv_numeric_sanity(csv_path)
    assert result.ok is True
    assert result.rows_checked == 2
    assert result.errors == []


def test_check_csv_numeric_sanity_rejects_nan(tmp_path):
    csv_path = tmp_path / "scattering_spectrum.csv"
    csv_path.write_text(
        "wavelength_nm,particle_induced_flux_relative\n"
        "400.0,nan\n",
        encoding="utf-8",
    )

    result = check_csv_numeric_sanity(csv_path)
    assert result.ok is False
    assert any("NaN" in error for error in result.errors)


def test_check_csv_numeric_sanity_rejects_inf(tmp_path):
    csv_path = tmp_path / "scattering_spectrum.csv"
    csv_path.write_text(
        "wavelength_nm,particle_induced_flux_relative\n"
        "400.0,inf\n",
        encoding="utf-8",
    )

    result = check_csv_numeric_sanity(csv_path)
    assert result.ok is False
    assert any("Inf" in error for error in result.errors)
