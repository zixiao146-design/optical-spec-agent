"""Local Agent API response model checks."""

from __future__ import annotations

from optical_spec_agent.api.models import (
    API_CONTRACT_VERSION,
    AdapterSummary,
    ApiErrorResponse,
    AgentSessionRequest,
    AgentTaskSessionResponse,
    HealthResponse,
    OpticalCalculatorResponse,
    ParseRequest,
    ReadinessResponse,
    ToolCapabilitiesResponse,
    ToolCapabilityItem,
    ValidateRequest,
    VersionResponse,
    WorkflowPlanRequest,
)
from optical_spec_agent.adapters.registry import list_adapters
from pydantic import ValidationError


def _assert_safety_defaults(model) -> None:
    assert model.external_solver_executed is False
    assert model.external_llm_required is False
    assert model.proprietary_solver_required is False
    assert model.production_grade_validation_claimed is False
    assert model.formal_convergence_proof_claimed is False


def test_health_response_defaults_safety_flags_false():
    response = HealthResponse()
    _assert_safety_defaults(response)
    assert response.status == "ok"
    assert response.service == "optical-spec-agent"


def test_version_response_tracks_current_versions():
    response = VersionResponse(
        package_version="0.9.0rc8",
        current_public_prerelease="v0.9.0rc7",
        main_development_version="0.9.0rc8",
    )
    _assert_safety_defaults(response)
    assert API_CONTRACT_VERSION == "0.1"
    assert response.api_contract_version == "0.1"
    assert response.package_version == "0.9.0rc8"
    assert response.current_public_prerelease == "v0.9.0rc7"
    assert response.main_development_version == "0.9.0rc8"
    assert response.testpypi_verified is True
    assert response.pypi_published is False


def test_adapter_summary_can_represent_all_known_adapters_without_claim_expansion():
    for metadata in list_adapters():
        summary = AdapterSummary(
            tool_name=metadata.tool_name,
            display_name=metadata.display_name,
            solver_family=metadata.solver_family,
            current_status=metadata.current_status,
            maturity_level="Level 3" if metadata.tool_name != "elmer" else "Level 2 + Level-3-ready",
            limitations=metadata.limitations,
        )
        assert summary.tool_name in {"meep", "mpb", "gmsh", "elmer", "optiland"}
        assert summary.external_solver_required_by_default is False
        assert summary.production_grade_validation_claimed is False
        assert summary.formal_convergence_proof_claimed is False


def test_error_response_preserves_safety_boundaries():
    response = ApiErrorResponse(error_code="invalid_spec", message="Invalid spec")
    _assert_safety_defaults(response)
    assert response.api_contract_version == "0.1"
    assert response.status == "error"
    assert response.error_code == "invalid_spec"
    assert response.message == "Invalid spec"
    assert response.diagnostics.errors == []


def test_readiness_response_includes_api_contract_version():
    response = ReadinessResponse(
        current_public_prerelease="v0.9.0rc7",
        main_development_version="0.9.0rc8",
        testpypi={"uploaded_and_verified": True},
        pypi={"published": False},
        public_contract_freeze={"status": "approved"},
        adapter_maturity={"elmer": "Level 2 + Level-3-ready"},
    )
    _assert_safety_defaults(response)
    assert response.api_contract_version == "0.1"
    assert response.v1_0_0_released is False


def test_agent_api_request_models_reject_unknown_fields():
    for model, payload in [
        (ParseRequest, {"text": "Use Meep.", "unexpected": True}),
        (ValidateRequest, {"path": "examples/specs/minimal_nanoparticle.json", "unexpected": True}),
        (WorkflowPlanRequest, {"text": "Use MPB.", "unexpected": True}),
        (AgentSessionRequest, {"goal": "Plan a preview.", "unexpected": True}),
    ]:
        try:
            model.model_validate(payload)
        except ValidationError as exc:
            assert "extra_forbidden" in str(exc)
        else:  # pragma: no cover - explicit failure path
            raise AssertionError(f"{model.__name__} accepted an unknown field")


def test_agent_task_session_response_preserves_safety_defaults():
    response = AgentTaskSessionResponse(
        session_id="session-test",
        user_goal="Plan a local preview.",
        optical_intent_summary="general optical design preview",
        design_case_summary="generic preview",
        agent_trace={
            "trace_id": "trace-test",
            "final_recommendation": "Review the local preview.",
        },
        final_recommendation="Review the local preview.",
    )
    _assert_safety_defaults(response)
    assert response.api_contract_version == "0.1"
    assert response.plan_steps == []
    assert response.artifacts == []
    assert response.permission_gates == []
    assert response.tool_call_ledger == []


def test_tool_capabilities_and_calculator_response_models_keep_safety_defaults():
    capabilities = ToolCapabilitiesResponse(
        internal_tools=[
            ToolCapabilityItem(
                tool_name="material_catalog",
                tool_kind="internal_python",
                available=True,
                default_allowed=True,
                status="available",
                detection_method="import",
            )
        ]
    )
    _assert_safety_defaults(capabilities)
    assert capabilities.internal_tools[0].tool_name == "material_catalog"

    calculator = OpticalCalculatorResponse(
        result={"reflectance": 0.1},
        assumptions=["preview"],
        limitations=["not production-grade"],
    )
    _assert_safety_defaults(calculator)
    assert calculator.result["reflectance"] == 0.1
