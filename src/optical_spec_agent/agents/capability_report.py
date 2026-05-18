"""Backend capability report for local Agent Studio reality checks."""

from __future__ import annotations

import importlib
import importlib.util
from typing import Any

from pydantic import BaseModel, Field

from optical_spec_agent import __version__
from optical_spec_agent.adapters.registry import dispatch_adapter
from optical_spec_agent.agents.orchestrator import build_agent_trace
from optical_spec_agent.agents.roles import AGENT_ROLES
from optical_spec_agent.agents.task_session import build_agent_task_session
from optical_spec_agent.examples.cross_check import (
    DesignCaseCrossCheck,
    cross_check_all_design_cases,
)
from optical_spec_agent.examples.registry import list_optical_design_examples
from optical_spec_agent.examples.requirements import (
    list_requirement_templates,
    match_goal_to_template,
)
from optical_spec_agent.materials.catalog import suggest_materials_for_application
from optical_spec_agent.optical_language import (
    diagnose_missing_inputs,
    infer_source_monitor_from_goal,
)
from optical_spec_agent.optics import (
    analyze_two_lens_relay,
    calculate_thin_film_spectrum,
    gaussian_beam_parameters,
    slab_waveguide_sweep,
)
from optical_spec_agent.workflows import plan_workflow


class PackageCapability(BaseModel):
    package_version: str
    current_public_prerelease: str = "v0.9.0rc6"
    main_development_version: str = "0.9.0rc7.dev0"
    pypi_published: bool = False
    testpypi_verified_for: str = "0.9.0rc6.dev0"


class SubAgentCapability(BaseModel):
    role_name: str
    importable_module: bool
    role_exists_in_trace: bool
    executed_in_sample_session: bool
    output_summary_available: bool
    evidence_refs_available: bool
    notes: list[str] = Field(default_factory=list)


class InternalToolCapabilityReport(BaseModel):
    tool_name: str
    importable: bool
    callable: bool
    executed_in_sample: bool
    notes: list[str] = Field(default_factory=list)


class OpticalCalculatorCapability(BaseModel):
    calculator_name: str
    implemented: bool
    api_endpoints: list[str] = Field(default_factory=list)
    reference_cases: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
    quality_level: str = "sanity_checked_preview"
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class BlockedExternalAction(BaseModel):
    action_name: str
    default_allowed: bool = False
    executed: bool = False
    reason: str


class RequirementTemplateCapability(BaseModel):
    template_id: str
    goal_en_present: bool
    goal_zh_present: bool
    matched_by_heuristic: bool
    expected_tools: list[str] = Field(default_factory=list)
    cross_check_status: str
    preview_only: bool = True


