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

    provenance = payload["material_provenance_coverage"]
    ambiguous = payload["ambiguous_requirement_matching"]
    missing = payload["missing_input_diagnostics"]
    domain_coverage = payload["application_domain_coverage"]
    material_template = payload["material_template_cross_checks"]
    domain_benchmarks = payload["application_domain_benchmarks"]
    maturity = payload["validation_maturity_summary"]
    preview_boundaries = payload["preview_boundary_summary"]
    lines.extend(
        [
            "",
            "## Material Provenance Coverage",
            "",
            f"- material_count: `{provenance['material_count']}`",
            f"- materials_with_provenance: `{provenance['materials_with_provenance']}`",
            f"- materials_requiring_user_verification: `{provenance['materials_requiring_user_verification']}`",
            f"- production_grade_optical_constants_claimed: `{provenance['production_grade_optical_constants_claimed']}`",
            "",
            "## Ambiguous Requirement Matching",
            "",
            f"- available: `{ambiguous['available']}`",
            f"- deterministic: `{ambiguous['deterministic']}`",
            f"- no_external_llm_used: `{ambiguous['no_external_llm_used']}`",
            f"- covered_cases: `{', '.join(ambiguous['covered_cases'])}`",
            "",
            "## Missing-input Diagnostics",
            "",
            f"- available: `{missing['available']}`",
            f"- critical_optional_split: `{missing['critical_optional_split']}`",
            f"- safe_to_preview_default: `{missing['safe_to_preview_default']}`",
            f"- safe_to_run_solver_default: `{missing['safe_to_run_solver_default']}`",
            "",
            "## Application-Domain Coverage",
            "",
            f"- domain_count: `{domain_coverage['domain_count']}`",
            f"- covered_domains: `{', '.join(domain_coverage['covered_domains'])}`",
            f"- partial_domains: `{', '.join(domain_coverage['partial_domains']) or 'none'}`",
            f"- failed_domains: `{', '.join(domain_coverage['failed_domains']) or 'none'}`",
            f"- preview_only: `{domain_coverage['preview_only']}`",
            "",
            "## Material-Template Cross-Checks",
            "",
            f"- total: `{material_template['total']}`",
            f"- pass_count: `{material_template['pass_count']}`",
            f"- warning_count: `{material_template['warning_count']}`",
            f"- fail_count: `{material_template['fail_count']}`",
            "",
            "| Domain | Status | Tool status | Templates | Materials | Questions |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in material_template["cross_checks"]:
        lines.append(
            "| {domain_id} | {status} | {expected_tool_status} | {template_coverage} | "
            "{material_suitability_coverage} | {missing_input_questions_present} |".format(**item)
        )

    lines.extend(
        [
            "",
            "## Application-Domain Benchmarks",
            "",
            f"- scenario_count: `{domain_benchmarks['scenario_count']}`",
            f"- pass_count: `{domain_benchmarks['pass_count']}`",
            f"- warn_count: `{domain_benchmarks['warn_count']}`",
            f"- fail_count: `{domain_benchmarks['fail_count']}`",
            f"- positive_count: `{domain_benchmarks['positive_count']}`",
            f"- ambiguous_count: `{domain_benchmarks['ambiguous_count']}`",
            f"- underconstrained_count: `{domain_benchmarks['underconstrained_count']}`",
            f"- unsupported_count: `{domain_benchmarks['unsupported_count']}`",
            f"- preview_only: `{domain_benchmarks['preview_only']}`",
            "",
            "## Validation Maturity Summary",
            "",
            f"- record_count: `{maturity['summary']['record_count']}`",
            f"- calculator_maturity_level: `{maturity['summary']['calculator_maturity_level']}`",
            f"- application_domain_maturity_level: `{maturity['summary']['application_domain_maturity_level']}`",
            f"- adapter_source_monitor_maturity_level: `{maturity['summary']['adapter_source_monitor_maturity_level']}`",
            f"- material_maturity_level: `{maturity['summary']['material_maturity_level']}`",
            f"- validation_claim_audit_available: `{payload['validation_claim_audit_available']}`",
            "",
            "## Preview Boundary Summary",
            "",
            f"- calculators: `{preview_boundaries['calculators']}`",
            f"- materials: `{preview_boundaries['materials']}`",
            f"- adapters: `{preview_boundaries['adapters']}`",
            f"- application_domains: `{preview_boundaries['application_domains']}`",
        ]
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
        "## Maintainer Evidence Pack",
        "",
        "For a review-oriented bundle that combines sub-agent reality, tool-call",
        "reality, calculator evidence, design-case cross-checks, source/monitor",
        "diagnostics, and adapter-native golden coverage, run:",
        "",
        "```bash",
        "python scripts/generate_backend_evidence_pack.py --json-out /tmp/osa-backend-evidence-pack.json --markdown-out /tmp/osa-backend-evidence-pack.md",
        "```",
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
    print(
        "material_provenance_coverage="
        f"{payload['material_provenance_coverage']['materials_with_provenance']}/"
        f"{payload['material_provenance_coverage']['material_count']}"
    )
    print(
        "ambiguous_requirement_matching="
        f"{payload['ambiguous_requirement_matching']['available']}"
    )
    print(
        "application_domain_coverage="
        f"{payload['application_domain_coverage']['domain_count']}"
    )
    print(
        "material_template_cross_checks="
        f"{payload['material_template_cross_checks']['pass_count']} pass/"
        f"{payload['material_template_cross_checks']['warning_count']} warning/"
        f"{payload['material_template_cross_checks']['fail_count']} fail"
    )
    print(
        "application_domain_benchmarks="
        f"{payload['application_domain_benchmarks']['pass_count']} pass/"
        f"{payload['application_domain_benchmarks']['warn_count']} warn/"
        f"{payload['application_domain_benchmarks']['fail_count']} fail"
    )
    print(f"requirements_templates={len(payload['requirements_templates'])}")
    print(
        "validation_maturity_records="
        f"{payload['validation_maturity_summary']['summary']['record_count']}"
    )
    print("validation_claim_audit_available=True")
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
