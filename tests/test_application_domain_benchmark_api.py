"""Application-domain benchmark API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_application_domain_benchmark_api_endpoints_are_safe():
    client = TestClient(app)
    listing = client.get("/api/application-domain-benchmarks")
    assert listing.status_code == 200
    listing_body = listing.json()
    assert listing_body["scenario_count"] >= 19
    assert listing_body["external_solver_executed"] is False

    detail = client.get("/api/application-domain-benchmarks/nanoparticle_plasmonics_positive")
    assert detail.status_code == 200
    assert detail.json()["scenario"]["scenario_id"] == "nanoparticle_plasmonics_positive"
    assert detail.json()["external_solver_executed"] is False

    eval_positive = client.post(
        "/api/application-domain-benchmarks/nanoparticle_plasmonics_positive/evaluate"
    )
    assert eval_positive.status_code == 200
    assert eval_positive.json()["status"] == "pass"
    assert eval_positive.json()["external_solver_executed"] is False

    eval_ambiguous = client.post(
        "/api/application-domain-benchmarks/waveguide_or_coating_ambiguous/evaluate"
    )
    assert eval_ambiguous.status_code == 200
    assert eval_ambiguous.json()["actual_questions"]

    results = client.get("/api/application-domain-benchmark-results")
    assert results.status_code == 200
    body = results.json()
    assert body["status"] == "ok"
    assert body["summary"]["fail"] == 0
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    assert body["production_grade_validation_claimed"] is False
