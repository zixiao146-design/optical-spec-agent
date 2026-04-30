"""Tests for the manual/local v0.6 candidate hardening script."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HARDENING_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_meep_candidate_hardening.py"


def test_local_meep_candidate_hardening_help():
    result = subprocess.run(
        [sys.executable, str(HARDENING_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "--repeatability-only" in result.stdout
    assert "--dry-run" in result.stdout
    assert "repeat-1" in result.stdout


def test_local_meep_candidate_hardening_dry_run(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(HARDENING_SCRIPT),
            "--repeatability-only",
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
    assert [case["case_name"] for case in data["cases"]] == ["repeat-1", "repeat-2", "repeat-3"]
    assert all(case["csv_sanity"] is None for case in data["cases"])
