"""API routes."""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path
import shutil
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from optical_spec_agent import __version__
from optical_spec_agent.api.models import (
    AgentTraceRequest,
    AgentTraceResponse,
    AgentSessionRequest,
    AgentTaskSessionResponse,
    ApplicationDomainDetailResponse,
    ApplicationDomainBenchmarkResponse,
    ApplicationDomainBenchmarkResultResponse,
    ApplicationDomainMatchRequest,
    ApplicationDomainMatchResult,
    ApplicationDomainScenarioResponse,
    ApplicationDomainScenarioResult,
    ApplicationDomainsResponse,
    ApplicationDomainCrossChecksResponse,
    AdapterPreviewRequest as AgentAdapterPreviewRequest,
    AdapterPreviewResponse,
    AdapterSummary,
    AdaptersResponse,
    ApiDiagnostic,
    ApiErrorResponse,
    DesignRequirementDetailResponse,
    DesignRequirementMatchRequest,
    DesignRequirementsResponse,
    ExampleDetailResponse,
    ExamplesResponse,
    HealthResponse,
    MaterialDetailResponse,
    MaterialDiagnoseRequest,
    MaterialDiagnoseResponse,
    MaterialSuggestionRequest,
    MaterialSuggestionResponse,
    MaterialsResponse,
    OpticalCalculatorResponse,
    OpticalLanguageDiagnoseRequest,
    OpticalLanguageDiagnoseResponse,
    OpticalLanguageAdapterMappingRequest,
    OpticalLanguageAdapterMappingResponse,
    OpticalLanguageInferRequest,
    OpticalLanguageObservableDiagnoseRequest,
    OpticalLanguageObservableDiagnoseResponse,
    ParaxialSystemRequest,
    ParaxialLensRequest,
    QuarterWaveARRequest,
    ParseRequest as AgentParseRequest,
    ParseResponse as AgentParseResponse,
    ReadinessResponse,
    RequirementMatchResult,
    SchemaResponse,
    ThinFilmSpectrumRequest,
    ThinFilmCalculatorRequest,
    ToolCapabilitiesResponse,
    ToolCapabilityItem,
    ValidateRequest as AgentSpecRequest,
    ValidateResponse as AgentValidateResponse,
    ValidationEvidenceItem,
    ValidationEvidenceResponse,
    VersionResponse,
    GaussianBeamFocusRequest,
    GaussianBeamRequest,
    GaussianBeamSeriesRequest,
    FiberCouplingRequest,
    PolarizationJonesRequest,
    TwoLensRelayRequest,
    WaveguideSingleModeRangeRequest,
    WaveguideEstimateRequest,
    WaveguideSweepRequest,
    WorkflowPlanRequest as AgentWorkflowPlanRequest,
    WorkflowPlanResponse,
    SourceMonitorInference,
)
from optical_spec_agent.agents.orchestrator import build_agent_trace
from optical_spec_agent.agents.capability_report import (
    BackendCapabilityReport,
    generate_backend_capability_report,
)
from optical_spec_agent.agents.evidence_pack import (
    BackendEvidencePack,
    generate_backend_evidence_pack,
)
from optical_spec_agent.agents.task_session import build_agent_task_session
from optical_spec_agent.adapters.registry import (
    AdapterRegistryError,
    dispatch_adapter,
    get_adapter,
    list_adapters,
)
from optical_spec_agent.examples.registry import (
    ExampleRegistryError,
    build_example_agent_trace,
    get_optical_design_example,
    list_optical_design_examples,
)
from optical_spec_agent.examples.cross_check import (
    DesignCaseCrossChecksResponse,
    cross_check_all_design_cases,
)
from optical_spec_agent.examples.application_domains import (
    get_application_domain,
    list_application_domains,
    match_goal_to_application_domains,
)
from optical_spec_agent.examples.domain_cross_check import (
    cross_check_all_application_domains,
    cross_check_application_domain,
)
from optical_spec_agent.examples.domain_benchmarks import (
    application_domain_benchmark_response,
    evaluate_all_domain_scenarios,
    evaluate_domain_scenario,
    get_domain_scenario,
)
from optical_spec_agent.examples.requirements import (
    get_requirement_template,
    list_requirement_templates,
    match_goal_to_template,
)
from optical_spec_agent.optical_language import (
    AdapterGoldenCoverageReport,
    build_adapter_golden_coverage_report,
    diagnose_observable,
    diagnose_missing_inputs,
    infer_source_monitor_from_goal,
    map_source_monitor_to_adapter,
)
from optical_spec_agent.materials.catalog import (
    diagnose_material_suitability,
    get_material,
    list_materials,
    suggest_materials_for_application,
)
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.optics import (
    analyze_two_lens_relay,
    calculate_thin_film_spectrum,
    calculate_thin_film_stack,
    compose_abcd,
    design_quarter_wave_ar_coating,
    focus_gaussian_beam_thin_lens,
    gaussian_beam_parameters,
    gaussian_mode_overlap,
    jones_linear_polarizer,
    jones_waveplate,
    linear_polarization,
    summarize_polarization_state,
    propagate_gaussian_beam,
    propagate_gaussian_beam_series,
    slab_waveguide_sweep,
    thin_lens,
    slab_waveguide_v_number,
    suggest_single_mode_thickness_range,
)
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.validation_maturity import (
    BackendValidationMaturityResponse,
    build_backend_validation_maturity_summary,
)
from optical_spec_agent.utils.format import spec_to_summary
from optical_spec_agent.validators.spec_validator import SpecValidator


router = APIRouter()

REPO_ROOT = Path(__file__).resolve().parents[3]
CURRENT_PUBLIC_PRERELEASE = "v0.9.0rc7"
MAIN_DEVELOPMENT_VERSION = __version__

SAFETY_FLAGS: dict[str, bool] = {
    "external_solver_executed": False,
    "external_llm_required": False,
    "proprietary_solver_required": False,
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
}

API_ERROR_RESPONSES = {
    400: {"model": ApiErrorResponse},
    404: {"model": ApiErrorResponse},
}

ADAPTER_MATURITY: dict[str, dict[str, Any]] = {
    "gmsh": {
        "maturity_level": "Level 3",
        "evidence": "validation/gmsh/gmsh_validation_pilot_2026-05-14.md",
    },
    "meep": {
        "maturity_level": "Level 3",
        "evidence": "validation/meep/meep_validation_pilot_2026-05-14.md",
    },
    "mpb": {
        "maturity_level": "Level 3",
        "evidence": "validation/mpb/mpb_validation_pilot_2026-05-14.md",
    },
    "optiland": {
        "maturity_level": "Level 3",
        "evidence": "validation/optiland/optiland_validation_pilot_2026-05-14.md",
    },
    "elmer": {
        "maturity_level": "Level 2 + Level-3-ready",
        "evidence": "validation/elmer/elmer_install_deferred_2026-05-15.md",
        "status_note": "Level 3 validation deferred pending maintainable ElmerSolver availability.",
    },
}


# ---- Request / Response schemas ----

class ParseRequest(BaseModel):
    text: str = Field(..., description="Natural language optical task description")
    task_id: str = Field("", description="Optional task ID (auto-generated if empty)")
    parser: str = Field("rule", description="Parser mode: rule, llm, or hybrid")
    llm_provider: str = Field("mock", description="LLM provider for llm/hybrid modes")
    llm_model: str | None = Field(None, description="Optional LLM model label")
    parser_report: bool = Field(False, description="Include parser report when available")


class ParseResponse(BaseModel):
    spec_json: dict[str, Any]
    summary: str
    confirmed_fields: dict[str, Any]
    inferred_fields: dict[str, Any]
    missing_fields: list[str]
    assumption_log: list[str]
    validation_status: dict[str, Any]
    parser_report: dict[str, Any] | None = None


