"""Backend capability report for local Agent Studio reality checks."""

from __future__ import annotations

import importlib
import importlib.util
import json
from pathlib import Path
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
from optical_spec_agent.examples.application_domains import (
    list_application_domains,
    match_goal_to_application_domains,
)
from optical_spec_agent.examples.domain_cross_check import (
    ApplicationDomainCrossCheck,
    cross_check_all_application_domains,
)
from optical_spec_agent.examples.domain_benchmarks import (
    ApplicationDomainBenchmarkResultResponse,
    evaluate_all_domain_scenarios,
)
from optical_spec_agent.materials.catalog import (
    diagnose_material_suitability,
    list_materials,
    suggest_materials_for_application,
)
from optical_spec_agent.optical_language import (
    AdapterGoldenCoverageReport,
    build_adapter_golden_coverage_report,
    diagnose_observable,
    diagnose_missing_inputs,
    infer_source_monitor_from_goal,
    map_source_monitor_to_adapter,
)
from optical_spec_agent.optics import (
    analyze_two_lens_relay,
    calculate_thin_film_spectrum,
    gaussian_mode_overlap,
    gaussian_beam_parameters,
    jones_waveplate,
    slab_waveguide_sweep,
)
from optical_spec_agent.validation_maturity import (
    BackendValidationMaturityResponse,
    build_backend_validation_maturity_summary,
)
from optical_spec_agent.workflows import plan_workflow


class PackageCapability(BaseModel):
    package_version: str
    current_public_prerelease: str = "v0.9.0rc7"
    main_development_version: str = "0.9.0rc8"
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


class MaterialProvenanceCoverage(BaseModel):
    material_count: int
    materials_with_provenance: int
    materials_requiring_user_verification: int
    production_grade_optical_constants_claimed: bool = False
    notes: list[str] = Field(default_factory=list)


class AmbiguousRequirementMatchingCapability(BaseModel):
    available: bool = True
    deterministic: bool = True
    no_external_llm_used: bool = True
    covered_cases: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class MissingInputDiagnosticsCapability(BaseModel):
    available: bool = True
    critical_optional_split: bool = True
    safe_to_preview_default: bool = True
    safe_to_run_solver_default: bool = False
    notes: list[str] = Field(default_factory=list)


class ApplicationDomainCoverage(BaseModel):
    domain_count: int
    covered_domains: list[str] = Field(default_factory=list)
    partial_domains: list[str] = Field(default_factory=list)
    failed_domains: list[str] = Field(default_factory=list)
    preview_only: bool = True
    production_grade_validation_claimed: bool = False
    notes: list[str] = Field(default_factory=list)


