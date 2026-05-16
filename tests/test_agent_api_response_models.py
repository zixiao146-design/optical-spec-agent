"""Local Agent API response model checks."""

from __future__ import annotations

from optical_spec_agent.api.models import (
    AdapterSummary,
    ApiErrorResponse,
    HealthResponse,
    VersionResponse,
)
from optical_spec_agent.adapters.registry import list_adapters


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
        package_version="0.9.0rc7.dev0",
        current_public_prerelease="v0.9.0rc6",
        main_development_version="0.9.0rc7.dev0",
    )
    _assert_safety_defaults(response)
    assert response.package_version == "0.9.0rc7.dev0"
    assert response.current_public_prerelease == "v0.9.0rc6"
    assert response.main_development_version == "0.9.0rc7.dev0"
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
    assert response.status == "error"
    assert response.error_code == "invalid_spec"
    assert response.message == "Invalid spec"
    assert response.diagnostics.errors == []