class ValidateRequest(BaseModel):
    """Accept either raw text or a pre-built spec dict."""
    text: str | None = None
    spec_json: dict[str, Any] | None = None


class ValidateResponse(BaseModel):
    is_executable: bool
    errors: list[str]
    warnings: list[str]
    missing_fields: list[str]


class WorkflowPlanRequest(BaseModel):
    text: str
    parser: str = "rule"
    llm_provider: str = "mock"
    tool: str = "auto"


class WorkflowRunRequest(BaseModel):
    text: str
    parser: str = "rule"
    llm_provider: str = "mock"
    tool: str = "auto"
    output_dir: str = "outputs/workflows/api"
    allow_execute: bool = False
    run_diagnostics: bool = True
    strict: bool = False


class WorkflowReportRequest(BaseModel):
    workflow_run: dict[str, Any]
    format: str = "markdown"


# ---- Routes ----

@router.get("/health")
def health_check():
    return {"status": "ok", "version": __version__}


@router.post("/parse", response_model=ParseResponse)
def parse(req: ParseRequest):
    from optical_spec_agent.parsers.llm import LLMParserConfig, LLMParserError
    from optical_spec_agent.parsers.llm.client import LLMProviderError
    from optical_spec_agent.parsers.registry import ParserRegistryError

    config = LLMParserConfig(
        provider=req.llm_provider,
        model=req.llm_model or "mock-optical-parser",
        parser_mode="hybrid" if req.parser == "hybrid" else "llm",
    )
    try:
        svc = SpecService(parser=req.parser, llm_config=config)
        spec = svc.process(req.text, task_id=req.task_id)
    except (ParserRegistryError, LLMProviderError, LLMParserError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ParseResponse(
        spec_json=spec.to_flat_dict(),
        summary=spec_to_summary(spec),
        confirmed_fields=spec.confirmed_fields,
        inferred_fields=spec.inferred_fields,
        missing_fields=spec.missing_fields,
        assumption_log=spec.assumption_log,
        validation_status=spec.validation_status.model_dump(),
        parser_report=svc.last_parser_report.model_dump() if req.parser_report and svc.last_parser_report else None,
    )


@router.post("/validate", response_model=ValidateResponse)
def validate(req: ValidateRequest):
    from optical_spec_agent.validators.spec_validator import SpecValidator

    if req.text:
        svc = SpecService()
        spec = svc.process(req.text)
    elif req.spec_json:
        spec = OpticalSpec.model_validate(req.spec_json)
        validator = SpecValidator()
        spec = validator.validate(spec)
    else:
        return ValidateResponse(
            is_executable=False,
            errors=["请提供 text 或 spec_json"],
            warnings=[],
            missing_fields=[],
        )

    return ValidateResponse(
        is_executable=spec.validation_status.is_executable,
        errors=spec.validation_status.errors,
        warnings=spec.validation_status.warnings,
        missing_fields=spec.missing_fields,
    )


@router.get("/schema")
def get_schema():
    """Export the JSON Schema for the OpticalSpec model."""
    return OpticalSpec.export_json_schema_dict()


@router.post("/workflow/plan")
def workflow_plan(req: WorkflowPlanRequest):
    """Plan a synchronous local workflow. Does not run solvers."""
    from optical_spec_agent.parsers.llm.client import LLMProviderError
    from optical_spec_agent.workflows import plan_workflow

    try:
        return plan_workflow(
            req.text,
            parser=req.parser,
            llm_provider=req.llm_provider,
            tool=req.tool,
        ).model_dump(mode="json")
    except LLMProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/workflow/run")
def workflow_run(req: WorkflowRunRequest):
    """Run a synchronous local workflow. API defaults to no solver execution."""
    from pathlib import Path

    from optical_spec_agent.parsers.llm.client import LLMProviderError
    from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig

    try:
        config = WorkflowRunnerConfig(
            parser=req.parser,
            llm_provider=req.llm_provider,
            tool=req.tool,
            output_dir=Path(req.output_dir),
            allow_execute=req.allow_execute,
            run_diagnostics=req.run_diagnostics,
            strict=req.strict,
        )
        return WorkflowRunner(config).run(req.text).model_dump(mode="json")
    except LLMProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/workflow/report")
def workflow_report(req: WorkflowReportRequest):
    """Render a workflow report from a workflow_run object."""
    from optical_spec_agent.workflows import render_workflow_report
    from optical_spec_agent.workflows.models import WorkflowRun

    try:
        workflow = WorkflowRun.model_validate(req.workflow_run)
        content = render_workflow_report(workflow, fmt=req.format)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"format": req.format, "content": content}


# ---- Local Agent API routes ----


@router.get("/api/health", response_model=HealthResponse)
def agent_health():
    """Local-first API health endpoint for future Agent Studio clients."""
    return HealthResponse(
        status="ok",
        service="optical-spec-agent",
    )


@router.get("/api/version", response_model=VersionResponse)
def agent_version():
    return VersionResponse(
        package_version=__version__,
        current_public_prerelease=CURRENT_PUBLIC_PRERELEASE,
        main_development_version=MAIN_DEVELOPMENT_VERSION,
    )


@router.get("/api/adapters", response_model=AdaptersResponse)
def agent_adapters():
    adapters: list[AdapterSummary] = []
    for metadata in list_adapters():
        maturity = ADAPTER_MATURITY.get(metadata.tool_name, {})
        adapters.append(
            AdapterSummary(
                tool_name=metadata.tool_name,
                display_name=metadata.display_name,
                solver_family=metadata.solver_family,
                current_status=metadata.current_status,
                maturity_level=maturity.get("maturity_level", "unclassified"),
                evidence=maturity.get("evidence"),
                limitations=metadata.limitations,
            )
        )
    return AdaptersResponse(adapters=adapters)


@router.get("/api/schema", response_model=SchemaResponse)
def agent_schema():
    return SchemaResponse(json_schema=OpticalSpec.export_json_schema_dict())


