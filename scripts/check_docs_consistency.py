#!/usr/bin/env python3
"""Lightweight documentation consistency checks for release readiness."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
README_ZH = ROOT / "README.zh-CN.md"
DOCS = ROOT / "docs"
SRC = ROOT / "src" / "optical_spec_agent"

README_REQUIRED_PHRASES = [
    "Release status",
    "Current scope",
    "What works",
    "What does NOT work yet",
    "Quick start",
    "Roadmap",
    "License",
]

MISLEADING_PATTERNS = [
    "production-grade physical validation",
    "production-ready solver input",
    "fully automated solver",
    "validated physical result",
    "formal convergence proof",
    "real LLM provider required",
    "external solvers are run by default",
]

NEGATION_HINTS = [
    "no ",
    "not ",
    "never ",
    "does not",
    "do not",
    "is not",
    "are not",
    "without",
    "non-goal",
    "limitation",
    "limitations",
    "not production",
    "not a production",
    "not solver",
    "only",
    "scaffold",
    "doesn't",
    "block",
    "blocker",
    "contradict",
    "imply",
    "must not",
    "不是",
    "不提供",
    "不声明",
    "不声称",
    "不运行",
    "不默认",
    "不要",
    "不能",
    "不会",
    "限制",
    "已知限制",
    "不是最终",
]


def _line_is_negated(line: str) -> bool:
    lowered = line.lower()
    return any(hint in lowered for hint in NEGATION_HINTS)


def _scan_misleading_claims() -> list[str]:
    findings: list[str] = []
    for path in [README, README_ZH, *sorted(DOCS.glob("*.md"))]:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            lowered = line.lower()
            context = " ".join(lines[max(0, lineno - 5) : lineno + 2])
            for phrase in MISLEADING_PATTERNS:
                if phrase.lower() in lowered and not _line_is_negated(context):
                    findings.append(f"{path.relative_to(ROOT)}:{lineno}: {phrase}")
    return findings


def _release_doc_pairs() -> list[str]:
    warnings: list[str] = []
    def normalize(version: str) -> str:
        return version[:-2] if version.endswith(".0") else version

    readiness_versions = {
        normalize(re.search(r"release_readiness_v(.+)\.md", path.name).group(1))
        for path in DOCS.glob("release_readiness_v*.md")
        if re.search(r"release_readiness_v(.+)\.md", path.name)
    }
    notes_versions = {
        normalize(re.search(r"release_notes_v(.+)\.md", path.name).group(1))
        for path in DOCS.glob("release_notes_v*.md")
        if re.search(r"release_notes_v(.+)\.md", path.name)
    }
    for version in sorted(readiness_versions - notes_versions):
        warnings.append(f"release_readiness_v{version}.md has no matching release_notes_v{version}.md")
    for version in sorted(notes_versions - readiness_versions):
        if version in {"0.2", "0.5"}:
            continue
        warnings.append(f"release_notes_v{version}.md has no matching release_readiness_v{version}.md")
    return warnings


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not README.exists():
        errors.append("README.md is missing.")
        readme_text = ""
    else:
        readme_text = README.read_text(encoding="utf-8")

    if not README_ZH.exists():
        errors.append("README.zh-CN.md is missing.")
        readme_zh_text = ""
    else:
        readme_zh_text = README_ZH.read_text(encoding="utf-8")

    for phrase in README_REQUIRED_PHRASES:
        if phrase not in readme_text:
            errors.append(f"README.md must include `{phrase}`.")

    if "README.zh-CN.md" not in readme_text:
        errors.append("README.md must link to README.zh-CN.md.")
    if "README.md" not in readme_zh_text:
        errors.append("README.zh-CN.md must link back to README.md.")

    bilingual_requirements = [
        ("0.9.0rc1", "README.zh-CN.md must mention 0.9.0rc1."),
        ("release candidate", "README.zh-CN.md must mention release candidate status."),
        ("不是求解器", "README.zh-CN.md must state that the project is not a solver."),
        (
            "不提供 production-grade physical validation",
            "README.zh-CN.md must state no production-grade physical validation.",
        ),
        ("adapter outputs", "README.zh-CN.md must discuss adapter outputs."),
        ("MVP/scaffold", "README.zh-CN.md must discuss MVP/scaffold limitations."),
        ("workflow", "README.zh-CN.md must discuss workflow scope."),
        ("本地同步", "README.zh-CN.md must state workflow is local/synchronous."),
    ]
    for needle, message in bilingual_requirements:
        if needle not in readme_zh_text:
            errors.append(message)
    if "release candidate" not in readme_text:
        errors.append("README.md must mention release candidate status.")

    if (DOCS / "llm_parser_v0.8.md").exists() and "parser" not in readme_text.lower():
        errors.append("README.md should mention parser modes because LLM parser docs exist.")

    if (DOCS / "adapter_mvp_v0.7.md").exists():
        if "adapter-list" not in readme_text or "adapter-generate" not in readme_text:
            errors.append("README.md should mention adapter-list and adapter-generate.")

    workflows_dir = SRC / "workflows"
    if workflows_dir.exists() and "workflow" not in readme_text.lower():
        errors.append("Workflow code exists, but README.md does not mention workflow scope.")

    if not (DOCS / "versioning_policy.md").exists():
        errors.append("docs/versioning_policy.md is missing.")

    if not (DOCS / "release_readiness_current.md").exists():
        errors.append("docs/release_readiness_current.md is missing.")

    errors.extend(_scan_misleading_claims())
    warnings.extend(_release_doc_pairs())

    readiness = DOCS / "release_readiness_current.md"
    if readiness.exists():
        current_text = readiness.read_text(encoding="utf-8").lower()
        pyproject = ROOT / "pyproject.toml"
        if pyproject.exists():
            version = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {}).get(
                "version"
            )
            if version and version not in readme_text:
                errors.append(f"README.md does not mention current pyproject version {version}.")
            if version and version not in readme_zh_text:
                errors.append(
                    f"README.zh-CN.md does not mention current pyproject version {version}."
                )
            if version and version not in current_text:
                errors.append(
                    f"release_readiness_current.md does not mention current pyproject version {version}."
                )

    return {
        "schema_version": "docs_consistency_check.v0.1",
        "status": "blocked" if errors else ("warning" if warnings else "ready"),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Docs consistency check: {report['status']}")
        for error in report["errors"]:
            print(f"ERROR: {error}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
