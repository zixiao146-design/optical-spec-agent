"""Cross-check bundled optical design cases against backend task sessions."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from optical_spec_agent.agents.task_session import build_agent_task_session

from .registry import EXAMPLES_ROOT, get_optical_design_example, list_optical_design_examples


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


class DesignCaseCrossChecksResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    cross_checks: list[DesignCaseCrossCheck] = Field(default_factory=list)
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
    summary = {
        "total": len(checks),
        "pass": sum(1 for check in checks if check.status == "pass"),
        "warning": sum(1 for check in checks if check.status == "warning"),
        "fail": sum(1 for check in checks if check.status == "fail"),
    }
    status = "ok" if summary["fail"] == 0 else "needs_review"
    return DesignCaseCrossChecksResponse(
        status=status,
        cross_checks=checks,
        summary=summary,
        recommended_next_actions=[
            "Review warning/fail diagnostics before public demo use.",
            "Use calculator-backed cases to inspect tool_call_ledger evidence.",
            "Keep all cross-check results labeled as preview/design-assist.",
        ],
    )


def required_files_for_example(example_id: str) -> list[Path]:
    """Return the local files a design case must have."""

    example_dir = EXAMPLES_ROOT / example_id
    return [
        example_dir / "spec.json",
        example_dir / "README.md",
        example_dir / "expected_agent_trace.json",
    ]