@router.post(
    "/api/parse",
    response_model=AgentParseResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_parse(req: AgentParseRequest):
    try:
        parser = _local_parser(req.parser)
        svc = SpecService(parser=parser)
        spec = svc.process(req.text, task_id=req.task_id)
    except AgentApiError as exc:
        return _agent_error_response(exc)
    except Exception as exc:  # noqa: BLE001 - API returns structured diagnostics.
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return AgentParseResponse(
        parser=parser,
        spec=spec.to_flat_dict(),
        summary=spec_to_summary(spec),
        diagnostics=ApiDiagnostic(
            missing_fields=spec.missing_fields,
            warnings=spec.validation_status.warnings,
            errors=spec.validation_status.errors,
            assumptions=spec.assumption_log,
        ),
        recommended_next_actions=[
            "Review inferred fields before generation.",
            "Use /api/validate before adapter preview.",
        ],
    )


@router.post(
    "/api/validate",
    response_model=AgentValidateResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_validate(req: AgentSpecRequest):
    try:
        spec = _load_spec(req.spec, req.path)
        validated = SpecValidator().validate(spec)
    except AgentApiError as exc:
        return _agent_error_response(exc)
    return AgentValidateResponse(
        status="ok" if validated.validation_status.is_executable else "needs_review",
        valid=validated.validation_status.is_executable,
        diagnostics=ApiDiagnostic(
            errors=validated.validation_status.errors,
            warnings=validated.validation_status.warnings,
            missing_fields=validated.missing_fields,
        ),
    )


@router.post(
    "/api/workflow-plan",
    response_model=WorkflowPlanResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_workflow_plan(req: AgentWorkflowPlanRequest):
    from optical_spec_agent.workflows import plan_workflow

    try:
        parser = _local_parser(req.parser)
        if req.text is None and req.path is None and req.spec is None:
            raise AgentApiError(
                "invalid_workflow_request",
                "Provide text, spec, or local path for workflow planning.",
                diagnostics=ApiDiagnostic(
                    errors=["Workflow planning requires text, spec, or path."]
                ),
                recommended_next_actions=[
                    "Send local text, an inline OpticalSpec, or a repo-local workflow fixture path."
                ],
            )
        input_text = req.text
        if input_text is None and req.path:
            input_text = _load_workflow_input_text(req.path)
        if input_text is None:
            spec = _load_spec(req.spec, req.path)
            input_text = _workflow_text_from_spec(spec)

        plan = plan_workflow(input_text, parser=parser, llm_provider="mock", tool=req.tool)
    except AgentApiError as exc:
        return _agent_error_response(exc)
    except Exception as exc:  # noqa: BLE001 - return stable local API errors.
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    payload = plan.model_dump(mode="json")
    return WorkflowPlanResponse(
        workflow_plan=payload,
        public_top_level_keys=sorted(payload),
        recommended_next_actions=[
            "Review workflow_plan.risk_flags before running any optional execution.",
            "Use /api/adapter-preview for local artifact preview.",
        ],
    )


@router.post(
    "/api/adapter-preview",
    response_model=AdapterPreviewResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_adapter_preview(req: AgentAdapterPreviewRequest):
    try:
        spec = _load_spec(req.spec, req.path)
        adapter = dispatch_adapter(spec, preferred_tool=req.tool)
        metadata = adapter.metadata()
        result = adapter.generate(spec)
    except AgentApiError as exc:
        return _agent_error_response(exc)
    except AdapterRegistryError as exc:
        return _agent_error_response(
            AgentApiError(
                "unsupported_adapter",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=["Use /api/adapters to inspect supported adapter names."],
            )
        )
    except Exception as exc:  # noqa: BLE001 - preview should return clean API errors.
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )

    status = "ok" if not result.errors else "needs_review"
    source_monitor = infer_source_monitor_from_goal(_workflow_text_from_spec(spec))
    observable_diagnostics = diagnose_observable(
        source_monitor.source_model,
        source_monitor.monitor_model,
        template_id=source_monitor.matched_template_id,
    )
    adapter_mapping = map_source_monitor_to_adapter(
        result.tool,
        source_monitor.source_model,
        source_monitor.monitor_model,
        observable_diagnostics,
    )
    observable_warnings = [
        warning
        for diagnostic in observable_diagnostics
        for warning in diagnostic.warnings
    ]
    all_warnings = [
        *result.warnings,
        *observable_warnings,
        *adapter_mapping.warnings,
    ]
    return AdapterPreviewResponse(
        status=status,
        tool=result.tool,
        display_name=metadata.display_name,
        output_language=result.language,
        output_extension=metadata.output_extension,
        preview_content=result.content,
        source_model=source_monitor.source_model,
        monitor_model=source_monitor.monitor_model,
        observable_diagnostics=observable_diagnostics,
        adapter_source_monitor_mapping=adapter_mapping,
        preview_only=True,
        solver_execution_required_for_real_result=(
            adapter_mapping.requires_solver_for_real_result
        ),
        warnings=all_warnings,
        artifact_summary={
            "content_length": len(result.content),
            "generated_files": result.generated_files,
            "missing_required": result.missing_required,
            "defaults_applied": result.defaults_applied,
            "source_model": source_monitor.source_model.model_dump(mode="json"),
            "monitor_model": source_monitor.monitor_model.model_dump(mode="json"),
            "observable_diagnostics": [
                item.model_dump(mode="json") for item in observable_diagnostics
            ],
            "adapter_source_monitor_mapping": adapter_mapping.model_dump(mode="json"),
            "observable_summary": source_monitor.monitor_model.observable,
            "source_monitor_default_assumptions": (
                source_monitor.diagnostics.default_assumptions_applied
            ),
            "preview_only": True,
            "solver_execution_required_for_real_result": (
                adapter_mapping.requires_solver_for_real_result
            ),
        },
        diagnostics=ApiDiagnostic(
            warnings=all_warnings,
            errors=result.errors,
            limitations=[
                *result.limitations,
                "Adapter-native source/monitor mapping is preview metadata only.",
                "No real solver monitor result was produced.",
            ],
        ),
    )


@router.get("/api/validation-evidence", response_model=ValidationEvidenceResponse)
def agent_validation_evidence():
    evidence = []
    for tool in ("gmsh", "meep", "mpb", "optiland", "elmer"):
        adapter = get_adapter(tool)
        metadata = adapter.metadata()
        maturity = ADAPTER_MATURITY[tool]
        evidence.append(
            ValidationEvidenceItem(
                tool_name=tool,
                display_name=metadata.display_name,
                maturity_level=maturity["maturity_level"],
                evidence=maturity.get("evidence"),
                status_note=maturity.get(
                    "status_note", "Optional manual validation evidence recorded."
                ),
            )
        )
    return ValidationEvidenceResponse(validation_evidence=evidence)


@router.get("/api/readiness", response_model=ReadinessResponse)
def agent_readiness():
    adapter_maturity = {
        tool: data["maturity_level"] for tool, data in ADAPTER_MATURITY.items()
    }
    return ReadinessResponse(
        current_public_prerelease=CURRENT_PUBLIC_PRERELEASE,
        main_development_version=MAIN_DEVELOPMENT_VERSION,
        testpypi={
            "uploaded_and_verified": True,
            "verified_version": "0.9.0rc6.dev0",
            "upload_for_current_dev_version": "not performed",
        },
        pypi={
            "published": False,
            "publication_approval": "not granted",
        },
        public_contract_freeze={
            "status": "approved",
            "date": "2026-05-16",
        },
        adapter_maturity=adapter_maturity,
        v1_0_0_released=False,
        recommended_next_actions=[
            "Continue API readiness engineering.",
            "Decide PyPI publication later with explicit maintainer approval.",
            "Prepare v1.0.0 release draft only after explicit approval.",
        ],
    )


@router.get("/api/tool-capabilities", response_model=ToolCapabilitiesResponse)
def agent_tool_capabilities():
    """Report backend tool reality without executing external tools."""

    internal = [
        ToolCapabilityItem(
            tool_name="material_catalog",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.materials.catalog",
            notes=["Callable local preview material catalog."],
        ),
        ToolCapabilityItem(
            tool_name="material_suitability_diagnostics",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.materials.catalog",
            notes=[
                "Reports local preview provenance, suitability warnings, and verification prompts."
            ],
        ),
        ToolCapabilityItem(
            tool_name="example_registry",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.examples.registry",
            notes=["Loads repo-local optical design examples."],
        ),
        ToolCapabilityItem(
            tool_name="agent_trace_builder",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.agents.orchestrator",
            notes=["Builds deterministic local sub-agent traces."],
        ),
        ToolCapabilityItem(
            tool_name="workflow_planner",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.workflows",
            notes=["Plans local no-execute workflows."],
        ),
        ToolCapabilityItem(
            tool_name="adapter_preview_generator",
            tool_kind="adapter_preview",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="adapter registry dispatch",
            notes=["Generates preview scaffold content only."],
        ),
        ToolCapabilityItem(
            tool_name="ambiguous_requirement_matching",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.examples.requirements",
            notes=[
                "Reports match confidence, candidate templates, and deterministic follow-up questions."
            ],
        ),
        ToolCapabilityItem(
            tool_name="application_domain_registry",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.examples.application_domains",
            notes=[
                "Maps application domains to templates, materials, calculators, adapters, and questions."
            ],
        ),
        ToolCapabilityItem(
            tool_name="material_template_cross_checks",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.examples.domain_cross_check",
            notes=[
                "Cross-checks application-domain material/template/calculator/adapter coverage."
            ],
        ),
        ToolCapabilityItem(
            tool_name="application_domain_benchmarks",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.examples.domain_benchmarks",
            notes=[
                "Evaluates positive, ambiguous, underconstrained, and unsupported optical-design scenarios."
            ],
        ),
        ToolCapabilityItem(
            tool_name="source_monitor_inference",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.optical_language",
            notes=[
                "Infers preview source, monitor, observable, and defaults with local heuristics."
            ],
        ),
        ToolCapabilityItem(
            tool_name="missing_input_diagnostics",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.optical_language",
            notes=[
                "Reports source/monitor missing inputs, ambiguity notes, and safe_to_run_solver=false."
            ],
        ),
        ToolCapabilityItem(
            tool_name="observable_diagnostics",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.optical_language",
            notes=[
                "Diagnoses observable taxonomy, required inputs, and preview-vs-real-result boundaries."
            ],
        ),
        ToolCapabilityItem(
            tool_name="adapter_native_mapping",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.optical_language",
            notes=[
                "Maps source/monitor/observable intent to adapter-native preview semantics."
            ],
        ),
        ToolCapabilityItem(
            tool_name="adapter_native_golden_coverage",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.optical_language",
            notes=[
                "Builds local adapter-native golden coverage and strict metadata diff evidence."
            ],
        ),
        ToolCapabilityItem(
            tool_name="validation_maturity_summary",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.validation_maturity",
            notes=[
                "Classifies conservative backend evidence levels and preview boundaries."
            ],
        ),
        ToolCapabilityItem(
            tool_name="optical_calculators",
            tool_kind="internal_python",
            available=True,
            default_allowed=True,
            status="available",
            detection_method="import optical_spec_agent.optics",
            notes=[
                "Thin-film, paraxial, Gaussian beam, waveguide, fiber-coupling, and polarization preview calculators."
            ],
        ),
    ]
    external = [
        _external_tool_capability("meep", module_name="meep"),
        _external_tool_capability("gmsh", module_name="gmsh", executable_name="gmsh"),
        _external_tool_capability("mpb", executable_name="mpb"),
        _external_tool_capability("ElmerSolver", executable_name="ElmerSolver"),
        _external_tool_capability("optiland", module_name="optiland"),
    ]
    publication = [
        ToolCapabilityItem(
            tool_name="testpypi_upload",
            tool_kind="publication",
            available=False,
            default_allowed=False,
            status="disabled_not_exposed",
            detection_method="policy",
            notes=["No TestPyPI upload endpoint or UI control is exposed."],
        ),
        ToolCapabilityItem(
            tool_name="pypi_publish",
            tool_kind="publication",
            available=False,
            default_allowed=False,
            status="disabled_not_exposed",
            detection_method="policy",
            notes=["PyPI is not published and publication approval is not granted."],
        ),
        ToolCapabilityItem(
            tool_name="tag_or_release_create",
            tool_kind="release",
            available=False,
            default_allowed=False,
            status="disabled_not_exposed",
            detection_method="policy",
            notes=["No tag or GitHub release endpoint is exposed."],
        ),
    ]
    return ToolCapabilitiesResponse(
        internal_tools=internal,
        external_solvers=external,
        publication_release_controls=publication,
        diagnostics=ApiDiagnostic(
            warnings=["External solver availability is detected only; solvers are not executed."],
            limitations=["Availability does not imply validation or production readiness."],
        ),
        recommended_next_actions=[
            "Use /api/agent-session to inspect the tool-call ledger for a concrete task.",
            "Run scripts/audit_sub_agents.py for installed/callable/executed status.",
        ],
    )


@router.get("/api/backend-capability-report", response_model=BackendCapabilityReport)
def agent_backend_capability_report():
    """Report what backend capabilities are importable, callable, and executed."""

    return generate_backend_capability_report()


@router.get("/api/backend-evidence-summary", response_model=BackendEvidencePack)
def agent_backend_evidence_summary():
    """Return a maintainer-facing backend evidence summary."""

    return generate_backend_evidence_pack()


@router.get(
    "/api/backend-validation-maturity",
    response_model=BackendValidationMaturityResponse,
)
def agent_backend_validation_maturity():
    """Return conservative backend validation maturity and preview boundaries."""

    return build_backend_validation_maturity_summary()


@router.get("/api/design-case-cross-checks", response_model=DesignCaseCrossChecksResponse)
def agent_design_case_cross_checks():
    """Cross-check local optical design examples against backend task sessions."""

    return cross_check_all_design_cases()


@router.get(
    "/api/application-domain-benchmarks",
    response_model=ApplicationDomainBenchmarkResponse,
)
def agent_application_domain_benchmarks():
    """List local application-domain benchmark scenarios."""

    return application_domain_benchmark_response()


@router.get(
    "/api/application-domain-benchmark-results",
    response_model=ApplicationDomainBenchmarkResultResponse,
)
def agent_application_domain_benchmark_results():
    """Evaluate all application-domain benchmark scenarios."""

    return evaluate_all_domain_scenarios()


@router.post(
    "/api/application-domain-benchmarks/{scenario_id}/evaluate",
    response_model=ApplicationDomainScenarioResult,
    responses=API_ERROR_RESPONSES,
)
def agent_application_domain_benchmark_evaluate(scenario_id: str):
    """Evaluate one application-domain benchmark scenario."""

    try:
        return evaluate_domain_scenario(scenario_id)
    except ValueError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=[
                    "Use /api/application-domain-benchmarks to inspect supported scenarios."
                ],
            )
        )


@router.get(
    "/api/application-domain-benchmarks/{scenario_id}",
    response_model=ApplicationDomainScenarioResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_application_domain_benchmark_detail(scenario_id: str):
    """Return one application-domain benchmark scenario."""

    try:
        return ApplicationDomainScenarioResponse(scenario=get_domain_scenario(scenario_id))
    except ValueError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=[
                    "Use /api/application-domain-benchmarks to inspect supported scenarios."
                ],
            )
        )


