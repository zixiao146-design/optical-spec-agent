"""Cross-check bundled optical design cases against backend task sessions."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from optical_spec_agent.agents.task_session import build_agent_task_session

from .registry import EXAMPLES_ROOT, get_optical_design_example, list_optical_design_examples
from .requirements import list_requirement_templates, match_goal_to_template


CrossCheckStatus = Literal["pass", "warning", "fail"]


class DesignCaseSafetyFlags(BaseModel):
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class DesignCaseCrossCheck(BaseModel):
    example_id: str
    status: CrossCheckStatus
    spec_exists: bool
    agent_trace_exists: bool
    calculator_called: bool
    expected_calculator: str | None = None
    material_suggestions: list[str] = Field(default_factory=list)
    adapter_recommendation: str = ""
    tool_call_ledger_entries: list[str] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    safety_flags: DesignCaseSafetyFlags = Field(default_factory=DesignCaseSafetyFlags)


class RequirementTemplateCrossCheck(BaseModel):
    template_id: str
    status: CrossCheckStatus
    design_case_id: str | None = None
    requirement_files_exist: bool
    goal_en_matches_template: bool
    goal_zh_matches_template: bool
    expected_tool_calls: list[str] = Field(default_factory=list)
    missing_tool_calls: list[str] = Field(default_factory=list)
    calculator_expectations_met: bool
    diagnostics: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    safety_flags: DesignCaseSafetyFlags = Field(default_factory=DesignCaseSafetyFlags)


class DesignCaseCrossChecksResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    cross_checks: list[DesignCaseCrossCheck] = Field(default_factory=list)
    requirement_template_checks: list[RequirementTemplateCrossCheck] = Field(default_factory=list)
    summary: dict[str, int] = Field(default_factory=dict)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
    recommended_next_actions: list[str] = Field(default_factory=list)


EXPECTED_CALCULATORS: dict[str, str | None] = {
    "thin_film_coating": "optics.thin_film",
    "waveguide_mode": "optics.waveguide",
    "lens_raytrace_preview": "optics.paraxial",
    "nanoparticle_plasmonics": None,
    "photonic_crystal_band": None,
    "dielectric_metasurface_preview": None,
}


def cross_check_design_case(example_id: str) -> DesignCaseCrossCheck:
    """Cross-check one local example without running solvers or external LLMs."""

    example_dir = EXAMPLES_ROOT / example_id
    spec_exists = (example_dir / "spec.json").exists()
    agent_trace_exists = (example_dir / "expected_agent_trace.json").exists()
    expected_calculator = EXPECTED_CALCULATORS.get(example_id)
    diagnostics: list[str] = []
    warnings: list[str] = []

    try:
        detail = get_optical_design_example(example_id)
        session = build_agent_task_session(
            detail.summary.design_goal,
            example_id=example_id,
        )
    except Exception as exc:  # noqa: BLE001 - report the malformed case instead of hiding it.
        return DesignCaseCrossCheck(
            example_id=example_id,
            status="fail",
            spec_exists=spec_exists,
            agent_trace_exists=agent_trace_exists,
            calculator_called=False,
            expected_calculator=expected_calculator,
            diagnostics=[f"Could not build local task session: {exc}"],
        )

    ledger_names = [entry.tool_name for entry in session.tool_call_ledger]
    executed_ledger_names = [
        entry.tool_name for entry in session.tool_call_ledger if entry.executed
    ]
    calculator_called = any(name.startswith("optics.") for name in executed_ledger_names)
    status: CrossCheckStatus = "pass"

    if not spec_exists:
        status = "fail"
        diagnostics.append("spec.json is missing.")
    if not agent_trace_exists:
        status = "fail"
        diagnostics.append("expected_agent_trace.json is missing.")
    if expected_calculator is not None:
        if not any(name.startswith(expected_calculator) for name in executed_ledger_names):
            status = "fail"
            diagnostics.append(f"Expected calculator was not executed: {expected_calculator}.")
        else:
            diagnostics.append(f"Expected calculator executed: {expected_calculator}.")
    else:
        diagnostics.append("No scalar calculator is required for this example category.")
        if calculator_called:
            warnings.append("A calculator ran even though this case only requires material/adapter trace.")

    if "material_catalog.suggest" not in executed_ledger_names:
        status = "fail"
        diagnostics.append("Material catalog suggestion did not execute.")
    if "agent_trace.build" not in executed_ledger_names:
        status = "fail"
        diagnostics.append("Agent trace builder did not execute.")
    if not session.agent_trace.adapter_recommendation:
        status = "fail"
        diagnostics.append("Adapter recommendation is missing.")

    return DesignCaseCrossCheck(
        example_id=example_id,
        status=status,
        spec_exists=spec_exists,
        agent_trace_exists=agent_trace_exists,
        calculator_called=calculator_called,
        expected_calculator=expected_calculator,
        material_suggestions=session.agent_trace.material_suggestions,
        adapter_recommendation=session.agent_trace.adapter_recommendation,
        tool_call_ledger_entries=ledger_names,
        diagnostics=diagnostics,
        warnings=warnings,
        safety_flags=DesignCaseSafetyFlags(
            external_solver_executed=session.external_solver_executed,
            external_llm_required=session.external_llm_required,
            proprietary_solver_required=session.proprietary_solver_required,
            production_grade_validation_claimed=session.production_grade_validation_claimed,
            formal_convergence_proof_claimed=session.formal_convergence_proof_claimed,
        ),
    )


def cross_check_all_design_cases() -> DesignCaseCrossChecksResponse:
    """Cross-check every registered local optical design example."""

    checks = [
        cross_check_design_case(summary.example_id)
        for summary in list_optical_design_examples()
    ]
    requirement_checks = cross_check_all_requirement_templates()
    all_statuses = [check.status for check in checks] + [
        check.status for check in requirement_checks
    ]
    summary = {
        "total": len(checks),
        "pass": sum(1 for check in checks if check.status == "pass"),
        "warning": sum(1 for check in checks if check.status == "warning"),
        "fail": sum(1 for check in checks if check.status == "fail"),
        "requirement_templates_total": len(requirement_checks),
        "requirement_templates_pass": sum(
            1 for check in requirement_checks if check.status == "pass"
        ),
        "requirement_templates_warning": sum(
            1 for check in requirement_checks if check.status == "warning"
        ),
        "requirement_templates_fail": sum(
            1 for check in requirement_checks if check.status == "fail"
        ),
    }
    status = "ok" if "fail" not in all_statuses else "needs_review"
    return DesignCaseCrossChecksResponse(
        status=status,
        cross_checks=checks,
        requirement_template_checks=requirement_checks,
        summary=summary,
        recommended_next_actions=[
            "Review warning/fail diagnostics before public demo use.",
            "Use calculator-backed cases to inspect tool_call_ledger evidence.",
            "Use requirement_template_checks to verify natural-language goal matching.",
            "Keep all cross-check results labeled as preview/design-assist.",
        ],
    )


def cross_check_requirement_template(template_id: str) -> RequirementTemplateCrossCheck:
    template = next(
        item for item in list_requirement_templates() if item.template_id == template_id
    )
    requirement_dir = EXAMPLES_ROOT.parent / "design_requirements" / template.template_id
    required_files = [
        requirement_dir / "requirement.json",
        requirement_dir / "goal_en.txt",
        requirement_dir / "goal_zh.txt",
        requirement_dir / "expected_tool_calls.json",
        requirement_dir / "README.md",
    ]
    files_exist = all(path.exists() for path in required_files)
    diagnostics: list[str] = []
    warnings: list[str] = []
    status: CrossCheckStatus = "pass"

    match_en = match_goal_to_template(template.natural_language_goal_en)
    match_zh = match_goal_to_template(template.natural_language_goal_zh)
    goal_en_matches = match_en.matched_template_id == template.template_id
    goal_zh_matches = match_zh.matched_template_id == template.template_id

    if not files_exist:
        status = "fail"
        diagnostics.append("One or more design requirement files are missing.")
    if not goal_en_matches:
        status = "fail"
        diagnostics.append("English goal does not match its template.")
    if not goal_zh_matches:
        status = "fail"
        diagnostics.append("Chinese goal does not match its template.")

    session = build_agent_task_session(
        template.natural_language_goal_en,
        example_id=template.design_case_id,
    )
    ledger_names = [entry.tool_name for entry in session.tool_call_ledger]
    executed_ledger_names = [
        entry.tool_name for entry in session.tool_call_ledger if entry.executed
    ]
    missing_tool_calls = [
        tool_name
        for tool_name in template.expected_tool_calls
        if tool_name not in ledger_names
    ]
    for tool_name in template.expected_tool_calls:
        if tool_name.startswith("optics.") and not any(
            executed.startswith(tool_name) for executed in executed_ledger_names
        ):
            missing_tool_calls.append(tool_name)
    if missing_tool_calls:
        status = "fail"
        diagnostics.append(f"Expected tool calls missing: {sorted(set(missing_tool_calls))}")

    calculator_expectations_met = True
    for calculator in template.expected_calculators:
        if not any(entry.startswith(calculator) for entry in executed_ledger_names):
            calculator_expectations_met = False
    if not calculator_expectations_met:
        status = "fail"
        diagnostics.append("Expected calculator call was not executed.")
    if not template.expected_calculators:
        warnings.append("Template uses material/adapter/workflow trace without scalar calculator.")

    return RequirementTemplateCrossCheck(
        template_id=template.template_id,
        status=status,
        design_case_id=template.design_case_id,
        requirement_files_exist=files_exist,
        goal_en_matches_template=goal_en_matches,
        goal_zh_matches_template=goal_zh_matches,
        expected_tool_calls=template.expected_tool_calls,
        missing_tool_calls=sorted(set(missing_tool_calls)),
        calculator_expectations_met=calculator_expectations_met,
        diagnostics=diagnostics,
        warnings=warnings,
        safety_flags=DesignCaseSafetyFlags(
            external_solver_executed=session.external_solver_executed,
            external_llm_required=session.external_llm_required,
            proprietary_solver_required=session.proprietary_solver_required,
            production_grade_validation_claimed=session.production_grade_validation_claimed,
            formal_convergence_proof_claimed=session.formal_convergence_proof_claimed,
        ),
    )


def cross_check_all_requirement_templates() -> list[RequirementTemplateCrossCheck]:
    return [
        cross_check_requirement_template(template.template_id)
        for template in list_requirement_templates()
    ]


def required_files_for_example(example_id: str) -> list[Path]:
    """Return the local files a design case must have."""

    example_dir = EXAMPLES_ROOT / example_id
    return [
        example_dir / "spec.json",
        example_dir / "README.md",
        example_dir / "expected_agent_trace.json",
    ]
