"""Application-domain API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_application_domain_api_endpoints_are_safe():
    client = TestClient(app)
    listing = client.get("/api/application-domains")
    assert listing.status_code == 200
    body = listing.json()
    assert body["domain_count"] == 10
    assert body["external_solver_executed"] is False

    detail = client.get("/api/application-domains/nanoparticle_plasmonics")
    assert detail.status_code == 200
    assert detail.json()["domain"]["domain_id"] == "nanoparticle_plasmonics"

    match = client.post(
        "/api/application-domains/match",
        json={"goal": "Design a local thin-film coating preview.", "language": "en"},
    )
    assert match.status_code == 200
    assert match.json()["matched_domains"] == ["thin_film_coating"]
    assert match.json()["no_external_llm_used"] is True

    cross_check = client.get("/api/application-domains/thin_film_coating/cross-check")
    assert cross_check.status_code == 200
    assert cross_check.json()["cross_checks"][0]["status"] == "pass"

    all_checks = client.get("/api/application-domain-cross-checks")
    assert all_checks.status_code == 200
    assert all_checks.json()["summary"]["total"] == 10
    assert all_checks.json()["summary"]["fail"] == 0
    assert all_checks.json()["external_solver_executed"] is False

