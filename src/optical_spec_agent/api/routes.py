"""API routes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from optical_spec_agent import __version__
from optical_spec_agent.adapters.registry import (
    AdapterRegistryError,
    dispatch_adapter,
    get_adapter,
    list_adapters,
)
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_summary
from optical_spec_agent.validators.spec_validator import SpecValidator


router = APIRouter()

REPO_ROOT = Path(__file__).resolve().parents[3]
CURRENT_PUBLIC_PRERELEASE = "v0.9.0rc6"
MAIN_DEVELOPMENT_VERSION = __version__

SAFETY_FLAGS: dict[str, bool] = {
    "external_solver_executed": False,
    "external_llm_required": False,
    "proprietary_solver_required": False,
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
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


class AgentParseRequest(BaseModel):
    text: str = Field(..., description="Natural language optical task description")
    task_id: str = Field("", description="Optional task ID")
    parser: str = Field("heuristic", description="Local parser mode: heuristic or rule")
    json_output: bool = Field(True, alias="json", description="Return JSON response")


class AgentSpecRequest(BaseModel):
    spec: dict[str, Any] | None = Field(None, description="Inline OpticalSpec JSON")
    path: str | None = Field(None, description="Local repo-relative JSON spec path")


class AgentWorkflowPlanRequest(AgentSpecRequest):
    text: str | None = Field(None, description="Natural language workflow request")
    parser: str = Field("heuristic", description="Local parser mode: heuristic or rule")
    tool: str = Field("auto", description="Adapter tool hint")


class AgentAdapterPreviewRequest(AgentSpecRequest):
    tool: str = Field("auto", description="Adapter tool hint")


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


@router.get("/api/health")
def agent_health():
    """Local-first API health endpoint for future Agent Studio clients."""
    return {
        "status": "ok",
        "service": "optical-spec-agent",
        **SAFETY_FLAGS,
    }


@router.get("/api/version")
def agent_version():
    return {
        "status": "ok",
        "package_version": __version__,
        "current_public_prerelease": CURRENT_PUBLIC_PRERELEASE,
        "main_development_version": MAIN_DEVELOPMENT_VERSION,
        "pypi_published": False,
        "testpypi_verified": True,
        "testpypi_verified_version": "0.9.0rc6.dev0",
        **SAFETY_FLAGS,
    }


@router.get("/api/adapters")
def agent_adapters():
    adapters: list[dict[str, Any]] = []
    for metadata in list_adapters():
        maturity = ADAPTER_MATURITY.get(metadata.tool_name, {})
        adapters.append(
            {
                "tool_name": metadata.tool_name,
                "display_name": metadata.display_name,
                "solver_family": metadata.solver_family,
                "current_status": metadata.current_status,
                "maturity_level": maturity.get("maturity_level", "unclassified"),
                "evidence": maturity.get("evidence"),
                "external_solver_required_by_default": False,
                "production_grade_validation_claimed": False,
                "formal_convergence_proof_claimed": False,
                "limitations": metadata.limitations,
            }
        )
    return {"status": "ok", "adapters": adapters, **SAFETY_FLAGS}


@router.get("/api/schema")
def agent_schema():
    return {
        "status": "ok",
        "schema_name": "OpticalSpec",
        "schema": OpticalSpec.export_json_schema_dict(),
        **SAFETY_FLAGS,
    }


@router.post("/api/parse")
def agent_parse(req: AgentParseRequest):
    parser = _local_parser(req.parser)
    try:
        svc = SpecService(parser=parser)
        spec = svc.process(req.text, task_id=req.task_id)
    except Exception as exc:  # noqa: BLE001 - API returns structured diagnostics.
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "status": "ok",
        "parser": parser,
        "spec": spec.to_flat_dict(),
        "summary": spec_to_summary(spec),
        "diagnostics": {
            "missing_fields": spec.missing_fields,
            "warnings": spec.validation_status.warnings,
            "errors": spec.validation_status.errors,
            "assumptions": spec.assumption_log,
        },
        "recommended_next_actions": [
            "Review inferred fields before generation.",
            "Use /api/validate before adapter preview.",
        ],
        **SAFETY_FLAGS,
    }


@router.post("/api/validate")
def agent_validate(req: AgentSpecRequest):
    spec = _load_spec(req.spec, req.path)
    validated = SpecValidator().validate(spec)
    return {
        "status": "ok" if validated.validation_status.is_executable else "needs_review",
        "valid": validated.validation_status.is_executable,
        "diagnostics": {
            "errors": validated.validation_status.errors,
            "warnings": validated.validation_status.warnings,
            "missing_fields": validated.missing_fields,
        },
        **SAFETY_FLAGS,
    }


@router.post("/api/workflow-plan")
def agent_workflow_plan(req: AgentWorkflowPlanRequest):
    from optical_spec_agent.workflows import plan_workflow

    parser = _local_parser(req.parser)
    input_text = req.text
    if input_text is None and req.path:
        input_text = _load_workflow_input_text(req.path)
    if input_text is None:
        spec = _load_spec(req.spec, req.path)
        input_text = _workflow_text_from_spec(spec)

    plan = plan_workflow(input_text, parser=parser, llm_provider="mock", tool=req.tool)
    payload = plan.model_dump(mode="json")
    return {
        "status": "ok",
        "workflow_plan": payload,
        "public_top_level_keys": sorted(payload),
        "recommended_next_actions": [
            "Review workflow_plan.risk_flags before running any optional execution.",
            "Use /api/adapter-preview for local artifact preview.",
        ],
        **SAFETY_FLAGS,
    }


@router.post("/api/adapter-preview")
def agent_adapter_preview(req: AgentAdapterPreviewRequest):
    spec = _load_spec(req.spec, req.path)
    try:
        adapter = dispatch_adapter(spec, preferred_tool=req.tool)
        metadata = adapter.metadata()
        result = adapter.generate(spec)
    except AdapterRegistryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001 - preview should return clean API errors.
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    status = "ok" if not result.errors else "needs_review"
    return {
        "status": status,
        "tool": result.tool,
        "display_name": metadata.display_name,
        "output_language": result.language,
        "output_extension": metadata.output_extension,
        "preview_content": result.content,
        "artifact_summary": {
            "content_length": len(result.content),
            "generated_files": result.generated_files,
            "missing_required": result.missing_required,
            "defaults_applied": result.defaults_applied,
        },
        "diagnostics": {
            "warnings": result.warnings,
            "errors": result.errors,
            "limitations": result.limitations,
        },
        **SAFETY_FLAGS,
    }


@router.get("/api/validation-evidence")
def agent_validation_evidence():
    evidence = []
    for tool in ("gmsh", "meep", "mpb", "optiland", "elmer"):
        adapter = get_adapter(tool)
        metadata = adapter.metadata()
        maturity = ADAPTER_MATURITY[tool]
        evidence.append(
            {
                "tool_name": tool,
                "display_name": metadata.display_name,
                "maturity_level": maturity["maturity_level"],
                "evidence": maturity.get("evidence"),
                "status_note": maturity.get("status_note", "Optional manual validation evidence recorded."),
                "production_grade_validation_claimed": False,
                "formal_convergence_proof_claimed": False,
            }
        )
    return {"status": "ok", "validation_evidence": evidence, **SAFETY_FLAGS}


@router.get("/api/readiness")
def agent_readiness():
    adapter_maturity = {
        tool: data["maturity_level"] for tool, data in ADAPTER_MATURITY.items()
    }
    return {
        "status": "ok",
        "current_public_prerelease": CURRENT_PUBLIC_PRERELEASE,
        "main_development_version": MAIN_DEVELOPMENT_VERSION,
        "testpypi": {
            "uploaded_and_verified": True,
            "verified_version": "0.9.0rc6.dev0",
            "upload_for_current_dev_version": "not performed",
        },
        "pypi": {
            "published": False,
            "publication_approval": "not granted",
        },
        "public_contract_freeze": {
            "status": "approved",
            "date": "2026-05-16",
        },
        "adapter_maturity": adapter_maturity,
        "recommended_next_actions": [
            "Continue API readiness engineering.",
            "Decide PyPI publication later with explicit maintainer approval.",
            "Prepare v1.0.0 release draft only after explicit approval.",
        ],
        **SAFETY_FLAGS,
    }


def _local_parser(parser: str) -> str:
    normalized = (parser or "heuristic").strip().lower()
    if normalized in {"heuristic", "local"}:
        return "rule"
    if normalized == "rule":
        return normalized
    raise HTTPException(
        status_code=400,
        detail="The local Agent API only allows heuristic/rule parsing by default.",
    )


def _load_spec(spec_payload: dict[str, Any] | None, path: str | None) -> OpticalSpec:
    if spec_payload is None and path is None:
        raise HTTPException(status_code=400, detail="Provide spec or local path.")
    data = spec_payload if spec_payload is not None else _load_json_file(path or "")
    if isinstance(data, dict) and "spec" in data and isinstance(data["spec"], dict):
        data = data["spec"]
    try:
        return OpticalSpec.model_validate(data)
    except Exception as exc:  # noqa: BLE001 - surface validation details as API diagnostics.
        raise HTTPException(status_code=400, detail=f"Invalid OpticalSpec: {exc}") from exc


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
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {path}") from exc


def _resolve_local_path(path: str) -> Path:
    if "://" in path:
        raise HTTPException(status_code=400, detail="Network paths are not supported.")
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Path must stay inside the repository.") from exc
    if not resolved.exists():
        raise HTTPException(status_code=404, detail=f"Local path not found: {path}")
    return resolved


def _workflow_text_from_spec(spec: OpticalSpec) -> str:
    for field in (spec.task.research_goal, spec.task.task_name):
        value = getattr(field, "value", None)
        if isinstance(value, str) and value.strip():
            return value
    return "Create a local optical workflow preview from the provided OpticalSpec."
