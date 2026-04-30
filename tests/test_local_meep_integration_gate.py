"""Tests for the manual/local Meep integration gate script."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from optical_spec_agent.execution import find_meep_python


GATE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_meep_integration_gate.py"
_meep_available = find_meep_python() is not None


def test_local_meep_integration_gate_help():
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "--mode" in result.stdout
    assert "research-preview" in result.stdout


@pytest.mark.skipif(not _meep_available, reason="Meep not available locally")
def test_local_meep_integration_gate_smoke(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(GATE_SCRIPT),
            "--mode",
            "smoke",
            "--timeout",
            "300",
            "--output-root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=360,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["success"] is True
    assert data["expected_mode"] == "smoke"
    assert data["run_id"].startswith("local-gate-")
    workdir = Path(data["workdir"])
    assert (workdir / "generated_script.py").exists()
    assert (workdir / "execution_result.json").exists()
    assert (workdir / "run_manifest.json").exists()
