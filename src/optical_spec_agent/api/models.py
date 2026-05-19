"""Pydantic models for the local Agent API surface."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from optical_spec_agent.agents.models import AgentStep
from optical_spec_agent.agents.task_session import (
    AgentArtifact,
    AgentPlanStep,
    PermissionGate,
    ToolCallRecord,
)
from optical_spec_agent.examples.models import (
    OpticalDesignExampleDetail,
    OpticalDesignExampleSummary,
)
from optical_spec_agent.examples.application_domains import (
    ApplicationDomain,
    ApplicationDomainDetailResponse,
    ApplicationDomainMatchResult,
    ApplicationDomainsResponse,
)
from optical_spec_agent.examples.domain_cross_check import (
    ApplicationDomainCrossCheck,
    ApplicationDomainCrossChecksResponse,
)
from optical_spec_agent.examples.domain_benchmarks import (
    ApplicationDomainBenchmarkResponse,
    ApplicationDomainBenchmarkResultResponse,
    ApplicationDomainScenario,
    ApplicationDomainScenarioResponse,
    ApplicationDomainScenarioResult,
)
from optical_spec_agent.examples.requirements import (
    DesignRequirementDetailResponse,
    DesignRequirementsResponse,
    RequirementMatchResult,
)
from optical_spec_agent.materials.models import (
    MaterialDetail,
    MaterialSuitabilityDiagnostic,
    MaterialSummary,
)
from optical_spec_agent.optical_language import (
    AdapterSourceMonitorMapping,
    ObservableDiagnostic,
    OpticalLanguageDiagnostics,
    OpticalMonitorModel,
    OpticalSourceModel,
    SourceMonitorInference,
)


API_CONTRACT_VERSION = "0.1"


class ApiSafetyFlags(BaseModel):
    """Shared default safety flags for local preview-first API responses."""

    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApiDiagnostic(BaseModel):
    """Structured diagnostics intended for frontend rendering."""

    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)


class ApiResponseBase(ApiSafetyFlags):
    """Base response fields shared by local Agent API endpoints."""

    api_contract_version: str = API_CONTRACT_VERSION
    status: str = "ok"
    diagnostics: ApiDiagnostic = Field(default_factory=ApiDiagnostic)
    recommended_next_actions: list[str] = Field(default_factory=list)


class HealthResponse(ApiResponseBase):
    service: str = "optical-spec-agent"


class VersionResponse(ApiResponseBase):
    package_version: str
    current_public_prerelease: str
    main_development_version: str
    pypi_published: bool = False
    testpypi_verified: bool = True
    testpypi_verified_version: str = "0.9.0rc6.dev0"


class AdapterSummary(BaseModel):
    tool_name: str
    display_name: str
    solver_family: str
    current_status: str
    maturity_level: str
    evidence: str | None = None
    external_solver_required_by_default: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
    limitations: list[str] = Field(default_factory=list)


class AdaptersResponse(ApiResponseBase):
    adapters: list[AdapterSummary] = Field(default_factory=list)


class SchemaResponse(ApiResponseBase):
    model_config = ConfigDict(populate_by_name=True)

    schema_name: str = "OpticalSpec"
    json_schema: dict[str, Any] = Field(alias="schema")


class ApiRequestBase(BaseModel):
    """Base request model for explicit frontend-facing Agent API requests."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ParseRequest(ApiRequestBase):
    text: str = Field(..., description="Natural language optical task description")
    task_id: str = Field("", description="Optional task ID")
    parser: str = Field("heuristic", description="Local parser mode: heuristic or rule")
    json_output: bool = Field(True, alias="json", description="Return JSON response")


class ParseResponse(ApiResponseBase):
    parser: str = "rule"
    spec: dict[str, Any]
    summary: str


class ValidateRequest(ApiRequestBase):
    spec: dict[str, Any] | None = Field(None, description="Inline OpticalSpec JSON")
    path: str | None = Field(None, description="Local repo-relative JSON spec path")


class ValidateResponse(ApiResponseBase):
    valid: bool = False


class WorkflowPlanRequest(ValidateRequest):
    text: str | None = Field(None, description="Natural language workflow request")
    parser: str = Field("heuristic", description="Local parser mode: heuristic or rule")
    tool: str = Field("auto", description="Adapter tool hint")


class WorkflowPlanResponse(ApiResponseBase):
    workflow_plan: dict[str, Any]
    public_top_level_keys: list[str] = Field(default_factory=list)


