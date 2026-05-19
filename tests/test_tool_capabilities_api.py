"""Tool capability API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_tool_capabilities_reports_internal_external_and_release_sections():
    client = TestClient(app)
    response = client.get("/api/tool-capabilities")
    assert response.status_code == 200
    payload = response.json()
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False

    internal = {item["tool_name"]: item for item in payload["internal_tools"]}
    assert internal["material_catalog"]["available"] is True
    assert internal["material_suitability_diagnostics"]["available"] is True
    assert internal["example_registry"]["available"] is True
    assert internal["ambiguous_requirement_matching"]["available"] is True
    assert internal["application_domain_registry"]["available"] is True
    assert internal["material_template_cross_checks"]["available"] is True
    assert internal["agent_trace_builder"]["available"] is True
    assert internal["workflow_planner"]["available"] is True
    assert internal["adapter_preview_generator"]["available"] is True
    assert internal["adapter_native_golden_coverage"]["available"] is True
    assert internal["optical_calculators"]["available"] is True

    external = {item["tool_name"]: item for item in payload["external_solvers"]}
    for tool in ["meep", "gmsh", "mpb", "ElmerSolver", "optiland"]:
        assert tool in external
        assert external[tool]["default_allowed"] is False
        assert "not_executed" in external[tool]["status"]

    publication = {item["tool_name"]: item for item in payload["publication_release_controls"]}
    assert publication["testpypi_upload"]["status"] == "disabled_not_exposed"
    assert publication["pypi_publish"]["status"] == "disabled_not_exposed"
    assert publication["tag_or_release_create"]["status"] == "disabled_not_exposed"
