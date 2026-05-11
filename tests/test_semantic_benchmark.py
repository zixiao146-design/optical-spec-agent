"""Smoke test for the semantic benchmark runner."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_semantic_benchmark_runner_passes():
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "benchmarks/run_semantic_benchmark.py"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_semantic_benchmark_report_output(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    report_path = tmp_path / "semantic_report.json"
    result = subprocess.run(
        [
            sys.executable,
            "benchmarks/run_semantic_benchmark.py",
            "--report",
            str(report_path),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert report_path.exists()
    import json

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["schema_version"] == "semantic_benchmark_report.v0.1"
    assert report["all_passed"] is True
    assert report["case_count"] >= 15
    assert all("checks" in case for case in report["cases"])
    assert all("case_name" in case for case in report["cases"])
