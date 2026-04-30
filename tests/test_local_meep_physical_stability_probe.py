"""Tests for the manual/local v0.6 physical stability probe script."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROBE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_meep_physical_stability_probe.py"


def test_local_meep_physical_stability_probe_help():
    result = subprocess.run(
        [sys.executable, str(PROBE_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "--quick" in result.stdout
    assert "--only" in result.stdout
    assert "--dry-run" in result.stdout
    assert "low-cost-dielectric-sanity-control" in result.stdout


def test_local_meep_physical_stability_probe_dry_run_low_cost(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(PROBE_SCRIPT),
            "--only",
            "low-cost-dielectric-sanity-control",
            "--dry-run",
            "--output-root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["dry_run"] is True
    assert len(data["cases"]) == 1
    case = data["cases"][0]
    assert case["case_name"] == "low-cost-dielectric-sanity-control"
    assert case["diagnostic_profile"] == "low_cost"
    assert case["success"] is None