class BackendCapabilityReport(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    package: PackageCapability
    sub_agents: list[SubAgentCapability] = Field(default_factory=list)
    internal_tools: list[InternalToolCapabilityReport] = Field(default_factory=list)
    optical_calculators: list[OpticalCalculatorCapability] = Field(default_factory=list)
    requirements_templates: list[RequirementTemplateCapability] = Field(default_factory=list)
    design_case_cross_checks: list[DesignCaseCrossCheck] = Field(default_factory=list)
    blocked_external_actions: list[BlockedExternalAction] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
    recommended_next_actions: list[str] = Field(default_factory=list)


def generate_backend_capability_report() -> BackendCapabilityReport:
    """Generate a local-only backend capability report.

    The report builds deterministic sample sessions and inspects local Python
    capabilities only. It does not execute external solvers, call LLMs, access
    the network, upload, tag, or release.
    """

    sample_session = build_agent_task_session(
        "Create a local preview workflow for silver nanoparticle scattering on a thin film.",
        example_id="nanoparticle_plasmonics",
    )
    calculator_session = build_agent_task_session(
        "Plan a local thin film coating preview with no external solver.",
        example_id="thin_film_coating",
    )
    all_sample_tool_names = {
        entry.tool_name
        for session in (sample_session, calculator_session)
        for entry in session.tool_call_ledger
        if entry.executed
    }
    cross_checks = cross_check_all_design_cases()
    failed = any(check.status == "fail" for check in cross_checks.cross_checks)
    return BackendCapabilityReport(
        status="needs_review" if failed else "ok",
        package=PackageCapability(package_version=__version__),
        sub_agents=_sub_agent_capabilities(sample_session),
        internal_tools=_internal_tool_capabilities(all_sample_tool_names),
        optical_calculators=_optical_calculator_capabilities(),
        requirements_templates=_requirement_template_capabilities(),
        design_case_cross_checks=cross_checks.cross_checks,
        blocked_external_actions=_blocked_external_actions(sample_session),
        recommended_next_actions=[
            "Inspect design_case_cross_checks for any warning/fail status.",
            "Use scripts/audit_sub_agents.py for a concise import/call/execution view.",
            "Use scripts/smoke_backend_capabilities.sh for calculator sanity checks.",
            "Treat calculator outputs as sanity-checked preview/design-assist only.",
        ],
    )


def _sub_agent_capabilities(sample_session: Any) -> list[SubAgentCapability]:
    module_importable = importlib.util.find_spec("optical_spec_agent.agents") is not None
    executed_steps = {step.agent_name: step for step in sample_session.agent_trace.agents}
    return [
        SubAgentCapability(
            role_name=role_name,
            importable_module=module_importable,
            role_exists_in_trace=role_name in executed_steps,
            executed_in_sample_session=role_name in executed_steps,
            output_summary_available=bool(
                executed_steps.get(role_name) and executed_steps[role_name].output_summary
            ),
            evidence_refs_available=bool(
                executed_steps.get(role_name) and executed_steps[role_name].evidence_refs
            ),
            notes=[
                description,
                "Current sub-agents are deterministic backend roles, not separate autonomous packages.",
            ],
        )
        for role_name, description in AGENT_ROLES
    ]


def _internal_tool_capabilities(
    executed_tool_names: set[str],
) -> list[InternalToolCapabilityReport]:
    checks = [
        (
            "material_catalog",
            "optical_spec_agent.materials.catalog",
            suggest_materials_for_application,
            "material_catalog.suggest",
            "Suggests materials from the bundled local preview catalog.",
        ),
        (
            "example_registry",
            "optical_spec_agent.examples.registry",
            list_optical_design_examples,
            "example_registry.load",
            "Loads repo-local optical design examples.",
        ),
        (
            "agent_trace_builder",
            "optical_spec_agent.agents.orchestrator",
            build_agent_trace,
            "agent_trace.build",
            "Builds deterministic eight-role collaboration traces.",
        ),
        (
            "task_session_builder",
            "optical_spec_agent.agents.task_session",
            build_agent_task_session,
            "agent_trace.build",
            "Composes goal, example, trace, ledger, gates, and artifacts.",
        ),
        (
            "adapter_preview_generator",
            "optical_spec_agent.adapters.registry",
            dispatch_adapter,
            "adapter_preview.generate",
            "Generates preview scaffolds only; no solver process is launched.",
        ),
        (
            "workflow_planner",
            "optical_spec_agent.workflows",
            plan_workflow,
            "workflow_plan.preview",
            "Plans local no-execute workflows.",
        ),
        (
            "source_monitor_inference",
            "optical_spec_agent.optical_language",
            infer_source_monitor_from_goal,
            "optical_language.infer_source_monitor",
            "Infers preview source, monitor, observable, and defaults from local heuristics.",
        ),
        (
            "missing_input_diagnostics",
            "optical_spec_agent.optical_language",
            diagnose_missing_inputs,
            "optical_language.diagnose_missing_inputs",
            "Reports missing source/monitor inputs, default assumptions, and solver safety state.",
        ),
        (
            "optical_calculators",
            "optical_spec_agent.optics",
            calculate_thin_film_spectrum,
            "optics.thin_film.spectrum",
            "Runs sanity-checked preview calculators for applicable design cases.",
        ),
    ]
    return [
        InternalToolCapabilityReport(
            tool_name=tool_name,
            importable=_module_importable(module_name),
            callable=callable(function),
            executed_in_sample=ledger_name in executed_tool_names,
            notes=[note],
        )
        for tool_name, module_name, function, ledger_name, note in checks
    ]


def _optical_calculator_capabilities() -> list[OpticalCalculatorCapability]:
    calculators = [
        OpticalCalculatorCapability(
            calculator_name="thin_film",
            implemented=callable(calculate_thin_film_spectrum),
            api_endpoints=[
                "/api/optics/thin-film",
                "/api/optics/thin-film-spectrum",
                "/api/optics/quarter-wave-ar",
            ],
            reference_cases=[
                "thin_film_single_interface_air_glass",
                "thin_film_quarter_wave_ar_550nm",
            ],
            failure_modes=[
                "negative wavelength",
                "zero/negative thickness",
                "invalid refractive index",
            ],
        ),
        OpticalCalculatorCapability(
            calculator_name="paraxial",
            implemented=callable(analyze_two_lens_relay),
            api_endpoints=[
                "/api/optics/paraxial-lens",
                "/api/optics/paraxial-system",
                "/api/optics/two-lens-relay",
            ],
            reference_cases=[
                "paraxial_thin_lens_1to1",
                "abcd_free_space_matrix",
                "two_lens_4f_relay_1_to_1",
            ],
            failure_modes=[
                "zero focal length",
                "object at focal plane",
                "invalid ABCD element",
            ],
        ),
        OpticalCalculatorCapability(
            calculator_name="gaussian_beam",
            implemented=callable(gaussian_beam_parameters),
            api_endpoints=[
                "/api/optics/gaussian-beam",
                "/api/optics/gaussian-beam-series",
                "/api/optics/gaussian-beam-focus",
            ],
            reference_cases=[
                "gaussian_beam_rayleigh_range",
                "gaussian_beam_radius_at_waist",
                "gaussian_beam_radius_at_rayleigh_range",
            ],
            failure_modes=[
                "negative wavelength",
                "zero waist",
                "invalid sweep points",
            ],
        ),
        OpticalCalculatorCapability(
            calculator_name="waveguide",
            implemented=callable(slab_waveguide_sweep),
            api_endpoints=[
                "/api/optics/waveguide-estimate",
                "/api/optics/waveguide-sweep",
                "/api/optics/waveguide-single-mode-range",
            ],
            reference_cases=[
                "waveguide_v_number_sanity",
                "slab_waveguide_v_number_sweep",
            ],
            failure_modes=[
                "core_n <= cladding_n",
                "negative wavelength",
                "invalid sweep points",
            ],
        ),
    ]
    return calculators


def _requirement_template_capabilities() -> list[RequirementTemplateCapability]:
    capabilities: list[RequirementTemplateCapability] = []
    for template in list_requirement_templates():
        match_en = match_goal_to_template(template.natural_language_goal_en)
        match_zh = match_goal_to_template(template.natural_language_goal_zh)
        matched = (
            match_en.matched_template_id == template.template_id
            and match_zh.matched_template_id == template.template_id
        )
        capabilities.append(
            RequirementTemplateCapability(
                template_id=template.template_id,
                goal_en_present=bool(template.natural_language_goal_en),
                goal_zh_present=bool(template.natural_language_goal_zh),
                matched_by_heuristic=matched,
                expected_tools=template.expected_tool_calls,
                cross_check_status="pass" if matched else "fail",
                preview_only=(
                    template.safety.production_grade_validation_claimed is False
                    and template.safety.formal_convergence_proof_claimed is False
                ),
            )
        )
    return capabilities


def _blocked_external_actions(sample_session: Any) -> list[BlockedExternalAction]:
    ledger_by_name = {entry.tool_name: entry for entry in sample_session.tool_call_ledger}
    actions = [
        ("external_solver", "external_solver.meep", "External solvers require explicit approval."),
        ("external_llm", "external_llm", "External LLM calls are disabled by default."),
        ("testpypi_upload", "testpypi_upload", "TestPyPI upload is not exposed."),
        ("pypi_publish", "pypi_publish", "PyPI publication is not approved or exposed."),
        ("git_tag", "git_tag_create", "Tag creation is not exposed."),
        ("github_release", "github_release_create", "GitHub release creation is not exposed."),
    ]
    return [
        BlockedExternalAction(
            action_name=action_name,
            default_allowed=False,
            executed=bool(ledger_by_name.get(tool_name) and ledger_by_name[tool_name].executed),
            reason=ledger_by_name.get(tool_name).reason if tool_name in ledger_by_name else reason,
        )
        for action_name, tool_name, reason in actions
    ]


def _module_importable(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
    except Exception:  # noqa: BLE001 - report import reality without failing the whole report.
        return False
    return True
