"""Optional solver readiness script tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_readiness_script_default_mode(tmp_path: Path):
    script = ROOT / "scripts" / "check_optional_solver_readiness.py"
    assert script.exists()
    text = script.read_text(encoding="utf-8")
    for marker in [
        "SOLVER READINESS CHECK PASSED",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
    ]:
        assert marker in text
    assert "subprocess.run" in text
    assert "OSA_SOLVER_PYTHON" in text
    assert "OSA_SOLVER_READINESS_PROFILE" in text
    for forbidden in [
        "twine upload",
        "gh release create",
        "git tag",
        "OSA_RUN_OPTIONAL_GMSH_VALIDATION=1",
    ]:
        assert forbidden not in text

    report_path = tmp_path / "solver-readiness.json"
    env = os.environ.copy()
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
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert "NO UPLOAD PERFORMED" in result.stdout
    assert "NO TAG CREATED" in result.stdout
    assert "NO RELEASE CREATED" in result.stdout
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "optional_solver_readiness.v0.2"
    assert payload["detection_profile"] == "current"
    assert payload["python_executable_used"]
    assert "python_probe_available" in payload
    assert "cli_probe_path" in payload
    assert "module_probe_results" in payload
    assert payload["availability_detection_only"] is True
    assert payload["default_executes_solver"] is False
    assert payload["external_solver_executed"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False
    solvers = {item["solver_name"]: item for item in payload["solvers"]}
    assert set(solvers) == {"gmsh", "meep", "mpb", "optiland", "elmer"}
    for item in solvers.values():
        assert item["availability_checked"] is True
        assert item["detection_profile"] == "current"
        assert item["python_executable_used"]
        assert "python_probe_available" in item
        assert "detected_in_profile" in item
        assert "cli_probe_path" in item
        assert "module_probe_results" in item
        assert "command_probe_results" in item
        assert item["default_executes_solver"] is False
        assert item["production_grade_validation_claimed"] is False
        assert item["formal_convergence_proof_claimed"] is False
    assert solvers["elmer"]["install_deferred"] is True
