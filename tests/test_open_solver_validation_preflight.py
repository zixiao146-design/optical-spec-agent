"""No-execution open-source solver validation preflight checks."""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "open_solver_validation_preflight.sh"


def test_open_solver_preflight_script_exists_and_is_no_execution():
    assert SCRIPT.exists()
    text = SCRIPT.read_text(encoding="utf-8")
    assert "NO SOLVER EXECUTION PERFORMED" in text
    assert "NO PROPRIETARY SOLVER REQUIRED" in text
    assert "NO TAG CREATED" in text
    assert "NO RELEASE CREATED" in text
    assert "NO UPLOAD PERFORMED" in text
    assert "command -v" in text

    forbidden = [
        "twine upload",
        "python -m twine upload",
        "gh release create",
        "git tag",
        "git push",
    ]
    lowered = text.lower()
    for phrase in forbidden:
        assert phrase not in lowered


def test_open_solver_preflight_does_not_directly_execute_solver_commands():
    text = SCRIPT.read_text(encoding="utf-8")
    executable_line = re.compile(r"^\s*(meep|mpb|gmsh|ElmerSolver|optiland)(\s|$)")
    for line in text.splitlines():
        assert not executable_line.search(line), f"solver command appears executable: {line}"
    assert "command -v \"${candidate}\"" in text


def test_open_solver_preflight_runs_without_installed_solvers_and_writes_json(tmp_path):
    report = tmp_path / "open-solver-preflight.json"
    env = os.environ.copy()
    env["OSA_SOLVER_PREFLIGHT_JSON"] = str(report)
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
        env=env,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO PROPRIETARY SOLVER REQUIRED" in result.stdout
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["package_version"] == "0.9.0rc5.dev0"
    assert data["executed_solvers"] is False
    assert data["proprietary_required"] is False
    assert set(data["checked_commands"]) == {"meep", "mpb", "gmsh", "ElmerSolver", "optiland"}