@router.get("/api/application-domains", response_model=ApplicationDomainsResponse)
def agent_application_domains():
    """List local application-domain coverage for backend optical design previews."""

    domains = list_application_domains()
    return ApplicationDomainsResponse(
        domains=domains,
        domain_count=len(domains),
    )


@router.post(
    "/api/application-domains/match",
    response_model=ApplicationDomainMatchResult,
    responses=API_ERROR_RESPONSES,
)
def agent_application_domain_match(req: ApplicationDomainMatchRequest):
    goal = req.goal.strip()
    if not goal:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Application-domain matching requires a non-empty goal.",
                diagnostics=ApiDiagnostic(errors=["goal must be a non-empty string."]),
                recommended_next_actions=[
                    "Provide a natural-language optical design goal."
                ],
            )
        )
    if req.language not in (None, "en", "zh-CN"):
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "language must be 'en' or 'zh-CN' when provided.",
                diagnostics=ApiDiagnostic(errors=["Unsupported language hint."]),
                recommended_next_actions=["Use language='en', language='zh-CN', or omit language."],
            )
        )
    return match_goal_to_application_domains(goal)


@router.get(
    "/api/application-domain-cross-checks",
    response_model=ApplicationDomainCrossChecksResponse,
)
def agent_application_domain_cross_checks():
    """Cross-check all application domains against material/template/tool coverage."""

    return cross_check_all_application_domains()