class AdapterPreviewRequest(ValidateRequest):
    tool: str = Field("auto", description="Adapter tool hint")


class AdapterPreviewResponse(ApiResponseBase):
    tool: str
    display_name: str
    output_language: str
    output_extension: str
    preview_content: str = ""
    artifact_summary: dict[str, Any] = Field(default_factory=dict)
    source_model: OpticalSourceModel | None = None
    monitor_model: OpticalMonitorModel | None = None
    observable_diagnostics: list[ObservableDiagnostic] = Field(default_factory=list)
    adapter_source_monitor_mapping: AdapterSourceMonitorMapping | None = None
    preview_only: bool = True
    solver_execution_required_for_real_result: bool = False
    warnings: list[str] = Field(default_factory=list)


class ValidationEvidenceItem(BaseModel):
    tool_name: str
    display_name: str
    maturity_level: str
    evidence: str | None = None
    status_note: str
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ValidationEvidenceResponse(ApiResponseBase):
    validation_evidence: list[ValidationEvidenceItem] = Field(default_factory=list)


class ReadinessResponse(ApiResponseBase):
    current_public_prerelease: str
    main_development_version: str
    testpypi: dict[str, Any]
    pypi: dict[str, Any]
    public_contract_freeze: dict[str, Any]
    adapter_maturity: dict[str, str]
    v1_0_0_released: bool = False


class MaterialsResponse(ApiResponseBase):
    materials: list[MaterialSummary] = Field(default_factory=list)
    catalog_status: str = "local_preview_catalog"
    catalog_note: str = (
        "Material data is a local preview/design-assist catalog and not a "
        "production-grade optical constants database."
    )


class MaterialDetailResponse(ApiResponseBase):
    material: MaterialDetail
    catalog_status: str = "local_preview_catalog"
    catalog_note: str = (
        "Verify material constants before drawing physical conclusions."
    )


class MaterialSuggestionRequest(ApiRequestBase):
    application: str = Field(..., description="Optical application phrase")
    wavelength_nm: float | None = Field(None, description="Optional design wavelength")


class MaterialSuggestionResponse(ApiResponseBase):
    application: str
    suggested_materials: list[MaterialSummary] = Field(default_factory=list)
    catalog_status: str = "local_preview_catalog"
    catalog_note: str = (
        "Suggestions are local preview guidance only; verify material data independently."
    )


class MaterialDiagnoseRequest(ApiRequestBase):
    material_id: str = Field(..., description="Local preview material ID or alias")
    application: str = Field(..., description="Optical application phrase")


class MaterialDiagnoseResponse(ApiResponseBase):
    diagnostic: MaterialSuitabilityDiagnostic
    catalog_status: str = "local_preview_catalog"
    catalog_note: str = (
        "Suitability diagnostics are design-assist only; verify material data independently."
    )


class AgentTraceRequest(ApiRequestBase):
    spec: dict[str, Any] | None = Field(None, description="Inline OpticalSpec-like payload")
    text: str | None = Field(None, description="Natural language optical design request")
    example_id: str | None = Field(None, description="Local example identifier")


class AgentTraceResponse(ApiResponseBase):
    trace_id: str
    example_id: str | None = None
    design_goal: str = ""
    timeline_summary: str = ""
    agents: list[AgentStep] = Field(default_factory=list)
    final_recommendation: str
    material_suggestions: list[str] = Field(default_factory=list)
    adapter_recommendation: str = ""


class AgentSessionRequest(ApiRequestBase):
    goal: str = Field(..., description="Natural language optical design goal")
    example_id: str | None = Field(None, description="Optional local example identifier")
    language: str | None = Field(None, description="Optional UI language hint: en or zh-CN")


