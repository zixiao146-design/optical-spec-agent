"""Profile-aware optional solver readiness checks."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_readiness_supports_solver_python_profiles(tmp_path: Path):
    script = ROOT / "scripts" / "check_optional_solver_readiness.py"
    text = script.read_text(encoding="utf-8")
    assert "OSA_SOLVER_PYTHON" in text
    assert "OSA_SOLVER_READINESS_PROFILE" in text
    assert "python_executable_used" in text
    assert "module_probe_results" in text
    assert "meep.mpb" not in text  # module names come from the manifest
    assert "subprocess.run" in text
    assert "command_path_only" in text
    assert "external_solver_executed" in text
    for forbidden in ["twine upload", "gh release create", "git tag"]:
        assert forbidden not in text

    report_path = tmp_path / "solver-readiness-profile.json"
    env = os.environ.copy()
    env["OSA_SOLVER_PYTHON"] = sys.executable
    env["OSA_SOLVER_READINESS_PROFILE"] = "test-current-python"
    env["OSA_SOLVER_READINESS_REPORT"] = str(report_path)
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SOLVER READINESS CHECK PASSED" in result.stdout
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["detection_profile"] == "test-current-python"
    assert payload["python_executable_used"] == sys.executable
    assert payload["python_probe_available"] is True
    assert payload["external_solver_executed"] is False
    solvers = {item["solver_name"]: item for item in payload["solvers"]}
    assert "meep.mpb" in {
        probe["module_name"]
        for probe in solvers["mpb"]["module_probe_results"]
    }
    for item in solvers.values():
        assert item["detection_profile"] == "test-current-python"
        assert item["python_executable_used"] == sys.executable
        assert item["default_executes_solver"] is False
        assert item["production_grade_validation_claimed"] is False
        assert item["formal_convergence_proof_claimed"] is False
