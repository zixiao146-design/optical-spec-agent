"""Application-domain benchmark script tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_application_domain_benchmark_script_runs_and_writes_report(tmp_path: Path):
    report = tmp_path / "application-domain-benchmark-report.json"
    env = dict(os.environ)
    env["OSA_APPLICATION_DOMAIN_BENCHMARK_REPORT"] = str(report)
    result = subprocess.run(
        [sys.executable, "scripts/evaluate_application_domain_benchmarks.py"],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "APPLICATION DOMAIN BENCHMARKS PASSED" in result.stdout
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert "NO UPLOAD PERFORMED" in result.stdout
    assert "NO TAG CREATED" in result.stdout
    assert "NO RELEASE CREATED" in result.stdout
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["summary"]["fail"] == 0
    assert payload["external_solver_executed"] is False