@router.get(
    "/api/application-domains/{domain_id}/cross-check",
    response_model=ApplicationDomainCrossChecksResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_application_domain_cross_check(domain_id: str):
    try:
        check = cross_check_application_domain(domain_id)
    except ValueError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=[
                    "Use /api/application-domains to inspect supported domains."
                ],
            )
        )
    return ApplicationDomainCrossChecksResponse(
        status="needs_review" if check.status == "fail" else "ok",
        cross_checks=[check],
        summary={
            "total": 1,
            "pass": 1 if check.status == "pass" else 0,
            "warning": 1 if check.status == "warning" else 0,
            "fail": 1 if check.status == "fail" else 0,
            "preview_only": 1 if check.preview_only else 0,
        },
    )


@router.get(
    "/api/application-domains/{domain_id}",
    response_model=ApplicationDomainDetailResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_application_domain_detail(domain_id: str):
    try:
        domain = get_application_domain(domain_id)
    except ValueError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=[
                    "Use /api/application-domains to inspect supported domains."
                ],
            )
        )
    return ApplicationDomainDetailResponse(
        domain=domain,
        recommended_next_actions=[
            *domain.recommended_questions,
            "Use the domain cross-check endpoint before treating a case as covered.",
        ],
    )


@router.get(
    "/api/adapter-native-golden-coverage",
    response_model=AdapterGoldenCoverageReport,
)
def agent_adapter_native_golden_coverage():
    """Report adapter-native golden preview coverage without solver execution."""

    return build_adapter_golden_coverage_report()


