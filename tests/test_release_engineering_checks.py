"""Release-engineering script and contract tests."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_docs_check_module():
    path = ROOT / "scripts" / "check_docs_consistency.py"
    spec = importlib.util.spec_from_file_location("check_docs_consistency_for_tests", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_validation_boundary_docs_keep_non_overclaiming_contract():
    text = (ROOT / "docs" / "validation_boundary.md").read_text(encoding="utf-8")
    required = [
        "No production-grade physical validation",
        "No formal convergence proof",
        "External solver validation is optional/manual",
        "do not require Meep, MPB, Gmsh, Elmer, Optiland, or external LLM providers",
    ]
    for phrase in required:
        assert phrase in text


def test_pypi_publication_decision_requires_explicit_approval():
    text = (ROOT / "docs" / "pypi_publication_decision.md").read_text(encoding="utf-8")
    assert "PyPI published: no" in text
    assert "Do not publish automatically" in text
    assert "explicit maintainer approval" in text


def test_validation_and_packaging_gate_docs_exist_and_bound_claims():
    required_docs = [
        "packaging_gate.md",
        "validation_gate.md",
        "external_solver_policy.md",
        "external_llm_policy.md",
        "pypi_publication_decision.md",
        "validation_boundary.md",
        "release_engineering_playbook.md",
        "adapter_support_matrix.md",
        "testpypi_dry_run_gate.md",
        "v1_0_stability_gate.md",
        "schema_compatibility_policy.md",
        "open_source_solver_strategy.md",
        "proprietary_solver_policy.md",
        "v1_0_compatibility_policy.md",
        "validation_evidence_manifest.md",
        "open_source_solver_validation_plan.md",
    ]
    for name in required_docs:
        assert (ROOT / "docs" / name).exists()
    assert (ROOT / "examples" / "README.md").exists()
    assert (ROOT / "examples" / "examples_manifest.json").exists()

    combined = "\n".join(
        (ROOT / "docs" / name).read_text(encoding="utf-8") for name in required_docs
    )
    assert "PyPI published: no" in combined or "PyPI status: not published" in combined
    assert "TestPyPI upload requires explicit maintainer approval" in combined
    assert "No production-grade physical validation" in combined
    assert "No formal convergence proof" in combined
    assert "External solvers are not run by default" in combined
    assert "External LLM access is not required by default" in combined
    assert "open-source-solver-first" in combined
    assert "not default dependencies" in combined
    assert "No proprietary license is required" in combined
    assert "v1.0 compatibility" in combined
    assert "Validation Evidence Manifest" in combined
    assert "Open-source Solver Validation Plan" in combined
    assert "0.9.0rc4.dev0" in combined
    assert "v0.9.0rc3" in combined
    assert "Never move existing tags" in combined
    assert "No automatic package publishing" in combined


def test_adapter_support_matrix_covers_registered_adapter_families():
    from optical_spec_agent.adapters.registry import list_adapters

    text = (ROOT / "docs" / "adapter_support_matrix.md").read_text(encoding="utf-8")
    for metadata in list_adapters():
        assert f"`{metadata.tool_name}`" in text
        assert metadata.current_status in text
    assert "External solvers are not run by default" in text
    assert "External LLM providers are not required" in text
    assert "no production-grade physical validation" in text.lower()
    assert "open-source-solver-first" in text
    assert "Proprietary/export-only future target" in text
    assert "not registered adapters unless" in text
    assert "0.9.0rc4.dev0" in text
    assert "v0.9.0rc3" in text
    assert "PyPI/TestPyPI remain unpublished" in text


def test_v1_evidence_docs_and_examples_are_offline_and_unpublished():
    paths = [
        ROOT / "examples" / "README.md",
        ROOT / "docs" / "release_readiness_current.md",
        ROOT / "docs" / "schema_compatibility_policy.md",
        ROOT / "docs" / "testpypi_dry_run_gate.md",
        ROOT / "docs" / "v1_0_stability_gate.md",
        ROOT / "docs" / "validation_gate.md",
        ROOT / "docs" / "packaging_gate.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    required = [
        "offline by default",
        "no external solver",
        "external LLM",
        "PyPI/TestPyPI remain unpublished",
        "not uploaded",
        "0.9.0rc4.dev0",
        "not a public release",
        "v0.9.0rc4",
        "not created",
    ]
    for phrase in required:
        assert phrase in combined


def test_external_solver_policy_keeps_solver_validation_optional():
    text = (ROOT / "docs" / "external_solver_policy.md").read_text(encoding="utf-8")
    assert "External solvers are not run by default" in text
    assert "Optional solver validation may be run manually" in text
    assert "No production-grade physical validation is claimed" in text
    assert "open-source-solver-first" in text
    assert "Proprietary commercial tools" in text
    assert "No proprietary license is required" in text


def test_external_llm_policy_keeps_network_llm_optional_and_tokens_safe():
    text = (ROOT / "docs" / "external_llm_policy.md").read_text(encoding="utf-8")
    assert "External LLM access is not required by default" in text
    assert "Default tests must not require network LLM calls" in text
    assert "Do not print, commit, or store provider tokens" in text


def test_bilingual_readme_contract_present():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    assert "README.zh-CN.md" in readme
    assert "README.md" in readme_zh
    assert "0.9.0rc1" in readme_zh
    assert "不是求解器" in readme_zh
    assert "不提供 production-grade physical validation" in readme_zh
    assert "MVP/scaffold" in readme_zh
    assert "workflow" in readme_zh
    assert "本地同步" in readme_zh


def test_docs_consistency_detects_missing_chinese_readme(tmp_path, monkeypatch):
    module = _load_docs_check_module()
    docs = tmp_path / "docs"
    src = tmp_path / "src" / "optical_spec_agent"
    docs.mkdir()
    src.mkdir(parents=True)
    (tmp_path / "README.md").write_text(
        """
# optical-spec-agent

Release status: current package version is 0.9.0rc1 release candidate.

## Current scope
## What works
## What does NOT work yet
## Quick start
## Roadmap
## License
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "optical-spec-agent"
version = "0.9.0rc1"
""".strip(),
        encoding="utf-8",
    )
    (docs / "versioning_policy.md").write_text("policy\n", encoding="utf-8")
    (docs / "release_readiness_current.md").write_text("0.9.0rc1\n", encoding="utf-8")

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "README", tmp_path / "README.md")
    monkeypatch.setattr(module, "README_ZH", tmp_path / "README.zh-CN.md")
    monkeypatch.setattr(module, "DOCS", docs)
    monkeypatch.setattr(module, "SRC", src)

    report = module.build_report()
    assert report["status"] == "blocked"
    assert "README.zh-CN.md is missing." in report["errors"]


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
