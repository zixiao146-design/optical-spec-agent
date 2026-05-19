"""Maintainer-facing backend evidence pack aggregation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from optical_spec_agent.agents.capability_report import (
    BackendCapabilityReport,
    generate_backend_capability_report,
)


EVIDENCE_PACK_SECTIONS = [
    "Package and release status",
    "Sub-agent reality",
    "Tool-call reality",
    "Optical calculators",
    "Material provenance coverage",
    "Ambiguous requirement matching",
    "Missing-input diagnostics",
    "Application-domain coverage",
    "Material-template cross-checks",
    "Design-case cross-checks",
    "Source / monitor / observable diagnostics",
    "Adapter-native golden coverage",
    "Blocked or deferred capabilities",
    "Maintainer review questions",
]


class BackendEvidencePack(BaseModel):
    """Structured backend evidence pack for maintainer review."""

    api_contract_version: str = "0.1"
    status: str = "ok"
    evidence_pack_available: bool = True
    preview_design_assist_only: bool = True
    package_and_release_status: dict[str, Any]
    sub_agent_reality: list[dict[str, Any]] = Field(default_factory=list)
    tool_call_reality: dict[str, Any]
    optical_calculators: list[dict[str, Any]] = Field(default_factory=list)
    material_provenance_coverage: dict[str, Any] = Field(default_factory=dict)
    ambiguous_requirement_matching: dict[str, Any] = Field(default_factory=dict)
    missing_input_diagnostics: dict[str, Any] = Field(default_factory=dict)
    application_domain_coverage: dict[str, Any] = Field(default_factory=dict)
    material_template_cross_checks: dict[str, Any] = Field(default_factory=dict)
    design_case_cross_checks: list[dict[str, Any]] = Field(default_factory=list)
    source_monitor_observable_diagnostics: dict[str, Any]
    adapter_native_golden_coverage: dict[str, Any]
    blocked_or_deferred_capabilities: list[dict[str, Any]] = Field(default_factory=list)
    maintainer_review_questions: list[str] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


def generate_backend_evidence_pack(
    capability_report: BackendCapabilityReport | None = None,
) -> BackendEvidencePack:
    """Build a local-only backend evidence pack from existing reports.

    This function reuses the backend capability report, design case
    cross-checks, tool-call ledger evidence, and adapter-native golden coverage.
    It does not execute external solvers, call LLMs, access the network, upload,
    tag, or release.
    """

    report = capability_report or generate_backend_capability_report()
    payload = report.model_dump(mode="json")
    package = payload["package"]
    internal_tools = payload["internal_tools"]
    calculators = payload["optical_calculators"]
    golden = payload["adapter_native_golden_coverage"]
    blocked_actions = payload["blocked_external_actions"]
    source_monitor_tools = {
        item["tool_name"]: item
        for item in internal_tools
        if item["tool_name"]
        in {
            "source_monitor_inference",
            "missing_input_diagnostics",
            "observable_diagnostics",
            "adapter_native_mapping",
        }
    }
    return BackendEvidencePack(
        status=payload["status"],
        package_and_release_status={
            "package_version": package["package_version"],
            "current_public_prerelease": package["current_public_prerelease"],
            "main_development_version": package["main_development_version"],
            "pypi_published": package["pypi_published"],
            "testpypi_verified_only_for": package["testpypi_verified_for"],
            "tag_release_actions": "none",
            "upload_actions": "none",
        },
        sub_agent_reality=[
            {
                "role_name": item["role_name"],
                "role_exists": item["role_exists_in_trace"],
                "importable_or_trace_role": item["importable_module"]
                or item["role_exists_in_trace"],
                "executed_in_sample_session": item["executed_in_sample_session"],
                "output_summary_available": item["output_summary_available"],
                "evidence_refs_available": item["evidence_refs_available"],
            }
            for item in payload["sub_agents"]
        ],
        tool_call_reality={
            "internal_tools_executed": [
                item["tool_name"] for item in internal_tools if item["executed_in_sample"]
            ],
            "internal_tools_available": [
                item["tool_name"] for item in internal_tools if item["callable"]
            ],
            "calculator_tools_executed": [
                item["tool_name"]
                for item in internal_tools
                if item["tool_name"] == "optical_calculators"
                and item["executed_in_sample"]
            ],
            "blocked_external_actions": [
                item["action_name"] for item in blocked_actions if item["executed"] is False
            ],
        },
        optical_calculators=[
            {
                "calculator_name": item["calculator_name"],
                "implemented": item["implemented"],
                "sanity_reference_cases": item["reference_cases"],
                "failure_modes": item["failure_modes"],
                "api_endpoints": item["api_endpoints"],
                "quality_level": item["quality_level"],
                "preview_design_assist": True,
                "production_grade_validation_claimed": item[
                    "production_grade_validation_claimed"
                ],
                "formal_convergence_proof_claimed": item[
                    "formal_convergence_proof_claimed"
                ],
            }
            for item in calculators
        ],
        material_provenance_coverage={
            **payload["material_provenance_coverage"],
            "preview_design_assist_only": True,
            "no_external_material_database_lookup": True,
            "production_grade_optical_constants_database": False,
        },
        ambiguous_requirement_matching={
            **payload["ambiguous_requirement_matching"],
            "ambiguous_goals_generate_questions": True,
            "unsafe_default_solver_action": False,
        },
        missing_input_diagnostics={
            **payload["missing_input_diagnostics"],
            "safe_to_run_solver_default": False,
        },
        application_domain_coverage={
            **payload["application_domain_coverage"],
            "preview_design_assist_only": True,
            "no_external_solver_execution": True,
        },
        material_template_cross_checks={
            **payload["material_template_cross_checks"],
            "preview_design_assist_only": True,
            "no_production_grade_claim": True,
        },
        design_case_cross_checks=[
            {
                "example_id": item["example_id"],
                "status": item["status"],
                "expected_calculator": item["expected_calculator"],
                "calculator_called": item["calculator_called"],
                "material_suggestions": item["material_suggestions"],
                "adapter_recommendation": item["adapter_recommendation"],
                "tool_call_ledger_entries": item["tool_call_ledger_entries"],
                "diagnostics": item["diagnostics"],
            }
            for item in payload["design_case_cross_checks"]
        ],
        source_monitor_observable_diagnostics={
            "source_monitor_inference_available": source_monitor_tools[
                "source_monitor_inference"
            ]["callable"],
            "source_monitor_inference_executed": source_monitor_tools[
                "source_monitor_inference"
            ]["executed_in_sample"],
            "missing_input_diagnostics_available": source_monitor_tools[
                "missing_input_diagnostics"
            ]["callable"],
            "missing_input_diagnostics_executed": source_monitor_tools[
                "missing_input_diagnostics"
            ]["executed_in_sample"],
            "observable_taxonomy_available": source_monitor_tools[
                "observable_diagnostics"
            ]["callable"],
            "observable_diagnostics_executed": source_monitor_tools[
                "observable_diagnostics"
            ]["executed_in_sample"],
            "adapter_native_mapping_available": source_monitor_tools[
                "adapter_native_mapping"
            ]["callable"],
            "adapter_native_mapping_executed": source_monitor_tools[
                "adapter_native_mapping"
            ]["executed_in_sample"],
            "monitor_metadata": "preview-only; no real solver monitor result is claimed.",
        },
        adapter_native_golden_coverage={
            "status": golden["status"],
            "adapters_covered": golden["adapters_covered"],
            "missing_adapters": golden["missing_adapters"],
            "cases": [
                {
                    "adapter_name": item["adapter_name"],
                    "case_id": item["case_id"],
                    "metadata_match": item["coverage_status"] == "pass",
                    "fragment_match": item["coverage_status"] == "pass",
                    "safety_match": item["external_solver_executed"] is False
                    and item["production_grade_validation_claimed"] is False
                    and item["formal_convergence_proof_claimed"] is False,
                    "solver_required_for_real_result": item[
                        "requires_solver_for_real_result"
                    ],
                    "solver_executed": item["external_solver_executed"],
                    "preview_only": item["preview_only"],
                }
                for item in golden["coverage_items"]
            ],
        },
        blocked_or_deferred_capabilities=[
            {
                "capability": item["action_name"],
                "default_allowed": item["default_allowed"],
                "executed": item["executed"],
                "reason": item["reason"],
            }
            for item in blocked_actions
        ]
        + [
            {
                "capability": "elmer_level_3",
                "default_allowed": False,
                "executed": False,
                "reason": "Elmer remains Level 2 + Level-3-ready; Level 3 is not claimed.",
            },
            {
                "capability": "production_grade_validation",
                "default_allowed": False,
                "executed": False,
                "reason": "Calculator and adapter evidence is preview/design-assist only.",
            },
            {
                "capability": "formal_convergence_proof",
                "default_allowed": False,
                "executed": False,
                "reason": "No formal convergence proof is claimed.",
            },
        ],
        maintainer_review_questions=[
            "Is backend evidence sufficient for continued v0.9.0rc8.dev0 readiness work?",
            "Is PyPI still deferred?",
            "Should the frontend display backend evidence next?",
            "Which calculator or optical design domain should deepen next?",
        ],
    )
