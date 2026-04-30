"""Tests for the manual/local candidate convergence analysis script."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


CONVERGENCE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_meep_candidate_convergence.py"


def _write_csv(case_dir: Path, rows):
    case_dir.mkdir(parents=True, exist_ok=True)
    lines = ["wavelength_nm,particle_induced_flux_relative"]
    lines.extend(f"{wavelength},{flux}" for wavelength, flux in rows)
    (case_dir / "scattering_spectrum.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_local_meep_candidate_convergence_help():
    result = subprocess.run(
        [sys.executable, str(CONVERGENCE_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "--matrix-dir" in result.stdout
    assert "--latest" in result.stdout
    assert "--peak-shift-threshold-nm" in result.stdout


def test_local_meep_candidate_convergence_fake_matrix(tmp_path):
    matrix_dir = tmp_path / "candidate-hardening- fake"
    _write_csv(matrix_dir / "repeat-1", [(400, 0.0), (500, 1.0), (600, 0.0)])
    _write_csv(matrix_dir / "repeat-2", [(400, 0.0), (500, 1.0), (600, 0.0)])
    _write_csv(matrix_dir / "runtime-100", [(400, 0.0), (500, 0.8), (600, 0.0)])
    output_path = tmp_path / "summary.json"

    result = subprocess.run(
        [
            sys.executable,
            str(CONVERGENCE_SCRIPT),
            "--matrix-dir",
            str(matrix_dir),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert output_path.exists()
    summary = json.loads(output_path.read_text(encoding="utf-8"))
    assert summary["baseline_case"] == "repeat-1"
    assert "repeat-2" in summary["compared_cases"]
    assert "runtime-100" in summary["compared_cases"]
    assert "runtime-200" in summary["missing_cases"]
