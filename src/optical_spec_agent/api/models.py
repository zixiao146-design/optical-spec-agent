"""Pydantic models for the local Agent API surface."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


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


class ParseRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    text: str = Field(..., description="Natural language optical task description")
    task_id: str = Field("", description="Optional task ID")
    parser: str = Field("heuristic", description="Local parser mode: heuristic or rule")
    json_output: bool = Field(True, alias="json", description="Return JSON response")


class ParseResponse(ApiResponseBase):
    parser: str = "rule"
    spec: dict[str, Any]
    summary: str


class ValidateRequest(BaseModel):
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


class ApiErrorResponse(ApiResponseBase):
    status: str = "error"
    error_code: str
    message: str
