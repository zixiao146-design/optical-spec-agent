"""Tests for post-hoc physical diagnostics report generation."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from optical_spec_agent.analysis import (
    CORE_HERO_TASK,
    analyze_flux_artifacts,
    generate_physical_diagnostics,
)
from optical_spec_agent.analysis.mesh_sanity import analyze_mesh_resolution
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json


def test_generate_physical_diagnostics_writes_reports(tmp_path):
    spec = SpecService().process(CORE_HERO_TASK, task_id="diagnostic-test")
    spec_path = tmp_path / "my_spec.json"
    spec_path.write_text(spec_to_json(spec), encoding="utf-8")

    artifact_dir = tmp_path / "run"
    artifact_dir.mkdir()
    (artifact_dir / "scattering_spectrum.csv").write_text(
        "wavelength_nm,particle_induced_flux_relative\n400,0.0\n500,1.0\n600,0.2\n",
        encoding="utf-8",
    )
    (artifact_dir / "flux_surfaces.csv").write_text(
        "wavelength_nm,flux_x_minus,flux_x_plus,flux_total\n400,0.1,0.2,0.3\n"
        "500,0.4,0.5,0.9\n",
        encoding="utf-8",
    )
    (artifact_dir / "execution_result.json").write_text(
        json.dumps(
            {
                "success": False,
                "available": True,
                "returncode": 1,
                "run_id": "run-1",
                "outputs": {},
                "errors": ["RuntimeError: fields are NaN"],
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    result = generate_physical_diagnostics(
        spec_path=spec_path,
        output_dir=tmp_path / "outputs",
        artifact_dir=artifact_dir,
        resolution_px_per_um=12,
    )

    assert (tmp_path / "outputs" / "mesh_report.csv").exists()
    assert (tmp_path / "outputs" / "flux_report.csv").exists()
    assert (tmp_path / "outputs" / "execution_diagnostics.json").exists()
    assert (tmp_path / "outputs" / "diagnostic_preview.png").read_bytes().startswith(b"\x89PNG")
    assert result.mesh_diagnostics is not None
    assert result.execution_diagnostics["nan_or_inf_detected"] is True


def test_flux_artifacts_flag_nan_inf_values(tmp_path):
    flux_path = tmp_path / "flux_surfaces.csv"
    flux_path.write_text(
        "wavelength_nm,flux_x_minus,flux_total\n400,nan,1.0\n500,2.0,inf\n",
        encoding="utf-8",
    )

    summaries = analyze_flux_artifacts(flux_surfaces_path=flux_path, spectrum_path=None)

    assert any(summary.anomaly for summary in summaries)
    assert any("NaN/Inf" in note for summary in summaries for note in summary.notes)


def test_mesh_sanity_rejects_invalid_boundary_values():
    with pytest.raises(ValueError, match="resolution_px_per_um must be positive"):
        analyze_mesh_resolution(
            resolution_px_per_um=0,
            gap_thickness_nm=5,
            particle_radius_nm=40,
            film_thickness_nm=100,
        )


def test_generate_physical_diagnostics_help_succeeds():
    result = subprocess.run(
        [sys.executable, "scripts/generate_physical_diagnostics.py", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0
    assert "mesh_report.csv" in result.stdout
