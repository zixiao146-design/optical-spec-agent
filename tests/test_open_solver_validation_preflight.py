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
    assert "import meep as mp" in text
    assert "from meep import mpb" in text
    assert "import optiland" in text

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
    assert "command -v \"${command_name}\"" in text


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
    assert data["package_version"] == "0.9.0rc6"
    assert data["executed_solvers"] is False
    assert data["proprietary_required"] is False
    assert set(data["checked_commands"]) == {"meep", "mpb", "gmsh", "ElmerSolver", "optiland"}
    assert set(data["solvers"]) == {"gmsh", "meep", "mpb", "optiland", "elmer"}
    for solver in data["solvers"].values():
        assert set(solver) == {
            "cli_available",
            "cli_path",
            "python_available",
            "python_detail",
            "available",
            "execution_performed",
        }
        assert solver["execution_performed"] is False


def test_open_solver_preflight_detects_python_backed_availability(tmp_path):
    module_root = tmp_path / "modules"
    meep_pkg = module_root / "meep"
    meep_pkg.mkdir(parents=True)
    (meep_pkg / "__init__.py").write_text("__version__ = '1.33.0'\n", encoding="utf-8")
    (meep_pkg / "mpb.py").write_text("# fake MPB module for import-only detection\n", encoding="utf-8")
    (module_root / "optiland.py").write_text("__version__ = '0.6.0'\n", encoding="utf-8")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_gmsh = bin_dir / "gmsh"
    fake_gmsh.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
    fake_gmsh.chmod(0o755)

    report = tmp_path / "open-solver-preflight.json"
    env = os.environ.copy()
    env["OSA_SOLVER_PREFLIGHT_JSON"] = str(report)
    env["PYTHONPATH"] = str(module_root)
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

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
    data = json.loads(report.read_text(encoding="utf-8"))
    solvers = data["solvers"]
    assert solvers["gmsh"]["cli_available"] is True
    assert solvers["gmsh"]["available"] is True
    assert solvers["meep"]["python_available"] is True
    assert solvers["meep"]["available"] is True
    assert solvers["mpb"]["python_available"] is True
    assert solvers["mpb"]["available"] is True
    assert solvers["optiland"]["python_available"] is True
    assert solvers["optiland"]["available"] is True
    assert solvers["elmer"]["available"] is False
    for solver in solvers.values():
        assert solver["execution_performed"] is False
