"""OpenAPI contract tests for the local Agent API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_agent_api_openapi_includes_agent_endpoints():
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    for path in [
        "/api/health",
        "/api/version",
        "/api/adapters",
        "/api/schema",
        "/api/parse",
        "/api/validate",
        "/api/workflow-plan",
        "/api/adapter-preview",
        "/api/validation-evidence",
        "/api/readiness",
        "/api/materials",
        "/api/materials/{material_id}",
        "/api/materials/suggest",
        "/api/materials/diagnose",
        "/api/examples",
        "/api/examples/{example_id}",
        "/api/examples/{example_id}/agent-trace",
        "/api/design-requirements",
        "/api/design-requirements/{template_id}",
        "/api/design-requirements/match",
        "/api/application-domains",
        "/api/application-domains/{domain_id}",
        "/api/application-domains/match",
        "/api/application-domains/{domain_id}/cross-check",
        "/api/application-domain-cross-checks",
        "/api/application-domain-benchmarks",
        "/api/application-domain-benchmarks/{scenario_id}",
        "/api/application-domain-benchmarks/{scenario_id}/evaluate",
        "/api/application-domain-benchmark-results",
        "/api/optical-language/infer",
        "/api/optical-language/diagnose",
        "/api/optical-language/observables/diagnose",
        "/api/optical-language/adapter-mapping",
        "/api/agent-trace",
        "/api/agent-session",
        "/api/tool-capabilities",
        "/api/backend-capability-report",
        "/api/backend-evidence-summary",
        "/api/backend-validation-maturity",
        "/api/design-case-cross-checks",
        "/api/adapter-native-golden-coverage",
        "/api/optics/thin-film",
        "/api/optics/thin-film-spectrum",
        "/api/optics/quarter-wave-ar",
        "/api/optics/paraxial-lens",
        "/api/optics/paraxial-system",
        "/api/optics/two-lens-relay",
        "/api/optics/gaussian-beam",
        "/api/optics/gaussian-beam-series",
        "/api/optics/gaussian-beam-focus",
        "/api/optics/fiber-coupling",
        "/api/optics/polarization-jones",
        "/api/optics/waveguide-estimate",
        "/api/optics/waveguide-sweep",
        "/api/optics/waveguide-single-mode-range",
    ]:
        assert path in paths


def test_agent_api_openapi_uses_response_models_and_excludes_publish_or_run_api():
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi = response.json()
    paths = openapi["paths"]
    for path in [
        "/api/health",
        "/api/version",
        "/api/adapters",
        "/api/schema",
        "/api/parse",
        "/api/validate",
        "/api/workflow-plan",
        "/api/adapter-preview",
        "/api/validation-evidence",
        "/api/readiness",
        "/api/materials",
        "/api/materials/{material_id}",
        "/api/materials/suggest",
        "/api/materials/diagnose",
        "/api/examples",
        "/api/examples/{example_id}",
        "/api/examples/{example_id}/agent-trace",
        "/api/design-requirements",
        "/api/design-requirements/{template_id}",
        "/api/design-requirements/match",
        "/api/application-domains",
        "/api/application-domains/{domain_id}",
        "/api/application-domains/match",
        "/api/application-domains/{domain_id}/cross-check",
        "/api/application-domain-cross-checks",
        "/api/application-domain-benchmarks",
        "/api/application-domain-benchmarks/{scenario_id}",
        "/api/application-domain-benchmarks/{scenario_id}/evaluate",
        "/api/application-domain-benchmark-results",
        "/api/optical-language/infer",
        "/api/optical-language/diagnose",
        "/api/optical-language/observables/diagnose",
        "/api/optical-language/adapter-mapping",
        "/api/agent-trace",
        "/api/agent-session",
        "/api/tool-capabilities",
        "/api/backend-capability-report",
        "/api/backend-evidence-summary",
        "/api/backend-validation-maturity",
        "/api/design-case-cross-checks",
        "/api/adapter-native-golden-coverage",
        "/api/optics/thin-film",
        "/api/optics/thin-film-spectrum",
        "/api/optics/quarter-wave-ar",
        "/api/optics/paraxial-lens",
        "/api/optics/paraxial-system",
        "/api/optics/two-lens-relay",
        "/api/optics/gaussian-beam",
        "/api/optics/gaussian-beam-series",
        "/api/optics/gaussian-beam-focus",
        "/api/optics/fiber-coupling",
        "/api/optics/polarization-jones",
        "/api/optics/waveguide-estimate",
        "/api/optics/waveguide-sweep",
        "/api/optics/waveguide-single-mode-range",
    ]:
        operation = paths[path]["get"] if "get" in paths[path] else paths[path]["post"]
        schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
        assert "$ref" in schema or "allOf" in schema

    for path in [
        "/api/parse",
        "/api/validate",
        "/api/workflow-plan",
        "/api/adapter-preview",
        "/api/materials/suggest",
        "/api/materials/diagnose",
        "/api/design-requirements/match",
        "/api/application-domains/match",
        "/api/optical-language/infer",
        "/api/optical-language/diagnose",
        "/api/optical-language/observables/diagnose",
        "/api/optical-language/adapter-mapping",
        "/api/agent-trace",
        "/api/agent-session",
        "/api/optics/thin-film",
        "/api/optics/thin-film-spectrum",
        "/api/optics/quarter-wave-ar",
        "/api/optics/paraxial-lens",
        "/api/optics/paraxial-system",
        "/api/optics/two-lens-relay",
        "/api/optics/gaussian-beam",
        "/api/optics/gaussian-beam-series",
        "/api/optics/gaussian-beam-focus",
        "/api/optics/fiber-coupling",
        "/api/optics/polarization-jones",
        "/api/optics/waveguide-estimate",
        "/api/optics/waveguide-sweep",
        "/api/optics/waveguide-single-mode-range",
    ]:
        operation = paths[path]["post"]
        assert operation["requestBody"]["content"]["application/json"]["schema"]
        assert "400" in operation["responses"]
        error_schema = operation["responses"]["400"]["content"]["application/json"]["schema"]
        assert error_schema["$ref"].endswith("/ApiErrorResponse")

    schemas = openapi["components"]["schemas"]
    for schema_name in ("VersionResponse", "ReadinessResponse", "ApiErrorResponse"):
        assert "api_contract_version" in schemas[schema_name]["properties"]
    calculator_properties = schemas["OpticalCalculatorResponse"]["properties"]
    assert "quality" in calculator_properties
    assert "warnings" in calculator_properties

    forbidden_api_paths = {
        "/api/workflow-run",
        "/api/solver-run",
        "/api/tag",
        "/api/release",
        "/api/upload",
        "/api/publish",
        "/api/testpypi-upload",
        "/api/pypi-upload",
    }
    assert forbidden_api_paths.isdisjoint(paths)
