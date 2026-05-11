"""Tests for the workflow benchmark runner."""

import json
import subprocess
import sys
from pathlib import Path


def test_workflow_cases_load():
    cases = json.loads(Path("benchmarks/workflow_cases.json").read_text(encoding="utf-8"))
    assert len(cases) >= 12
    assert all("text" in case for case in cases)


def test_workflow_benchmark_generates_report(tmp_path):
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(
        json.dumps(
            [
                {
                    "id": "tiny_mpb",
                    "text": "用 MPB 计算二维光子晶体 band diagram。",
                    "parser": "hybrid",
                    "llm_provider": "mock",
                    "tool": "mpb",
                    "expected_steps": ["parse", "generation"],
                    "expected_artifacts": ["workflow_run.json", "artifacts/generated_input.py"],
                    "not_expected_claims": ["solver_executed"],
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    report = tmp_path / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            "benchmarks/run_workflow_benchmark.py",
            "--cases",
            str(cases_path),
            "--output-dir",
            str(tmp_path / "outputs"),
            "--report",
            str(report),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["passed_cases"] == 1
