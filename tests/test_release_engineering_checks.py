"""Release-engineering script and contract tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )


def test_cli_surface_check_runs():
    result = _run(["scripts/check_cli_surface.py", "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["schema_version"] == "cli_surface_check.v0.1"
    assert report["errors"] == []


def test_docs_consistency_check_runs():
    result = _run(["scripts/check_docs_consistency.py", "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["schema_version"] == "docs_consistency_check.v0.1"
    assert report["errors"] == []


def test_release_readiness_report_schema(tmp_path):
    report_path = tmp_path / "release_readiness_report.json"
    result = _run(["scripts/check_release_readiness.py", "--report", str(report_path), "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["schema_version"] == "release_readiness_report.v0.1"
    assert "status" in report
    assert "blockers" in report
    assert "warnings" in report
    assert "recommended_actions" in report


def test_artifact_contract_check_generates_report(tmp_path):
    output_dir = tmp_path / "artifact_contracts"
    report_path = tmp_path / "artifact_contract_report.json"
    result = _run(
        [
            "scripts/check_artifact_contracts.py",
            "--output-dir",
            str(output_dir),
            "--report",
            str(report_path),
            "--json",
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["schema_version"] == "artifact_contract_check.v0.1"
    assert report["errors"] == []
    assert "execution_diagnostics.json" in report["artifacts"]
    assert "mesh_report.csv" in report["artifacts"]
    assert "flux_report.csv" in report["artifacts"]


def test_regenerate_demo_outputs_runs(tmp_path):
    result = _run(["scripts/regenerate_demo_outputs.py", "--output-dir", str(tmp_path)])
    assert result.returncode == 0, result.stdout + result.stderr
    manifest = tmp_path / "demo_manifest.json"
    assert manifest.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["schema_version"] == "demo_artifacts.v0.1"
    assert data["generated_outputs"]


def test_pytest_markers_registered():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    markers = "\n".join(pyproject["tool"]["pytest"]["ini_options"]["markers"])
    assert "meep" in markers
    assert "external_solver" in markers
    assert "external_llm" in markers
    assert "slow" in markers