class AgentTaskSessionResponse(ApiResponseBase):
    session_id: str
    user_goal: str
    requirement_template_id: str | None = None
    optical_intent_summary: str
    optical_language_summary: dict[str, str] = Field(default_factory=dict)
    source_model: OpticalSourceModel | None = None
    monitor_model: OpticalMonitorModel | None = None
    optical_language_diagnostics: OpticalLanguageDiagnostics = Field(
        default_factory=OpticalLanguageDiagnostics
    )
    observable_diagnostics: list[ObservableDiagnostic] = Field(default_factory=list)
    adapter_source_monitor_mapping: AdapterSourceMonitorMapping | None = None
    match_confidence: str = "low"
    candidate_templates: list[str] = Field(default_factory=list)
    recommended_questions: list[str] = Field(default_factory=list)
    application_domain_id: str | None = None
    application_domain_candidates: list[str] = Field(default_factory=list)
    domain_material_suitability_summary: list[dict[str, Any]] = Field(default_factory=list)
    domain_cross_check_status: str = "not_checked"
    selected_example_id: str | None = None
    design_case_summary: str
    missing_required_inputs: list[str] = Field(default_factory=list)
    missing_critical_inputs: list[str] = Field(default_factory=list)
    missing_optional_inputs: list[str] = Field(default_factory=list)
    default_assumptions_applied: list[str] = Field(default_factory=list)
    plan_steps: list[AgentPlanStep] = Field(default_factory=list)
    agent_trace: AgentTraceResponse
    artifacts: list[AgentArtifact] = Field(default_factory=list)
    permission_gates: list[PermissionGate] = Field(default_factory=list)
    tool_call_ledger: list[ToolCallRecord] = Field(default_factory=list)
    final_recommendation: str


class DesignRequirementMatchRequest(ApiRequestBase):
    goal: str = Field(..., description="Natural language optical design goal")
    language: str | None = Field(None, description="Optional language hint: en or zh-CN")


class ApplicationDomainMatchRequest(ApiRequestBase):
    goal: str = Field(..., description="Natural language optical design goal")
    language: str | None = Field(None, description="Optional language hint: en or zh-CN")


class OpticalLanguageInferRequest(ApiRequestBase):
    goal: str = Field(..., description="Natural language optical design goal")
    template_id: str | None = Field(None, description="Optional design requirement template id")
    language: str | None = Field(None, description="Optional language hint: en or zh-CN")


class OpticalLanguageDiagnoseRequest(ApiRequestBase):
    goal: str = Field(..., description="Natural language optical design goal")
    spec: dict[str, Any] | None = Field(None, description="Optional partial spec payload")
    template_id: str | None = Field(None, description="Optional design requirement template id")
    language: str | None = Field(None, description="Optional language hint: en or zh-CN")


class OpticalLanguageDiagnoseResponse(ApiResponseBase):
    matched_template_id: str | None = None
    missing_required_inputs: list[str] = Field(default_factory=list)
    missing_critical_inputs: list[str] = Field(default_factory=list)
    missing_optional_inputs: list[str] = Field(default_factory=list)
    default_assumptions_applied: list[str] = Field(default_factory=list)
    ambiguity_notes: list[str] = Field(default_factory=list)
    blocking_questions: list[str] = Field(default_factory=list)
    safe_to_preview: bool = True
    safe_to_run_solver: bool = False


class OpticalLanguageObservableDiagnoseRequest(ApiRequestBase):
    goal: str = Field(..., description="Natural language optical design goal")
    template_id: str | None = Field(None, description="Optional design requirement template id")
    source_model: OpticalSourceModel | None = None
    monitor_model: OpticalMonitorModel | None = None
    language: str | None = Field(None, description="Optional language hint: en or zh-CN")


class OpticalLanguageObservableDiagnoseResponse(ApiResponseBase):
    matched_template_id: str | None = None
    source_model: OpticalSourceModel
    monitor_model: OpticalMonitorModel
    observable_diagnostics: list[ObservableDiagnostic] = Field(default_factory=list)


class OpticalLanguageAdapterMappingRequest(ApiRequestBase):
    adapter_name: str = Field(..., description="Adapter name such as meep, mpb, gmsh, elmer, optiland")
    goal: str = Field(..., description="Natural language optical design goal")
    template_id: str | None = Field(None, description="Optional design requirement template id")
    source_model: OpticalSourceModel | None = None
    monitor_model: OpticalMonitorModel | None = None
    language: str | None = Field(None, description="Optional language hint: en or zh-CN")


class OpticalLanguageAdapterMappingResponse(ApiResponseBase):
    matched_template_id: str | None = None
    source_model: OpticalSourceModel
    monitor_model: OpticalMonitorModel
    observable_diagnostics: list[ObservableDiagnostic] = Field(default_factory=list)
    adapter_source_monitor_mapping: AdapterSourceMonitorMapping


__all_optical_language_models__ = [
    "AdapterSourceMonitorMapping",
    "ObservableDiagnostic",
    "OpticalLanguageAdapterMappingRequest",
    "OpticalLanguageAdapterMappingResponse",
    "OpticalLanguageDiagnoseResponse",
    "OpticalLanguageInferRequest",
    "OpticalLanguageDiagnoseRequest",
    "OpticalLanguageObservableDiagnoseRequest",
    "OpticalLanguageObservableDiagnoseResponse",
    "SourceMonitorInference",
]


