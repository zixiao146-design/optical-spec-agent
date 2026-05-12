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


def _write_minimal_release_repo(root: Path, *, version: str, readme: str) -> None:
    (root / "docs").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "benchmarks").mkdir()
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / "src" / "optical_spec_agent" / "cli").mkdir(parents=True)
    (root / "pyproject.toml").write_text(
        f"""
[project]
name = "optical-spec-agent"
version = "{version}"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0", "build>=1.2", "twine>=5.0"]
""".strip(),
        encoding="utf-8",
    )
    (root / "README.md").write_text(readme, encoding="utf-8")
    (root / "Makefile").write_text("check:\n\tpytest -q\n", encoding="utf-8")
    (root / ".github" / "workflows" / "ci.yml").write_text(
        "steps:\n  - run: pytest -q\n  - run: python benchmarks/run_benchmark.py --mode key_fields\n",
        encoding="utf-8",
    )
    (root / "src" / "optical_spec_agent" / "cli" / "main.py").write_text("", encoding="utf-8")
    for name in [
        "versioning_policy.md",
        "release_readiness_current.md",
        "release_notes_current.md",
        "release_decision_matrix.md",
        "release_blockers_current.md",
        "version_bump_plan_0.9.0rc1.md",
        "artifact_contracts.md",
        "security_and_robustness.md",
        "api_contract.md",
        "cli_contract.md",
        "benchmark_contract.md",
    ]:
        (root / "docs" / name).write_text("Draft preview documentation.\n", encoding="utf-8")


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


def test_release_readiness_intentional_preview_mismatch_is_warning(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.5.0",
        readme=(
            "Release status: packaged baseline is 0.5.0. "
            "Main branch includes v0.9 preview capability, not a formal release."
        ),
    )
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "warning"
    assert report["blockers"] == []
    assert any("intentional" in warning for warning in report["warnings"])


def test_release_readiness_misleading_formal_release_claim_blocks(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.5.0",
        readme="Release status: formal GitHub release is v0.9.0.",
    )
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["status"] == "blocked"
    assert any("formal GitHub release" in blocker for blocker in report["blockers"])


def test_release_readiness_missing_policy_docs_blocks(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.9.0rc1",
        readme="Release status: packaged candidate is 0.9.0rc1.",
    )
    (tmp_path / "docs" / "versioning_policy.md").unlink()
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["status"] == "blocked"
    assert "docs/versioning_policy.md is missing." in report["blockers"]


def test_release_readiness_clean_rc_version_is_ready(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.9.0rc1",
        readme=(
            "Release status: packaged release candidate is 0.9.0rc1. "
            "Capabilities remain preview/scaffold/evaluation work."
        ),
    )
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "ready"
    assert report["warnings"] == []


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
