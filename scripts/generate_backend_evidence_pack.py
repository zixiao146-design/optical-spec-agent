#!/usr/bin/env python3
"""Generate the maintainer backend evidence review pack.

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

from optical_spec_agent.agents.evidence_pack import (  # noqa: E402
    BackendEvidencePack,
    generate_backend_evidence_pack,
)


def _write_json(pack: BackendEvidencePack, path: Path) -> None:
    path.write_text(
        json.dumps(pack.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _write_markdown(pack: BackendEvidencePack, path: Path) -> None:
    payload = pack.model_dump(mode="json")
    lines = [
        "# Backend Evidence Review Pack",
        "",
        "This generated maintainer artifact summarizes what the local backend proves",
        "today. It is preview/design-assist evidence, not production-grade physical",
        "validation, and it does not claim a formal convergence proof.",
        "No production-grade physical validation is claimed.",
        "",
        "## Package and release status",
        "",
        f"- current_public_prerelease: `{payload['package_and_release_status']['current_public_prerelease']}`",
        f"- main_development_version: `{payload['package_and_release_status']['main_development_version']}`",
        f"- package_version: `{payload['package_and_release_status']['package_version']}`",
        f"- PyPI published: `{payload['package_and_release_status']['pypi_published']}`",
        f"- TestPyPI verified only for: `{payload['package_and_release_status']['testpypi_verified_only_for']}`",
        f"- tag/release actions: `{payload['package_and_release_status']['tag_release_actions']}`",
        "",
        "## Sub-agent reality",
        "",
        "| Role | Exists | Importable or trace role | Executed | Output summary | Evidence refs |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in payload["sub_agent_reality"]:
        lines.append(
            "| {role_name} | {role_exists} | {importable_or_trace_role} | "
            "{executed_in_sample_session} | {output_summary_available} | "
            "{evidence_refs_available} |".format(**item)
        )

    tools = payload["tool_call_reality"]
    lines.extend(
        [
            "",
            "## Tool-call reality",
            "",
            f"- internal_tools_available: `{', '.join(tools['internal_tools_available'])}`",
            f"- internal_tools_executed: `{', '.join(tools['internal_tools_executed'])}`",
            f"- calculator_tools_executed: `{', '.join(tools['calculator_tools_executed']) or 'none'}`",
            f"- blocked_external_actions: `{', '.join(tools['blocked_external_actions'])}`",
            "",
            "## Optical calculators",
            "",
            "| Calculator | Implemented | Quality | Reference cases | Failure modes |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["optical_calculators"]:
        lines.append(
            "| {calculator_name} | {implemented} | {quality_level} | {refs} | {failures} |".format(
                refs=", ".join(item["sanity_reference_cases"]),
                failures=", ".join(item["failure_modes"]),
                **item,
            )
        )

    provenance = payload["material_provenance_coverage"]
    ambiguous = payload["ambiguous_requirement_matching"]
    missing = payload["missing_input_diagnostics"]
    domain_coverage = payload["application_domain_coverage"]
    material_template = payload["material_template_cross_checks"]
    domain_benchmarks = payload["application_domain_benchmarks"]
    lines.extend(
        [
            "",
            "## Material provenance coverage",
            "",
            f"- material_count: `{provenance['material_count']}`",
            f"- materials_with_provenance: `{provenance['materials_with_provenance']}`",
            f"- materials_requiring_user_verification: `{provenance['materials_requiring_user_verification']}`",
            f"- production_grade_optical_constants_database: `{provenance['production_grade_optical_constants_database']}`",
            f"- no_external_material_database_lookup: `{provenance['no_external_material_database_lookup']}`",
            "",
            "## Ambiguous requirement matching",
            "",
            f"- available: `{ambiguous['available']}`",
            f"- deterministic: `{ambiguous['deterministic']}`",
            f"- no_external_llm_used: `{ambiguous['no_external_llm_used']}`",
            f"- covered_cases: `{', '.join(ambiguous['covered_cases'])}`",
            f"- ambiguous_goals_generate_questions: `{ambiguous['ambiguous_goals_generate_questions']}`",
            "",
            "## Missing-input diagnostics",
            "",
            f"- available: `{missing['available']}`",
            f"- critical_optional_split: `{missing['critical_optional_split']}`",
            f"- safe_to_preview_default: `{missing['safe_to_preview_default']}`",
            f"- safe_to_run_solver_default: `{missing['safe_to_run_solver_default']}`",
            "",
            "## Application-domain coverage",
            "",
            f"- domain_count: `{domain_coverage['domain_count']}`",
            f"- covered_domains: `{', '.join(domain_coverage['covered_domains'])}`",
            f"- partial_domains: `{', '.join(domain_coverage['partial_domains']) or 'none'}`",
            f"- failed_domains: `{', '.join(domain_coverage['failed_domains']) or 'none'}`",
            f"- preview_design_assist_only: `{domain_coverage['preview_design_assist_only']}`",
            "",
            "## Material-template cross-checks",
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
            "## Application-domain benchmarks",
            "",
            f"- scenario_count: `{domain_benchmarks['scenario_count']}`",
            f"- pass_count: `{domain_benchmarks['pass_count']}`",
            f"- warn_count: `{domain_benchmarks['warn_count']}`",
            f"- fail_count: `{domain_benchmarks['fail_count']}`",
            f"- positive_count: `{domain_benchmarks['positive_count']}`",
            f"- ambiguous_count: `{domain_benchmarks['ambiguous_count']}`",
            f"- underconstrained_count: `{domain_benchmarks['underconstrained_count']}`",
            f"- unsupported_count: `{domain_benchmarks['unsupported_count']}`",
            f"- preview_design_assist_only: `{domain_benchmarks['preview_design_assist_only']}`",
        ]
    )

    lines.extend(
        [
            "",
            "## Design-case cross-checks",
            "",
            "| Example | Status | Expected calculator | Calculator called | Adapter |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["design_case_cross_checks"]:
        lines.append(
            "| {example_id} | {status} | {expected_calculator} | {calculator_called} | "
            "{adapter_recommendation} |".format(**item)
        )

    diagnostics = payload["source_monitor_observable_diagnostics"]
    lines.extend(
        [
            "",
            "## Source / monitor / observable diagnostics",
            "",
            f"- source_monitor_inference_available: `{diagnostics['source_monitor_inference_available']}`",
            f"- source_monitor_inference_executed: `{diagnostics['source_monitor_inference_executed']}`",
            f"- missing_input_diagnostics_available: `{diagnostics['missing_input_diagnostics_available']}`",
            f"- missing_input_diagnostics_executed: `{diagnostics['missing_input_diagnostics_executed']}`",
            f"- observable_taxonomy_available: `{diagnostics['observable_taxonomy_available']}`",
            f"- observable_diagnostics_executed: `{diagnostics['observable_diagnostics_executed']}`",
            f"- adapter_native_mapping_available: `{diagnostics['adapter_native_mapping_available']}`",
            f"- adapter_native_mapping_executed: `{diagnostics['adapter_native_mapping_executed']}`",
            f"- monitor_metadata: `{diagnostics['monitor_metadata']}`",
            "",
            "## Adapter-native golden coverage",
            "",
            "| Adapter | Case | Metadata match | Fragment match | Safety match | Solver required | Solver executed |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["adapter_native_golden_coverage"]["cases"]:
        lines.append(
            "| {adapter_name} | {case_id} | {metadata_match} | {fragment_match} | "
            "{safety_match} | {solver_required_for_real_result} | {solver_executed} |".format(
                **item
            )
        )

    lines.extend(
        [
            "",
            "## Blocked or deferred capabilities",
            "",
            "| Capability | Default allowed | Executed | Reason |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in payload["blocked_or_deferred_capabilities"]:
        lines.append(
            "| {capability} | {default_allowed} | {executed} | {reason} |".format(**item)
        )

    lines.extend(
        [
            "",
            "## Maintainer review questions",
            "",
        ]
    )
    for question in payload["maintainer_review_questions"]:
        lines.append(f"- {question}")

    lines.extend(
        [
            "",
            "## Safety markers",
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


def _print_summary(pack: BackendEvidencePack) -> None:
    payload: dict[str, Any] = pack.model_dump(mode="json")
    print("Backend evidence review pack")
    print(
        "current_public_prerelease="
        f"{payload['package_and_release_status']['current_public_prerelease']}"
    )
    print(
        "main_development_version="
        f"{payload['package_and_release_status']['main_development_version']}"
    )
    print(f"sub_agent_reality={len(payload['sub_agent_reality'])}")
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
    print(f"design_case_cross_checks={len(payload['design_case_cross_checks'])}")
    print(
        "adapter_native_golden_coverage="
        f"{payload['adapter_native_golden_coverage']['status']}"
    )
    print(
        "blocked_or_deferred_capabilities="
        f"{len(payload['blocked_or_deferred_capabilities'])}"
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

    pack = generate_backend_evidence_pack()
    if args.json_out:
        _write_json(pack, args.json_out)
    if args.markdown_out:
        _write_markdown(pack, args.markdown_out)
    _print_summary(pack)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