class MaterialTemplateCrossCheckCoverage(BaseModel):
    total: int
    pass_count: int
    warning_count: int
    fail_count: int
    cross_checks: list[ApplicationDomainCrossCheck] = Field(default_factory=list)
    preview_only: bool = True
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainBenchmarkCoverage(BaseModel):
    scenario_count: int
    pass_count: int
    warn_count: int
    fail_count: int
    positive_count: int
    ambiguous_count: int
    underconstrained_count: int
    unsupported_count: int
    safety_summary: dict[str, bool] = Field(default_factory=dict)
    preview_only: bool = True
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class OptionalSolverMicroBenchmarkCoverage(BaseModel):
    manifest_exists: bool
    manifest_path: str = "validation/solver_validation_micro_benchmarks.json"
    optional_solver_evidence_summary_available: bool = True
    optional_solver_evidence_summary_path: str = "docs/optional_solver_evidence_summary.md"
    rc8_backend_readiness_review_available: bool = True
    rc8_backend_readiness_review_path: str = "docs/rc8_backend_readiness_review.md"
    solver_evidence_validation_maturity_mapping_available: bool = True
    solver_evidence_validation_maturity_mapping_path: str = (
        "docs/solver_evidence_validation_maturity_mapping.md"
    )
    solver_evidence_closed_for: list[str] = Field(
        default_factory=lambda: ["gmsh", "optiland", "meep", "mpb"]
    )
    solver_evidence_deferred_for: list[str] = Field(default_factory=lambda: ["elmer"])
    optional_solver_evidence_review_complete: bool = True
    readiness_available: bool = True
    readiness_script: str = "scripts/check_optional_solver_readiness.py"
    approval_matrix_available: bool = True
    approval_matrix_path: str = "docs/optional_solver_micro_benchmark_approval_matrix.md"
    approval_record_template_path: str = "docs/optional_solver_micro_benchmark_approval_record_template.md"
    execution_approval_packet_available: bool = True
    execution_approval_packet_path: str = "docs/optional_solver_micro_benchmark_execution_packet.md"
    execution_sequence_path: str = "docs/optional_solver_execution_sequence.md"
    meep_decision_packet_available: bool = True
    meep_decision_packet_path: str = (
        "docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md"
    )
    mpb_decision_packet_available: bool = True
    mpb_decision_packet_path: str = (
        "docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md"
    )
    approval_records_present: bool = True
    approval_records_path: str = "docs/optional_solver_approval_records"
    readiness_status_path: str = "docs/optional_solver_micro_benchmark_readiness_status.md"
    environment_profiles_available: bool = True
    environment_profiles_path: str = "validation/solver_environment_profiles.json"
    environment_profiles_doc: str = "docs/optional_solver_environment_profiles.md"
    solver_python_env_var: str = "OSA_SOLVER_PYTHON"
    profile_env_var: str = "OSA_SOLVER_READINESS_PROFILE"
    default_runs_solver: bool = False
    execution_default: bool = False
    opt_in_required: bool = True
    explicit_approval_required: bool = True
    all_optional_solver_execution_authorized: bool = False
    solvers: list[dict[str, Any]] = Field(default_factory=list)
    elmer_deferred: bool = True
    production_grade_claim: bool = False
    formal_convergence_proof_claimed: bool = False
    notes: list[str] = Field(default_factory=list)