@router.post(
    "/api/optics/thin-film",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_thin_film(req: ThinFilmCalculatorRequest):
    try:
        result = calculate_thin_film_stack(
            req.layers,
            req.wavelength_nm,
            incident_n=req.incident_n,
            substrate_n=req.substrate_n,
            incidence_angle_deg=req.incidence_angle_deg,
            polarization=req.polarization,
        )
    except Exception as exc:  # noqa: BLE001 - stable calculator API error.
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/thin-film-spectrum",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_thin_film_spectrum(req: ThinFilmSpectrumRequest):
    try:
        result = calculate_thin_film_spectrum(
            req.layers,
            req.wavelength_start_nm,
            req.wavelength_stop_nm,
            req.points,
            incident_n=req.incident_n,
            substrate_n=req.substrate_n,
            incidence_angle_deg=req.incidence_angle_deg,
            polarization=req.polarization,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/quarter-wave-ar",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_quarter_wave_ar(req: QuarterWaveARRequest):
    try:
        result = design_quarter_wave_ar_coating(
            req.substrate_n,
            req.target_wavelength_nm,
            incident_n=req.incident_n,
            coating_n=req.coating_n,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/paraxial-lens",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_paraxial_lens(req: ParaxialLensRequest):
    try:
        result = thin_lens(req.focal_length_mm, req.object_distance_mm)
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/paraxial-system",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_paraxial_system(req: ParaxialSystemRequest):
    try:
        result = compose_abcd(req.elements)
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/two-lens-relay",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_two_lens_relay(req: TwoLensRelayRequest):
    try:
        result = analyze_two_lens_relay(
            req.f1_mm,
            req.f2_mm,
            req.separation_mm,
            req.object_distance_mm,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/gaussian-beam",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_gaussian_beam(req: GaussianBeamRequest):
    try:
        result = propagate_gaussian_beam(req.wavelength_nm, req.waist_um, req.z_mm)
        # Include the z=0 parameter helper explicitly in the response path.
        base = gaussian_beam_parameters(req.wavelength_nm, req.waist_um)
        result.result["parameter_summary"] = base.result
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/gaussian-beam-series",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_gaussian_beam_series(req: GaussianBeamSeriesRequest):
    try:
        result = propagate_gaussian_beam_series(
            req.wavelength_nm,
            req.waist_um,
            req.z_start_mm,
            req.z_stop_mm,
            req.points,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/gaussian-beam-focus",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_gaussian_beam_focus(req: GaussianBeamFocusRequest):
    try:
        result = focus_gaussian_beam_thin_lens(
            req.wavelength_nm,
            req.input_waist_um,
            req.focal_length_mm,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/fiber-coupling",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_fiber_coupling(req: FiberCouplingRequest):
    try:
        result = gaussian_mode_overlap(
            waist_input_um=req.waist_input_um,
            waist_fiber_um=req.waist_fiber_um,
            lateral_offset_um=req.lateral_offset_um,
            angular_tilt_mrad=req.angular_tilt_mrad,
            wavelength_nm=req.wavelength_nm,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/polarization-jones",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_polarization_jones(req: PolarizationJonesRequest):
    try:
        input_jones = req.input_jones
        if input_jones is None:
            input_state = linear_polarization(req.input_angle_deg)
            input_jones = input_state.result["output_jones"]
        element_type = req.element_type.lower()
        if element_type == "polarizer":
            result = jones_linear_polarizer(input_jones, req.angle_deg)
        elif element_type == "state":
            result = (
                linear_polarization(req.input_angle_deg)
                if req.input_jones is None
                else summarize_polarization_state(input_jones)
            )
        elif element_type == "waveplate":
            result = jones_waveplate(input_jones, req.retardance_rad, req.fast_axis_deg)
        else:
            raise ValueError("element_type must be waveplate, polarizer, or state.")
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/waveguide-estimate",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_waveguide_estimate(req: WaveguideEstimateRequest):
    try:
        result = slab_waveguide_v_number(
            req.core_n,
            req.cladding_n,
            req.core_thickness_um,
            req.wavelength_nm,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/waveguide-sweep",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_waveguide_sweep(req: WaveguideSweepRequest):
    try:
        result = slab_waveguide_sweep(
            req.core_n,
            req.cladding_n,
            req.wavelength_nm,
            req.thickness_start_um,
            req.thickness_stop_um,
            req.points,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.post(
    "/api/optics/waveguide-single-mode-range",
    response_model=OpticalCalculatorResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optics_waveguide_single_mode_range(req: WaveguideSingleModeRangeRequest):
    try:
        result = suggest_single_mode_thickness_range(
            req.core_n,
            req.cladding_n,
            req.wavelength_nm,
        )
    except Exception as exc:  # noqa: BLE001
        return _agent_error_response(
            AgentApiError(
                "preview_generation_error",
                str(exc),
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
            )
        )
    return _optical_calculator_response(result)


@router.get("/api/materials", response_model=MaterialsResponse)
def agent_materials():
    return MaterialsResponse(
        materials=list_materials(),
        diagnostics=ApiDiagnostic(
            warnings=[
                "Local preview material catalog; verify optical constants independently."
            ],
            limitations=[
                "Material records are design-assist hints, not production-grade optical constants."
            ],
        ),
        recommended_next_actions=[
            "Use /api/materials/suggest for broad application-oriented material hints.",
            "Verify material constants before physical conclusions.",
        ],
    )


@router.post(
    "/api/materials/suggest",
    response_model=MaterialSuggestionResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_material_suggest(req: MaterialSuggestionRequest):
    suggestions = suggest_materials_for_application(req.application)
    return MaterialSuggestionResponse(
        application=req.application,
        suggested_materials=suggestions,
        diagnostics=ApiDiagnostic(
            warnings=[
                "Suggestions are local preview guidance and do not replace material-data review."
            ],
            limitations=[
                "No external material database lookup was performed."
            ],
            details={"wavelength_nm": req.wavelength_nm},
        ),
        recommended_next_actions=[
            "Inspect the suggested material records.",
            "Verify wavelength-dependent n/k before physical interpretation.",
        ],
    )


@router.post(
    "/api/materials/diagnose",
    response_model=MaterialDiagnoseResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_material_diagnose(req: MaterialDiagnoseRequest):
    material_id = req.material_id.strip()
    application = req.application.strip()
    if not material_id or not application:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Material diagnostics require material_id and application.",
                diagnostics=ApiDiagnostic(errors=["material_id and application must be non-empty strings."]),
                recommended_next_actions=[
                    "Provide a local preview material ID and an optical application phrase."
                ],
            )
        )
    diagnostic = diagnose_material_suitability(material_id, application)
    return MaterialDiagnoseResponse(
        diagnostic=diagnostic,
        diagnostics=ApiDiagnostic(
            warnings=[
                "Material suitability diagnostics are local preview guidance only.",
                "No external material database lookup was performed.",
            ],
            limitations=[
                "This response is not a production-grade optical constants record."
            ],
            missing_fields=diagnostic.missing_context,
        ),
        recommended_next_actions=[
            *diagnostic.recommended_verification,
            "Use material diagnostics as review prompts before any solver setup.",
        ],
    )


@router.get(
    "/api/materials/{material_id}",
    response_model=MaterialDetailResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_material_detail(material_id: str):
    material = get_material(material_id)
    if material is None:
        return _agent_error_response(
            AgentApiError(
                "unsupported_material",
                f"Unknown material: {material_id}",
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[f"Unknown material: {material_id}"]),
                recommended_next_actions=["Use /api/materials to inspect supported local preview materials."],
            )
        )
    return MaterialDetailResponse(
        material=material,
        diagnostics=ApiDiagnostic(
            warnings=[
                "Material constants are approximate preview values unless stronger provenance is documented."
            ],
            limitations=[
                "This response is not a production-grade optical constants record."
            ],
        ),
        recommended_next_actions=[
            "Verify this material against trusted optical data before physical conclusions.",
            "Use /api/agent-trace to see how a local agent workflow would use this material.",
        ],
    )


@router.get("/api/examples", response_model=ExamplesResponse)
def agent_examples():
    return ExamplesResponse(
        examples=list_optical_design_examples(),
        diagnostics=ApiDiagnostic(
            warnings=[
                "Examples are local preview workflows; no solver or external LLM was used."
            ],
            limitations=[
                "Example outputs do not imply production-grade physical validation."
            ],
        ),
        recommended_next_actions=[
            "Load an example in Agent Studio Example Gallery.",
            "Review materials, adapter recommendation, and agent trace timeline.",
        ],
    )


@router.get("/api/design-requirements", response_model=DesignRequirementsResponse)
def agent_design_requirements():
    templates = list_requirement_templates()
    return DesignRequirementsResponse(
        templates=templates,
        template_count=len(templates),
        recommended_next_actions=[
            "Use /api/design-requirements/match to map a natural-language goal.",
            "Inspect expected_tool_calls before running an agent session.",
            "Keep outputs preview/design-assist and review missing inputs.",
        ],
    )


@router.post(
    "/api/design-requirements/match",
    response_model=RequirementMatchResult,
    responses=API_ERROR_RESPONSES,
)
def agent_design_requirement_match(req: DesignRequirementMatchRequest):
    goal = req.goal.strip()
    if not goal:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Design requirement matching requires a non-empty goal.",
                diagnostics=ApiDiagnostic(errors=["goal must be a non-empty string."]),
                recommended_next_actions=[
                    "Provide a natural-language optical design goal."
                ],
            )
        )
    if req.language not in (None, "en", "zh-CN"):
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "language must be 'en' or 'zh-CN' when provided.",
                diagnostics=ApiDiagnostic(errors=["Unsupported language hint."]),
                recommended_next_actions=["Use language='en', language='zh-CN', or omit language."],
            )
        )
    return match_goal_to_template(goal)


@router.get(
    "/api/design-requirements/{template_id}",
    response_model=DesignRequirementDetailResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_design_requirement_detail(template_id: str):
    try:
        template = get_requirement_template(template_id)
    except ValueError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=[
                    "Use /api/design-requirements to inspect available templates."
                ],
            )
        )
    return DesignRequirementDetailResponse(
        template=template,
        recommended_next_actions=template.next_actions,
    )


@router.post(
    "/api/optical-language/infer",
    response_model=SourceMonitorInference,
    responses=API_ERROR_RESPONSES,
)
def agent_optical_language_infer(req: OpticalLanguageInferRequest):
    goal = req.goal.strip()
    if not goal:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Optical-language inference requires a non-empty goal.",
                diagnostics=ApiDiagnostic(errors=["goal must be a non-empty string."]),
                recommended_next_actions=[
                    "Provide a local optical design goal with source and observable context."
                ],
            )
        )
    if req.language not in (None, "en", "zh-CN"):
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "language must be 'en' or 'zh-CN' when provided.",
                diagnostics=ApiDiagnostic(errors=["Unsupported language hint."]),
                recommended_next_actions=["Use language='en', language='zh-CN', or omit language."],
            )
        )
    if req.template_id is not None:
        try:
            get_requirement_template(req.template_id)
        except ValueError as exc:
            return _agent_error_response(
                AgentApiError(
                    "invalid_workflow_request",
                    str(exc),
                    status_code=404,
                    diagnostics=ApiDiagnostic(errors=[str(exc)]),
                    recommended_next_actions=[
                        "Use /api/design-requirements to inspect supported templates."
                    ],
                )
            )
    return infer_source_monitor_from_goal(goal, template_id=req.template_id)


@router.post(
    "/api/optical-language/diagnose",
    response_model=OpticalLanguageDiagnoseResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_optical_language_diagnose(req: OpticalLanguageDiagnoseRequest):
    goal = req.goal.strip()
    if not goal:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Optical-language diagnostics require a non-empty goal.",
                diagnostics=ApiDiagnostic(errors=["goal must be a non-empty string."]),
                recommended_next_actions=["Provide a local optical design goal."],
            )
        )
    if req.language not in (None, "en", "zh-CN"):
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "language must be 'en' or 'zh-CN' when provided.",
                diagnostics=ApiDiagnostic(errors=["Unsupported language hint."]),
                recommended_next_actions=["Use language='en', language='zh-CN', or omit language."],
            )
        )
    inference = infer_source_monitor_from_goal(goal, template_id=req.template_id)
    diagnostics = diagnose_missing_inputs(
        goal=goal,
        template_id=inference.matched_template_id,
        spec=req.spec,
    )
    # Re-run with template defaults when the caller did not provide explicit spec constraints.
    if not req.spec:
        diagnostics = inference.diagnostics
    return OpticalLanguageDiagnoseResponse(
        status="ok" if diagnostics.safe_to_preview else "needs_review",
        matched_template_id=inference.matched_template_id,
        missing_required_inputs=diagnostics.missing_required_inputs,
        missing_critical_inputs=diagnostics.missing_critical_inputs,
        missing_optional_inputs=diagnostics.missing_optional_inputs,
        default_assumptions_applied=diagnostics.default_assumptions_applied,
        ambiguity_notes=diagnostics.ambiguity_notes,
        blocking_questions=diagnostics.blocking_questions,
        safe_to_preview=diagnostics.safe_to_preview,
        safe_to_run_solver=diagnostics.safe_to_run_solver,
        diagnostics=ApiDiagnostic(
            missing_fields=diagnostics.missing_required_inputs,
            assumptions=diagnostics.default_assumptions_applied,
            warnings=diagnostics.ambiguity_notes,
            limitations=[
                "Diagnostics are preview/design-assist only.",
                "safe_to_run_solver is false by default.",
            ],
        ),
        recommended_next_actions=[
            "Review missing source/monitor inputs.",
            "Confirm default assumptions before optional solver setup.",
            "Use /api/agent-session to inspect the full tool-call ledger.",
        ],
    )


