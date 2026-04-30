"""Tests for the manual/local v0.6 observable diagnostics script."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


OBSERVABLE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_meep_observable_diagnostics.py"


def test_local_meep_observable_diagnostics_help():
    result = subprocess.run(
        [sys.executable, str(OBSERVABLE_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "--only" in result.stdout
    assert "top-plane" in result.stdout
    assert "--dry-run" in result.stdout


def test_local_meep_observable_diagnostics_dry_run(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(OBSERVABLE_SCRIPT),
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
    case_names = [case["case_name"] for case in data["cases"]]
    assert "closed-box-baseline" in case_names
    assert "top-plane" in case_names
    unsupported = [
        case for case in data["cases"]
        if case["case_name"] == "closed-box-larger-clearance"
    ][0]
    assert unsupported["supported"] is False
    assert unsupported["errors"] == ["unsupported observable diagnostic profile"]
