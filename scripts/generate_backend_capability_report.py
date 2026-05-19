#!/usr/bin/env python3
"""Generate a local backend capability report.

This script is deliberately local-only. It does not execute external solvers,
does not call external LLMs, does not upload, and does not create tags or
releases.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optical_spec_agent.agents.capability_report import (  # noqa: E402
    BackendCapabilityReport,
    generate_backend_capability_report,
)


def _write_json(report: BackendCapabilityReport, path: Path) -> None:
    path.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _write_markdown(report: BackendCapabilityReport, path: Path) -> None:
    payload = report.model_dump(mode="json")
    lines = [
        "# Backend Capability Report",
        "",
        "This generated report records what the local backend can actually import, call,",
        "execute, or block today. It is preview/design-assist evidence, not",
        "production-grade physical validation.",
        "",
        "## Package",
        "",
        f"- package_version: `{payload['package']['package_version']}`",
        f"- current_public_prerelease: `{payload['package']['current_public_prerelease']}`",
        f"- main_development_version: `{payload['package']['main_development_version']}`",
        f"- pypi_published: `{payload['package']['pypi_published']}`",
        f"- testpypi_verified_for: `{payload['package']['testpypi_verified_for']}`",
        "",
        "## Sub-Agents",
        "",
        "| Role | Module importable | In trace | Executed | Output summary | Evidence refs |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in payload["sub_agents"]:
        lines.append(
            "| {role_name} | {importable_module} | {role_exists_in_trace} | "
            "{executed_in_sample_session} | {output_summary_available} | "
            "{evidence_refs_available} |".format(**item)
        )

    lines.extend(
        [
            "",
            "## Internal Tools",
            "",
            "| Tool | Importable | Callable | Executed in sample |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in payload["internal_tools"]:
        lines.append(
            "| {tool_name} | {importable} | {callable} | {executed_in_sample} |".format(
                **item
            )
        )

    lines.extend(
        [
            "",
            "## Optical Calculators",
            "",
            "| Calculator | Implemented | Quality | Production claim | Formal proof claim |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["optical_calculators"]:
        lines.append(
            "| {calculator_name} | {implemented} | {quality_level} | "
            "{production_grade_validation_claimed} | "
            "{formal_convergence_proof_claimed} |".format(**item)
        )

    lines.extend(
        [
            "",
            "## Design Case Cross-Checks",
            "",
            "| Example | Status | Calculator called | Expected calculator |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in payload["design_case_cross_checks"]:
        lines.append(
            "| {example_id} | {status} | {calculator_called} | {expected_calculator} |".format(
                **item
            )
        )

    lines.extend(
        [
            "",
            "## Requirement Templates",
            "",
            "| Template | EN goal | ZH goal | Heuristic match | Cross-check | Preview only |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["requirements_templates"]:
        lines.append(
            "| {template_id} | {goal_en_present} | {goal_zh_present} | "
            "{matched_by_heuristic} | {cross_check_status} | {preview_only} |".format(
                **item
            )
        )

    golden = payload["adapter_native_golden_coverage"]
    lines.extend(
        [
            "",
            "## Adapter-Native Golden Coverage",
            "",
            f"- status: `{golden['status']}`",
            f"- adapters_covered: `{', '.join(golden['adapters_covered'])}`",
            f"- missing_adapters: `{', '.join(golden['missing_adapters']) or 'none'}`",
            "- preview_only: `True`",
            "",
            "| Adapter | Case | Source | Monitor | Observables | Solver required | Solver executed | Coverage |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in golden["coverage_items"]:
        lines.append(
            "| {adapter_name} | {case_id} | {source_type} | {monitor_type} | {observables} | "
            "{requires_solver_for_real_result} | {external_solver_executed} | {coverage_status} |".format(
                observables=", ".join(item["observable_kinds"]),
                **item,
            )
        )

    lines.extend(
        [
            "",
            "## Blocked External Actions",
            "",
            "| Action | Default allowed | Executed | Reason |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in payload["blocked_external_actions"]:
        lines.append(
            "| {action_name} | {default_allowed} | {executed} | {reason} |".format(**item)
        )

    lines.extend(
        [
            "",
            "## Safety Markers",
            "",
            "- NO SOLVER EXECUTION PERFORMED",
            "- NO EXTERNAL LLM CALLED",
            "- NO UPLOAD PERFORMED",
            "- NO TAG CREATED",
            "- NO RELEASE CREATED",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _print_summary(report: BackendCapabilityReport) -> None:
    payload: dict[str, Any] = report.model_dump(mode="json")
    print("Backend capability report")
    print(f"package_version={payload['package']['package_version']}")
    print(f"sub_agents={len(payload['sub_agents'])}")
    print(f"internal_tools={len(payload['internal_tools'])}")
    print(f"optical_calculators={len(payload['optical_calculators'])}")
    print(f"requirements_templates={len(payload['requirements_templates'])}")
    golden = payload["adapter_native_golden_coverage"]
    print(f"adapter_native_golden_coverage={golden['status']}")
    print(f"adapter_native_golden_adapters={','.join(golden['adapters_covered'])}")
    print(f"design_case_cross_checks={len(payload['design_case_cross_checks'])}")
    print(
        "blocked_external_actions="
        f"{len(payload['blocked_external_actions'])}"
    )
    print("NO SOLVER EXECUTION PERFORMED")
    print("NO EXTERNAL LLM CALLED")
    print("NO UPLOAD PERFORMED")
    print("NO TAG CREATED")
    print("NO RELEASE CREATED")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, help="Optional JSON output path.")
    parser.add_argument("--markdown-out", type=Path, help="Optional Markdown output path.")
    args = parser.parse_args()

    report = generate_backend_capability_report()
    if args.json_out:
        _write_json(report, args.json_out)
    if args.markdown_out:
        _write_markdown(report, args.markdown_out)
    _print_summary(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
