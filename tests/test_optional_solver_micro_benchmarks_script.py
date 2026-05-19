"""Unified optional solver micro-benchmark script tests."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _no_opt_in_env(tmp_path: Path) -> dict[str, str]:
    env = os.environ.copy()
    for key in [
        "OSA_RUN_OPTIONAL_GMSH_VALIDATION",
        "OSA_RUN_OPTIONAL_MEEP_VALIDATION",
        "OSA_RUN_OPTIONAL_MPB_VALIDATION",
        "OSA_RUN_OPTIONAL_OPTILAND_VALIDATION",
        "OSA_RUN_OPTIONAL_ELMER_VALIDATION",
    ]:
        env.pop(key, None)
    env["OSA_SOLVER_MICRO_BENCHMARK_REPORT"] = str(tmp_path / "solver-micro.json")
    return env


def test_optional_solver_micro_benchmark_script_default_mode(tmp_path: Path):
    script = ROOT / "scripts" / "run_optional_solver_micro_benchmarks.sh"
    assert script.exists()
    text = script.read_text(encoding="utf-8")
    for marker in [
        "OSA_RUN_OPTIONAL_GMSH_VALIDATION",
        "OSA_RUN_OPTIONAL_MEEP_VALIDATION",
        "OSA_RUN_OPTIONAL_MPB_VALIDATION",
        "OSA_RUN_OPTIONAL_OPTILAND_VALIDATION",
        "NO SOLVER EXECUTION PERFORMED BY DEFAULT",
        "NO EXTERNAL LLM CALLED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
    ]:
        assert marker in text
    for forbidden in ["twine upload", "gh release create", "git tag -", "git push --tags"]:
        assert forbidden not in text

    result = subprocess.run(
        [str(script)],
        cwd=ROOT,
        env=_no_opt_in_env(tmp_path),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NO SOLVER EXECUTION PERFORMED BY DEFAULT" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert "NO UPLOAD PERFORMED" in result.stdout
    assert "NO TAG CREATED" in result.stdout
    assert "NO RELEASE CREATED" in result.stdout
    report = json.loads((tmp_path / "solver-micro.json").read_text(encoding="utf-8"))
    assert report["default_runs_solver"] is False
    assert report["opt_in_required"] is True
    assert report["any_opt_in_enabled"] is False
    assert report["external_solver_executed"] is False
    assert all(item["executed"] is False for item in report["results"])

