"""API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from optical_spec_agent import __version__
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_summary


router = APIRouter()


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
