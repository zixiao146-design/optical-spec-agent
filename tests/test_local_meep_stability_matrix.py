"""Tests for the manual/local Meep stability matrix script."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


MATRIX_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_meep_stability_matrix.py"


def test_local_meep_stability_matrix_help():
    result = subprocess.run(
        [sys.executable, str(MATRIX_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "--timeout-research" in result.stdout
    assert "--skip-research" in result.stdout
    assert "--strict" in result.stdout
    assert "low-cost-dielectric-sanity" in result.stdout