@router.post(
    "/api/optical-language/observables/diagnose",
    response_model=OpticalLanguageObservableDiagnoseResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_observable_diagnose(req: OpticalLanguageObservableDiagnoseRequest):
    goal = req.goal.strip()
    if not goal:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Observable diagnostics require a non-empty goal.",
                diagnostics=ApiDiagnostic(errors=["goal must be a non-empty string."]),
                recommended_next_actions=["Provide a local optical design goal."],
            )
        )
    if req.language not in (None, "en", "zh-CN"):
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "language must be 'en' or 'zh-CN' when provided.",
                diagnostics=ApiDiagnostic(errors=["Unsupported language hint."]),
                recommended_next_actions=["Use language='en', language='zh-CN', or omit language."],
            )
        )
    inference = infer_source_monitor_from_goal(goal, template_id=req.template_id)
    source_model = req.source_model or inference.source_model
    monitor_model = req.monitor_model or inference.monitor_model
    observable_diagnostics = diagnose_observable(
        source_model,
        monitor_model,
        template_id=inference.matched_template_id,
    )
    warnings = [
        warning
        for diagnostic in observable_diagnostics
        for warning in diagnostic.warnings
    ]
    return OpticalLanguageObservableDiagnoseResponse(
        matched_template_id=inference.matched_template_id,
        source_model=source_model,
        monitor_model=monitor_model,
        observable_diagnostics=observable_diagnostics,
        diagnostics=ApiDiagnostic(
            warnings=warnings,
            limitations=[
                "Observable diagnostics are preview/design-assist metadata.",
                "Real solver results require explicit solver execution outside this endpoint.",
            ],
        ),
        recommended_next_actions=[
            "Review required_inputs for each observable before solver setup.",
            "Use /api/optical-language/adapter-mapping to inspect adapter-native preview semantics.",
        ],
    )


@router.post(
    "/api/optical-language/adapter-mapping",
    response_model=OpticalLanguageAdapterMappingResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_adapter_source_monitor_mapping(req: OpticalLanguageAdapterMappingRequest):
    goal = req.goal.strip()
    if not goal:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Adapter source/monitor mapping requires a non-empty goal.",
                diagnostics=ApiDiagnostic(errors=["goal must be a non-empty string."]),
                recommended_next_actions=["Provide a local optical design goal."],
            )
        )
    if req.language not in (None, "en", "zh-CN"):
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "language must be 'en' or 'zh-CN' when provided.",
                diagnostics=ApiDiagnostic(errors=["Unsupported language hint."]),
                recommended_next_actions=["Use language='en', language='zh-CN', or omit language."],
            )
        )
    inference = infer_source_monitor_from_goal(goal, template_id=req.template_id)
    source_model = req.source_model or inference.source_model
    monitor_model = req.monitor_model or inference.monitor_model
    observable_diagnostics = diagnose_observable(
        source_model,
        monitor_model,
        template_id=inference.matched_template_id,
    )
    adapter_mapping = map_source_monitor_to_adapter(
        req.adapter_name,
        source_model,
        monitor_model,
        observable_diagnostics,
    )
    return OpticalLanguageAdapterMappingResponse(
        matched_template_id=inference.matched_template_id,
        source_model=source_model,
        monitor_model=monitor_model,
        observable_diagnostics=observable_diagnostics,
        adapter_source_monitor_mapping=adapter_mapping,
        diagnostics=ApiDiagnostic(
            warnings=adapter_mapping.warnings,
            limitations=[
                "Adapter-native mapping is preview metadata only.",
                "No adapter or external solver process was executed.",
            ],
        ),
        recommended_next_actions=[
            "Inspect supported_observables and unsupported_observables.",
            "Use /api/adapter-preview for scaffold content; run solvers only after explicit approval.",
        ],
    )


@router.get(
    "/api/examples/{example_id}",
    response_model=ExampleDetailResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_example_detail(example_id: str):
    try:
        example = get_optical_design_example(example_id)
    except ExampleRegistryError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=["Use /api/examples to inspect available local examples."],
            )
        )
    return ExampleDetailResponse(
        example=example,
        diagnostics=ApiDiagnostic(
            warnings=[
                "Loaded local example only; no solver or external LLM was called."
            ],
            limitations=[
                "Example material and adapter choices are preview guidance only."
            ],
        ),
        recommended_next_actions=example.recommended_next_actions,
    )


@router.post(
    "/api/examples/{example_id}/agent-trace",
    response_model=AgentTraceResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_example_trace(example_id: str):
    try:
        trace = build_example_agent_trace(example_id)
    except ExampleRegistryError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=["Use /api/examples to inspect available local examples."],
            )
        )
    return _agent_trace_response(trace)


@router.post(
    "/api/agent-trace",
    response_model=AgentTraceResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_collaboration_trace(req: AgentTraceRequest):
    if req.text is None and req.spec is None and req.example_id is None:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Provide text, spec, or example_id for an agent collaboration trace.",
                diagnostics=ApiDiagnostic(errors=["Agent trace requires text, spec, or example_id."]),
                recommended_next_actions=[
                    "Use example_id='nanoparticle_plasmonics' or provide a local spec/text request."
                ],
            )
        )
    request_payload: dict[str, Any] = {}
    if req.text is not None:
        request_payload["text"] = req.text
    if req.spec is not None:
        request_payload["spec"] = req.spec
    if req.example_id is not None:
        request_payload["example_id"] = req.example_id
    if req.example_id is not None and req.text is None and req.spec is None:
        try:
            trace = build_example_agent_trace(req.example_id)
        except ExampleRegistryError:
            trace = build_agent_trace(request_payload)
    else:
        trace = build_agent_trace(request_payload)
    return _agent_trace_response(trace)


@router.post(
    "/api/agent-session",
    response_model=AgentTaskSessionResponse,
    responses=API_ERROR_RESPONSES,
)
def agent_task_session(req: AgentSessionRequest):
    goal = req.goal.strip()
    if not goal:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "Agent task session requires a non-empty goal.",
                diagnostics=ApiDiagnostic(errors=["goal must be a non-empty string."]),
                recommended_next_actions=[
                    "Describe a local optical design goal, for example a nanoparticle scattering preview."
                ],
            )
        )
    if req.language not in (None, "en", "zh-CN"):
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                "language must be 'en' or 'zh-CN' when provided.",
                diagnostics=ApiDiagnostic(errors=["Unsupported language hint."]),
                recommended_next_actions=["Use language='en', language='zh-CN', or omit language."],
            )
        )
    try:
        session = build_agent_task_session(goal, example_id=req.example_id)
    except ExampleRegistryError as exc:
        return _agent_error_response(
            AgentApiError(
                "invalid_workflow_request",
                str(exc),
                status_code=404,
                diagnostics=ApiDiagnostic(errors=[str(exc)]),
                recommended_next_actions=["Use /api/examples to inspect available local design cases."],
            )
        )
    return _agent_session_response(session)


def _agent_trace_response(trace: Any) -> AgentTraceResponse:
    return AgentTraceResponse(
        trace_id=trace.trace_id,
        example_id=trace.example_id,
        design_goal=trace.design_goal,
        timeline_summary=trace.timeline_summary,
        agents=trace.agents,
        final_recommendation=trace.final_recommendation,
        material_suggestions=trace.material_suggestions,
        adapter_recommendation=trace.adapter_recommendation,
        diagnostics=ApiDiagnostic(
            warnings=[
                "Sub-agent collaboration is a deterministic local preview trace, not autonomous external agents."
            ],
            limitations=[
                "No external LLM, external solver, network, upload, tag, or release action was performed."
            ],
        ),
        recommended_next_actions=trace.recommended_next_actions,
    )


