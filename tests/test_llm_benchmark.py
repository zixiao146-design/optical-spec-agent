"""Tests for v0.8 LLM benchmark runner."""

import json
import subprocess
import sys
from pathlib import Path


def test_llm_cases_load():
    cases = json.loads(Path("benchmarks/llm_cases.json").read_text(encoding="utf-8"))
    assert len(cases) >= 40
    assert all("id" in case and "text" in case and "expected" in case for case in cases)


def test_run_llm_benchmark_report(tmp_path):
    report = tmp_path / "llm_report.json"
    result = subprocess.run(
        [
            sys.executable,
            "benchmarks/run_llm_benchmark.py",
            "--cases",
            "benchmarks/llm_cases.json",
            "--parser",
            "hybrid",
            "--llm-provider",
            "mock",
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["schema_version"] == "llm_eval_report.v0.8"
    assert data["total_cases"] >= 40
    assert data["passed_cases"] == data["total_cases"]
    assert any(case["allowed_missing"] for case in data["cases"])
