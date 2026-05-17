from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_agent_trace_api_returns_all_roles_and_final_recommendation():
    client = TestClient(app)
    response = client.post(
        "/api/agent-trace",
        json={"example_id": "nanoparticle_plasmonics", "text": "nanoparticle plasmonics"},
    )
    assert response.status_code == 200
    payload = response.json()
    names = {agent["agent_name"] for agent in payload["agents"]}
    assert {
        "SpecAgent",
        "MaterialAgent",
        "GeometryAgent",
        "AdapterAgent",
        "WorkflowAgent",
        "EvidenceAgent",
        "SafetyAgent",
        "RecommendationAgent",
    }.issubset(names)
    assert payload["final_recommendation"]
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False