__all_requirement_models__ = [
    "ApplicationDomain",
    "ApplicationDomainCrossCheck",
    "ApplicationDomainCrossChecksResponse",
    "ApplicationDomainDetailResponse",
    "ApplicationDomainBenchmarkResponse",
    "ApplicationDomainBenchmarkResultResponse",
    "ApplicationDomainMatchRequest",
    "ApplicationDomainMatchResult",
    "ApplicationDomainScenario",
    "ApplicationDomainScenarioResponse",
    "ApplicationDomainScenarioResult",
    "ApplicationDomainsResponse",
    "DesignRequirementDetailResponse",
    "DesignRequirementsResponse",
    "RequirementMatchResult",
]


class ToolCapabilityItem(BaseModel):
    tool_name: str
    tool_kind: str
    available: bool
    default_allowed: bool
    status: str
    detection_method: str
    notes: list[str] = Field(default_factory=list)


class ToolCapabilitiesResponse(ApiResponseBase):
    internal_tools: list[ToolCapabilityItem] = Field(default_factory=list)
    external_solvers: list[ToolCapabilityItem] = Field(default_factory=list)
    publication_release_controls: list[ToolCapabilityItem] = Field(default_factory=list)


class ThinFilmCalculatorRequest(ApiRequestBase):
    incident_n: float = 1.0
    substrate_n: float = 1.5
    layers: list[dict[str, Any]] = Field(default_factory=list)
    wavelength_nm: float
    incidence_angle_deg: float = 0.0
    polarization: str = "s"


class ThinFilmSpectrumRequest(ApiRequestBase):
    incident_n: float = 1.0
    substrate_n: float = 1.5
    layers: list[dict[str, Any]] = Field(default_factory=list)
    wavelength_start_nm: float
    wavelength_stop_nm: float
    points: int = 11
    incidence_angle_deg: float = 0.0
    polarization: str = "s"


class QuarterWaveARRequest(ApiRequestBase):
    incident_n: float = 1.0
    substrate_n: float
    target_wavelength_nm: float
    coating_n: float | None = None


class ParaxialLensRequest(ApiRequestBase):
    focal_length_mm: float
    object_distance_mm: float


class ParaxialSystemRequest(ApiRequestBase):
    elements: list[dict[str, Any]] = Field(default_factory=list)


class TwoLensRelayRequest(ApiRequestBase):
    f1_mm: float
    f2_mm: float
    separation_mm: float
    object_distance_mm: float


class GaussianBeamRequest(ApiRequestBase):
    wavelength_nm: float
    waist_um: float
    z_mm: float = 0.0


class GaussianBeamSeriesRequest(ApiRequestBase):
    wavelength_nm: float
    waist_um: float
    z_start_mm: float
    z_stop_mm: float
    points: int = 11


class GaussianBeamFocusRequest(ApiRequestBase):
    wavelength_nm: float
    input_waist_um: float
    focal_length_mm: float


class WaveguideEstimateRequest(ApiRequestBase):
    core_n: float
    cladding_n: float
    core_thickness_um: float
    wavelength_nm: float


class WaveguideSweepRequest(ApiRequestBase):
    core_n: float
    cladding_n: float
    wavelength_nm: float
    thickness_start_um: float
    thickness_stop_um: float
    points: int = 11


class WaveguideSingleModeRangeRequest(ApiRequestBase):
    core_n: float
    cladding_n: float
    wavelength_nm: float


class OpticalCalculatorResponse(ApiResponseBase):
    result: dict[str, Any] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    quality: dict[str, Any] = Field(default_factory=dict)


class ExamplesResponse(ApiResponseBase):
    examples: list[OpticalDesignExampleSummary] = Field(default_factory=list)
    gallery_status: str = "local_preview_examples"
    gallery_note: str = (
        "Examples are local preview workflows and do not run solvers or claim "
        "production-grade validation."
    )


class ExampleDetailResponse(ApiResponseBase):
    example: OpticalDesignExampleDetail
    gallery_status: str = "local_preview_examples"
    gallery_note: str = "Use these examples for local Agent Studio workflow preview."


class ApiErrorResponse(ApiResponseBase):
    status: str = "error"
    error_code: str
    message: str
