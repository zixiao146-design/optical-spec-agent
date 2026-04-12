"""API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json, spec_to_summary


router = APIRouter()


# ---- Request / Response schemas ----

class ParseRequest(BaseModel):
    text: str = Field(..., description="Natural language optical task description")
    task_id: str = Field("", description="Optional task ID (auto-generated if empty)")


class ParseResponse(BaseModel):
    spec_json: dict[str, Any]
    summary: str
    confirmed_fields: dict[str, Any]
    inferred_fields: dict[str, Any]
    missing_fields: list[str]
    assumption_log: list[str]
    validation_status: dict[str, Any]


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
    return {"status": "ok", "version": "0.2.0"}


@router.post("/parse", response_model=ParseResponse)
def parse(req: ParseRequest):
    svc = SpecService()
    spec = svc.process(req.text, task_id=req.task_id)
    return ParseResponse(
        spec_json=spec.to_flat_dict(),
        summary=spec_to_summary(spec),
        confirmed_fields=spec.confirmed_fields,
        inferred_fields=spec.inferred_fields,
        missing_fields=spec.missing_fields,
        assumption_log=spec.assumption_log,
        validation_status=spec.validation_status.model_dump(),
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