class BackendCapabilityReport(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    evidence_pack_available: bool = True
    evidence_pack_sections: list[str] = Field(
        default_factory=lambda: [
            "Package and release status",
            "Sub-agent reality",
            "Tool-call reality",
            "Optical calculators",
            "Material provenance coverage",
            "Ambiguous requirement matching",
            "Missing-input diagnostics",
            "Application-domain coverage",
            "Material-template cross-checks",
            "Application-domain benchmarks",
            "Optional solver micro-benchmarks",
            "Design-case cross-checks",
            "Source / monitor / observable diagnostics",
            "Adapter-native golden coverage",
            "Validation maturity summary",
            "Preview boundary summary",
            "Blocked or deferred capabilities",
            "Maintainer review questions",
        ]
    )
    maintainer_review_recommended: bool = True
    package: PackageCapability
    sub_agents: list[SubAgentCapability] = Field(default_factory=list)
    internal_tools: list[InternalToolCapabilityReport] = Field(default_factory=list)
    optical_calculators: list[OpticalCalculatorCapability] = Field(default_factory=list)
    requirements_templates: list[RequirementTemplateCapability] = Field(default_factory=list)
    material_provenance_coverage: MaterialProvenanceCoverage
    ambiguous_requirement_matching: AmbiguousRequirementMatchingCapability
    missing_input_diagnostics: MissingInputDiagnosticsCapability
    application_domain_coverage: ApplicationDomainCoverage
    material_template_cross_checks: MaterialTemplateCrossCheckCoverage
    application_domain_benchmarks: ApplicationDomainBenchmarkCoverage
    optional_solver_micro_benchmarks: OptionalSolverMicroBenchmarkCoverage
    adapter_native_golden_coverage: AdapterGoldenCoverageReport
    validation_maturity_summary: BackendValidationMaturityResponse
    preview_boundary_summary: dict[str, object] = Field(default_factory=dict)
    validation_claim_audit_available: bool = True
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
    domain_cross_checks = cross_check_all_application_domains()
    domain_benchmarks = evaluate_all_domain_scenarios()
    golden_coverage = build_adapter_golden_coverage_report()
    maturity_summary = build_backend_validation_maturity_summary()
    all_sample_tool_names.add("adapter_native_golden.check")
    all_sample_tool_names.add("application_domain_benchmarks.evaluate")
    all_sample_tool_names.add("validation_maturity.build_summary")
    failed = any(check.status == "fail" for check in cross_checks.cross_checks)
    return BackendCapabilityReport(
        status="needs_review" if failed or golden_coverage.status == "needs_review" else "ok",
        package=PackageCapability(package_version=__version__),
        sub_agents=_sub_agent_capabilities(sample_session),
        internal_tools=_internal_tool_capabilities(all_sample_tool_names),
        optical_calculators=_optical_calculator_capabilities(),
        requirements_templates=_requirement_template_capabilities(),
        material_provenance_coverage=_material_provenance_coverage(),
        ambiguous_requirement_matching=_ambiguous_requirement_matching_capability(),
        missing_input_diagnostics=_missing_input_diagnostics_capability(),
        application_domain_coverage=_application_domain_coverage(domain_cross_checks.cross_checks),
        material_template_cross_checks=_material_template_cross_checks(domain_cross_checks.cross_checks),
        application_domain_benchmarks=_application_domain_benchmarks(domain_benchmarks),
        optional_solver_micro_benchmarks=_optional_solver_micro_benchmarks(),
        adapter_native_golden_coverage=golden_coverage,
        validation_maturity_summary=maturity_summary,
        preview_boundary_summary=maturity_summary.preview_boundary_summary,
        validation_claim_audit_available=True,
        design_case_cross_checks=cross_checks.cross_checks,
        blocked_external_actions=_blocked_external_actions(sample_session),
        recommended_next_actions=[
            "Generate the maintainer evidence pack with scripts/generate_backend_evidence_pack.py.",
            "Inspect design_case_cross_checks for any warning/fail status.",
            "Use scripts/audit_sub_agents.py for a concise import/call/execution view.",
            "Use scripts/smoke_backend_capabilities.sh for calculator sanity checks.",
            "Use scripts/check_adapter_native_golden.py for adapter-native metadata diff checks.",
            "Use /api/materials/diagnose to inspect material provenance and suitability warnings.",
            "Use /api/design-requirements/match to inspect ambiguous-goal questions.",
            "Use /api/application-domain-cross-checks to inspect domain/material/template coverage.",
            "Use /api/application-domain-benchmark-results to inspect scenario benchmark behavior.",
            "Use /api/backend-validation-maturity to inspect conservative evidence levels.",
            "Use scripts/run_optional_solver_micro_benchmarks.sh only after explicit opt-in validation approval.",
            "Run scripts/audit_validation_claims.py before release-draft work.",
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
            "material_suitability_diagnostics",
            "optical_spec_agent.materials.catalog",
            diagnose_material_suitability,
            "material_catalog.diagnose_suitability",
            "Reports material provenance, suitability, and verification warnings.",
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
            "ambiguous_requirement_matching",
            "optical_spec_agent.examples.requirements",
            match_goal_to_template,
            "requirements.match_ambiguity_check",
            "Reports candidate templates, confidence, and deterministic follow-up questions.",
        ),
        (
            "application_domain_registry",
            "optical_spec_agent.examples.application_domains",
            match_goal_to_application_domains,
            "application_domains.match_goal",
            "Maps application domains to templates, materials, calculators, adapters, and questions.",
        ),
        (
            "material_template_cross_checks",
            "optical_spec_agent.examples.domain_cross_check",
            cross_check_all_application_domains,
            "application_domains.cross_check_domain",
            "Cross-checks application-domain material/template/calculator/adapter coverage.",
        ),
        (
            "application_domain_benchmarks",
            "optical_spec_agent.examples.domain_benchmarks",
            evaluate_all_domain_scenarios,
            "application_domain_benchmarks.evaluate",
            "Evaluates positive, ambiguous, underconstrained, and unsupported optical-design scenarios.",
        ),
        (
            "missing_input_diagnostics",
            "optical_spec_agent.optical_language",
            diagnose_missing_inputs,
            "optical_language.diagnose_missing_inputs",
            "Reports missing source/monitor inputs, default assumptions, and solver safety state.",
        ),
        (
            "observable_diagnostics",
            "optical_spec_agent.optical_language",
            diagnose_observable,
            "optical_language.diagnose_observable",
            "Classifies observables, required inputs, and preview-vs-real-result boundaries.",
        ),
        (
            "adapter_native_mapping",
            "optical_spec_agent.optical_language",
            map_source_monitor_to_adapter,
            "optical_language.map_source_monitor_to_adapter",
            "Maps source/monitor/observable intent to adapter-native preview semantics.",
        ),
        (
            "adapter_native_golden_coverage",
            "optical_spec_agent.optical_language",
            build_adapter_golden_coverage_report,
            "adapter_native_golden.check",
            "Builds local adapter-native golden preview coverage and metadata diff evidence.",
        ),
        (
            "validation_maturity_summary",
            "optical_spec_agent.validation_maturity",
            build_backend_validation_maturity_summary,
            "validation_maturity.build_summary",
            "Classifies conservative backend evidence levels and preview boundaries.",
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
        OpticalCalculatorCapability(
            calculator_name="fiber_coupling",
            implemented=callable(gaussian_mode_overlap),
            api_endpoints=["/api/optics/fiber-coupling"],
            reference_cases=[
                "fiber_gaussian_perfect_overlap",
                "fiber_gaussian_waist_mismatch",
                "fiber_gaussian_offset_loss",
                "fiber_gaussian_tilt_loss",
            ],
            failure_modes=[
                "negative wavelength",
                "zero waist",
                "non-finite waist or wavelength",
                "negative lateral offset",
                "non-finite angular tilt",
            ],
        ),
        OpticalCalculatorCapability(
            calculator_name="polarization",
            implemented=callable(jones_waveplate),
            api_endpoints=["/api/optics/polarization-jones"],
            reference_cases=[
                "jones_linear_0deg",
                "jones_linear_90deg",
                "jones_linear_polarizer_malus",
                "jones_half_waveplate_preview",
                "jones_quarter_waveplate_phase_preview",
            ],
            failure_modes=[
                "zero Jones-vector intensity",
                "invalid Jones-vector shape",
                "non-finite retardance",
                "non-finite angle",
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


def _material_provenance_coverage() -> MaterialProvenanceCoverage:
    materials = list_materials()
    return MaterialProvenanceCoverage(
        material_count=len(materials),
        materials_with_provenance=sum(1 for item in materials if item.provenance_type),
        materials_requiring_user_verification=sum(
            1 for item in materials if item.requires_user_verification
        ),
        production_grade_optical_constants_claimed=any(
            item.production_grade_optical_constants for item in materials
        ),
        notes=[
            "All starter material records are local preview/design-assist entries.",
            "Numeric n/k values remain approximate and require user verification.",
            "No external material database lookup is performed.",
        ],
    )


def _ambiguous_requirement_matching_capability() -> AmbiguousRequirementMatchingCapability:
    generic = match_goal_to_template("Design an optical system.")
    mixed = match_goal_to_template("Plan a waveguide and thin film coating design.")
    lens = match_goal_to_template("Help me optimize a lens.")
    return AmbiguousRequirementMatchingCapability(
        covered_cases=[
            "generic_optical_system",
            "waveguide_or_coating",
            "lens_optimization_underconstrained",
            "unknown_application",
        ],
        notes=[
            f"Generic optical goal confidence: {generic.confidence}.",
            f"Mixed waveguide/coating candidates: {', '.join(mixed.candidate_templates)}.",
            f"Underconstrained lens missing inputs: {', '.join(lens.missing_disambiguation_inputs)}.",
            "Ambiguous goals generate questions instead of unsafe solver actions.",
        ],
    )


def _missing_input_diagnostics_capability() -> MissingInputDiagnosticsCapability:
    session = build_agent_task_session("Help me optimize a lens.")
    return MissingInputDiagnosticsCapability(
        notes=[
            f"Critical inputs reported: {', '.join(session.missing_critical_inputs)}.",
            f"Optional inputs reported: {', '.join(session.missing_optional_inputs)}.",
            "safe_to_preview remains true while safe_to_run_solver remains false.",
        ],
    )


def _application_domain_coverage(
    checks: list[ApplicationDomainCrossCheck],
) -> ApplicationDomainCoverage:
    domains = list_application_domains()
    return ApplicationDomainCoverage(
        domain_count=len(domains),
        covered_domains=[check.domain_id for check in checks if check.status == "pass"],
        partial_domains=[check.domain_id for check in checks if check.status == "warning"],
        failed_domains=[check.domain_id for check in checks if check.status == "fail"],
        notes=[
            "Application domains are local preview coverage anchors, not production validation.",
            "Fiber coupling and polarization optics now have deterministic local preview calculators; solver-backed validation remains deferred.",
            "No external solver, external LLM, or material database lookup is required.",
        ],
    )


def _material_template_cross_checks(
    checks: list[ApplicationDomainCrossCheck],
) -> MaterialTemplateCrossCheckCoverage:
    return MaterialTemplateCrossCheckCoverage(
        total=len(checks),
        pass_count=sum(1 for check in checks if check.status == "pass"),
        warning_count=sum(1 for check in checks if check.status == "warning"),
        fail_count=sum(1 for check in checks if check.status == "fail"),
        cross_checks=checks,
    )


def _application_domain_benchmarks(
    results: ApplicationDomainBenchmarkResultResponse,
) -> ApplicationDomainBenchmarkCoverage:
    summary = results.summary
    return ApplicationDomainBenchmarkCoverage(
        scenario_count=summary["total"],
        pass_count=summary["pass"],
        warn_count=summary["warn"],
        fail_count=summary["fail"],
        positive_count=summary["positive"],
        ambiguous_count=summary["ambiguous"],
        underconstrained_count=summary["underconstrained"],
        unsupported_count=summary["unsupported"],
        safety_summary={
            "external_solver_executed": results.external_solver_executed,
            "external_llm_required": results.external_llm_required,
            "proprietary_solver_required": results.proprietary_solver_required,
            "production_grade_validation_claimed": results.production_grade_validation_claimed,
            "formal_convergence_proof_claimed": results.formal_convergence_proof_claimed,
        },
    )


def _optional_solver_micro_benchmarks() -> OptionalSolverMicroBenchmarkCoverage:
    manifest_path = Path("validation/solver_validation_micro_benchmarks.json")
    if not manifest_path.exists():
        return OptionalSolverMicroBenchmarkCoverage(
            manifest_exists=False,
            readiness_available=Path("scripts/check_optional_solver_readiness.py").exists(),
            approval_matrix_available=Path(
                "docs/optional_solver_micro_benchmark_approval_matrix.md"
            ).exists(),
            notes=["Optional solver micro-benchmark manifest is missing."],
        )
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    solvers = payload.get("solvers", [])
    return OptionalSolverMicroBenchmarkCoverage(
        manifest_exists=True,
        optional_solver_evidence_summary_available=Path(
            "docs/optional_solver_evidence_summary.md"
        ).exists(),
        rc8_backend_readiness_review_available=Path(
            "docs/rc8_backend_readiness_review.md"
        ).exists(),
        solver_evidence_validation_maturity_mapping_available=Path(
            "docs/solver_evidence_validation_maturity_mapping.md"
        ).exists(),
        solver_evidence_closed_for=payload.get(
            "solver_evidence_closed_for", ["gmsh", "optiland", "meep", "mpb"]
        ),
        solver_evidence_deferred_for=payload.get(
            "solver_evidence_deferred_for", ["elmer"]
        ),
        optional_solver_evidence_review_complete=bool(
            payload.get("optional_solver_evidence_review_complete", True)
        ),
        readiness_available=Path("scripts/check_optional_solver_readiness.py").exists(),
        approval_matrix_available=Path(
            "docs/optional_solver_micro_benchmark_approval_matrix.md"
        ).exists(),
        execution_approval_packet_available=Path(
            "docs/optional_solver_micro_benchmark_execution_packet.md"
        ).exists(),
        meep_decision_packet_available=Path(
            "docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md"
        ).exists(),
        mpb_decision_packet_available=Path(
            "docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md"
        ).exists(),
        approval_records_present=Path("docs/optional_solver_approval_records").exists(),
        environment_profiles_available=Path(
            "validation/solver_environment_profiles.json"
        ).exists(),
        default_runs_solver=bool(payload.get("default_runs_solver", False)),
        execution_default=False,
        opt_in_required=bool(payload.get("opt_in_required", True)),
        explicit_approval_required=True,
        all_optional_solver_execution_authorized=all(
            bool(item.get("execution_authorized", False)) for item in solvers
        )
        if solvers
        else False,
        solvers=solvers,
        elmer_deferred=any(
            item.get("solver_name") == "elmer" and item.get("status") == "deferred"
            for item in solvers
        ),
        production_grade_claim=bool(
            payload.get("production_grade_validation_claimed", False)
        ),
        formal_convergence_proof_claimed=bool(
            payload.get("formal_convergence_proof_claimed", False)
        ),
        notes=[
            "Unified solver micro-benchmark wrapper is default no-execute.",
            "Readiness script performs availability detection only and does not execute solvers.",
            "Readiness can be calibrated with OSA_SOLVER_PYTHON and OSA_SOLVER_READINESS_PROFILE.",
            "Approval matrix and approval record template are maintainer review aids.",
            "Gmsh has an approved 2026-05-20 Gmsh-only optional micro-benchmark pass recorded as mesh generation smoke evidence.",
            "The Gmsh evidence was reviewed and accepted as optional manual mesh-generation smoke evidence; it does not authorize further solver execution.",
            "Optiland evidence was reviewed and accepted as optional manual ray/path smoke evidence; it does not authorize further solver execution.",
            (
                "Gmsh was not rerun by the Optiland, Meep, or MPB tasks; "
                "Optiland was not rerun by the Meep or MPB tasks; the Meep "
                "FDTD benchmark was not rerun by the MPB task."
            ),
            "Meep evidence was reviewed and accepted as optional manual PyMeep/FDTD smoke evidence; it does not authorize future Meep reruns or other solver execution.",
            "MPB evidence was reviewed and accepted as optional manual MPB/band-structure smoke evidence; it does not authorize future MPB reruns or other solver execution.",
            "Optional solver evidence review loops are closed for Gmsh, Optiland, Meep, and MPB; Elmer remains deferred and not Level 3.",
            "The rc8 backend readiness review summarizes this evidence without authorizing PyPI, TestPyPI, tag, release, or v1.0.0 actions.",
            "Execution approval packet and per-solver records preserve pending/deferred review aids for future runs.",
            "Future execution should run one solver at a time after explicit approval.",
            "Opt-in environment variables are required for solver-backed runs.",
            "Elmer remains deferred and is not Level 3.",
        ],
    )


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
