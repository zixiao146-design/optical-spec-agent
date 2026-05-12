#!/usr/bin/env python3
"""Check release-readiness prerequisites without creating a release or tag."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _pyproject(root: Path) -> dict[str, Any]:
    path = root / "pyproject.toml"
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _workflow_contains_required_gate(root: Path) -> bool:
    workflows = root / ".github" / "workflows"
    text = "\n".join(_read_text(path) for path in workflows.glob("*.yml"))
    return "pytest" in text and "run_benchmark.py --mode key_fields" in text


def _formal_release_claim_version(readme: str) -> str | None:
    patterns = [
        r"formal GitHub release\s*(?:is|:)\s*`?v?([0-9][0-9A-Za-z.\-]*)`?",
        r"released version\s*(?:is|:)\s*`?v?([0-9][0-9A-Za-z.\-]*)`?",
        r"GitHub release\s*(?:is|:)\s*`?v?([0-9][0-9A-Za-z.\-]*)`?",
    ]
    for pattern in patterns:
        match = re.search(pattern, readme, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def _release_notes_misclaim_release(docs: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(docs.glob("release_notes*.md")):
        text = _read_text(path)
        lowered = text.lower()
        if "released" not in lowered:
            continue
        if any(marker in lowered for marker in ["draft only", "draft", "preview", "release candidate"]):
            continue
        findings.append(f"{path.name} uses release language without draft/preview/RC context.")
    return findings


def build_report(root: Path = DEFAULT_ROOT) -> dict[str, Any]:
    pyproject = _pyproject(root)
    project = pyproject.get("project", {})
    optional = project.get("optional-dependencies", {})
    readme = _read_text(root / "README.md")
    docs = root / "docs"
    src = root / "src" / "optical_spec_agent"

    blockers: list[str] = []
    warnings: list[str] = []
    actions: list[str] = []

    version = project.get("version")
    if not version:
        blockers.append("pyproject.toml is missing project.version.")

    if "Release status" not in readme:
        blockers.append("README.md is missing release status.")

    required_docs = [
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
    ]
    for name in required_docs:
        if not (docs / name).exists():
            blockers.append(f"docs/{name} is missing.")

    if "check:" not in _read_text(root / "Makefile"):
        blockers.append("Makefile is missing a check target.")
    if not (root / "tests").exists():
        blockers.append("tests/ is missing.")
    if not (root / "benchmarks").exists():
        blockers.append("benchmarks/ is missing.")

    lower_readme = readme.lower()
    if (
        "production-grade physical validation" in lower_readme
        and "no production-grade physical validation" not in lower_readme
        and "not production-grade physical validation" not in lower_readme
    ):
        blockers.append("README may overclaim production-grade physical validation.")

    if (src / "workflows").exists() and not (docs / "workflow_orchestration_v0.9.md").exists():
        blockers.append("Workflow code exists but workflow docs are missing.")
    if (src / "parsers" / "llm").exists() and not (docs / "llm_parser_v0.8.md").exists():
        blockers.append("LLM parser code exists but docs/llm_parser_v0.8.md is missing.")
    if (src / "adapters" / "mpb").exists() and not (docs / "adapter_mvp_v0.7.md").exists():
        blockers.append("Multi-solver adapter code exists but adapter MVP docs are missing.")
    if "diagnose" in _read_text(src / "cli" / "main.py") and not (
        docs / "physical_diagnostics_v0.6.md"
    ).exists():
        blockers.append("diagnose command exists but physical diagnostics docs are missing.")

    formal_claim = _formal_release_claim_version(readme)
    if formal_claim and version and formal_claim != version:
        blockers.append(
            f"README claims formal GitHub release {formal_claim}, but pyproject version is {version}."
        )

    blockers.extend(_release_notes_misclaim_release(docs))

    if not _workflow_contains_required_gate(root):
        warnings.append("GitHub Actions should include pytest and key-field benchmark gates.")

    dependencies = project.get("dependencies", [])
    dev_dependencies = optional.get("dev", [])
    if "pytest" not in "\n".join(dev_dependencies):
        blockers.append("dev optional dependencies should include pytest.")
    if "build" not in "\n".join(dev_dependencies):
        warnings.append("dev optional dependencies should include build for release dry-runs.")
    if "twine" not in "\n".join(dev_dependencies):
        warnings.append("dev optional dependencies should include twine for artifact checks.")

    if version == "0.5.0" and "v0.9" in readme:
        warnings.append(
            "Version mismatch is intentional if main branch capabilities are unreleased preview. "
            "See docs/versioning_policy.md and docs/release_decision_matrix.md."
        )
        actions.append("Decide whether to keep 0.5.0 preview status or prepare 0.9.0rc1.")

    status = "blocked" if blockers else ("warning" if warnings else "ready")
    return {
        "schema_version": "release_readiness_report.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,
        "project_name": project.get("name"),
        "pyproject_version": version,
        "requires_python": project.get("requires-python"),
        "dependencies": dependencies,
        "dev_dependencies": dev_dependencies,
        "blockers": blockers,
        "warnings": warnings,
        "recommended_actions": actions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero on warnings too.")
    args = parser.parse_args()
    report = build_report(args.root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Release readiness: {report['status']}")
        for blocker in report["blockers"]:
            print(f"BLOCKER: {blocker}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
        for action in report["recommended_actions"]:
            print(f"ACTION: {action}")
        if args.report:
            print(f"Report written to {args.report}")
    if report["blockers"] or (args.strict and report["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