def _agent_session_response(session: Any) -> AgentTaskSessionResponse:
    trace = _agent_trace_response(session.agent_trace)
    return AgentTaskSessionResponse(
        status=session.status,
        session_id=session.session_id,
        user_goal=session.user_goal,
        requirement_template_id=session.requirement_template_id,
        optical_intent_summary=session.optical_intent_summary,
        optical_language_summary=session.optical_language_summary,
        source_model=session.source_model,
        monitor_model=session.monitor_model,
        optical_language_diagnostics=session.optical_language_diagnostics,
        observable_diagnostics=session.observable_diagnostics,
        adapter_source_monitor_mapping=session.adapter_source_monitor_mapping,
        match_confidence=session.match_confidence,
        candidate_templates=session.candidate_templates,
        recommended_questions=session.recommended_questions,
        application_domain_id=session.application_domain_id,
        application_domain_candidates=session.application_domain_candidates,
        domain_material_suitability_summary=session.domain_material_suitability_summary,
        domain_cross_check_status=session.domain_cross_check_status,
        selected_example_id=session.selected_example_id,
        design_case_summary=session.design_case_summary,
        missing_required_inputs=session.missing_required_inputs,
        missing_critical_inputs=session.missing_critical_inputs,
        missing_optional_inputs=session.missing_optional_inputs,
        default_assumptions_applied=session.default_assumptions_applied,
        plan_steps=session.plan_steps,
        agent_trace=trace,
        artifacts=session.artifacts,
        permission_gates=session.permission_gates,
        tool_call_ledger=session.tool_call_ledger,
        final_recommendation=session.final_recommendation,
        diagnostics=ApiDiagnostic(
            warnings=[
                "Agent session is deterministic and local; it is not an autonomous external-agent run."
            ],
            limitations=[
                "No external solver, external LLM, network, upload, tag, or release action was performed."
            ],
        ),
        recommended_next_actions=session.recommended_next_actions,
    )


def _external_tool_capability(
    tool_name: str,
    *,
    module_name: str | None = None,
    executable_name: str | None = None,
) -> ToolCapabilityItem:
    module_available = importlib.util.find_spec(module_name) is not None if module_name else False
    executable_path = shutil.which(executable_name) if executable_name else None
    available = bool(module_available or executable_path)
    methods = []
    if module_name:
        methods.append(f"importlib.util.find_spec('{module_name}')")
    if executable_name:
        methods.append(f"shutil.which('{executable_name}')")
    notes = [
        "Availability detection only; no solver command was executed.",
        "External solver execution remains blocked by default.",
    ]
    if executable_path:
        notes.append(f"Executable '{executable_name}' is detectable on PATH.")
    if module_available:
        notes.append(f"Python module '{module_name}' is import-detectable.")
    return ToolCapabilityItem(
        tool_name=tool_name,
        tool_kind="external_solver",
        available=available,
        default_allowed=False,
        status="detectable_not_executed" if available else "not_detected_not_executed",
        detection_method="; ".join(methods) or "not checked",
        notes=notes,
    )


def _optical_calculator_response(result: Any) -> OpticalCalculatorResponse:
    return OpticalCalculatorResponse(
        status=result.status,
        result=result.result,
        assumptions=result.assumptions,
        limitations=result.limitations,
        warnings=result.warnings,
        quality=result.quality.model_dump(mode="json") if hasattr(result.quality, "model_dump") else result.quality,
        diagnostics=ApiDiagnostic(
            warnings=[
                "Calculator output is preview/design-assist only.",
                *result.warnings,
            ],
            limitations=result.limitations,
            details={"calculator_diagnostics": result.diagnostics},
        ),
        recommended_next_actions=[
            "Inspect assumptions before using the estimate.",
            "Verify with validated material data and solver studies before physical conclusions.",
        ],
    )


class AgentApiError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        status_code: int = 400,
        diagnostics: ApiDiagnostic | None = None,
        recommended_next_actions: list[str] | None = None,
    ) -> None:
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.diagnostics = diagnostics or ApiDiagnostic(errors=[message])
        self.recommended_next_actions = recommended_next_actions or [
            "Review the request payload and retry with local, documented inputs."
        ]


def _agent_error_response(error: AgentApiError) -> JSONResponse:
    payload = ApiErrorResponse(
        error_code=error.error_code,
        message=error.message,
        diagnostics=error.diagnostics,
        recommended_next_actions=error.recommended_next_actions,
    )
    return JSONResponse(
        status_code=error.status_code,
        content=payload.model_dump(mode="json"),
    )


def _local_parser(parser: str) -> str:
    normalized = (parser or "heuristic").strip().lower()
    if normalized in {"heuristic", "local"}:
        return "rule"
    if normalized == "rule":
        return normalized
    raise AgentApiError(
        "external_llm_not_enabled",
        "The local Agent API only allows heuristic/rule parsing by default.",
        diagnostics=ApiDiagnostic(errors=["Parser must be heuristic or rule."]),
        recommended_next_actions=["Use parser='heuristic' or parser='rule'."],
    )


def _load_spec(spec_payload: dict[str, Any] | None, path: str | None) -> OpticalSpec:
    if spec_payload is None and path is None:
        raise AgentApiError(
            "invalid_spec",
            "Provide spec or local path.",
            recommended_next_actions=[
                "Send an inline OpticalSpec as spec or a repo-local JSON path."
            ],
        )
    data = spec_payload if spec_payload is not None else _load_json_file(path or "")
    if isinstance(data, dict) and "spec" in data and isinstance(data["spec"], dict):
        data = data["spec"]
    try:
        return OpticalSpec.model_validate(data)
    except Exception as exc:  # noqa: BLE001 - surface validation details as API diagnostics.
        raise AgentApiError(
            "invalid_spec",
            f"Invalid OpticalSpec: {exc}",
            diagnostics=ApiDiagnostic(errors=[str(exc)]),
        ) from exc


def _load_workflow_input_text(path: str) -> str | None:
    data = _load_json_file(path)
    if isinstance(data, dict):
        value = data.get("input_text") or data.get("text")
        if isinstance(value, str) and value.strip():
            return value
    return None


def _load_json_file(path: str) -> Any:
    local_path = _resolve_local_path(path)
    try:
        return json.loads(local_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AgentApiError(
            "invalid_json",
            f"Invalid JSON file: {path}",
            diagnostics=ApiDiagnostic(errors=[str(exc)]),
        ) from exc


def _resolve_local_path(path: str) -> Path:
    if "://" in path:
        raise AgentApiError(
            "invalid_workflow_request",
            "Network paths are not supported.",
            recommended_next_actions=["Use a repo-local JSON fixture path."],
        )
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise AgentApiError(
            "invalid_workflow_request",
            "Path must stay inside the repository.",
            recommended_next_actions=["Use a repo-local path under examples/ or docs/."],
        ) from exc
    if not resolved.exists():
        raise AgentApiError(
            "invalid_workflow_request",
            f"Local path not found: {path}",
            status_code=404,
            recommended_next_actions=["Check the path and retry with an existing local file."],
        )
    return resolved


def _workflow_text_from_spec(spec: OpticalSpec) -> str:
    for field in (spec.task.research_goal, spec.task.task_name):
        value = getattr(field, "value", None)
        if isinstance(value, str) and value.strip():
            return value
    return "Create a local optical workflow preview from the provided OpticalSpec."
