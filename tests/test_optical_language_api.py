from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


client = TestClient(app)


def test_optical_language_infer_endpoint_returns_source_monitor_models():
    response = client.post(
        "/api/optical-language/infer",
        json={
            "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
            "template_id": "nanoparticle_plasmonics",
            "language": "zh-CN",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["source_model"]["source_type"] == "plane_wave"
    assert body["monitor_model"]["monitor_type"] == "scattering_spectrum"
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False


def test_optical_language_diagnose_endpoint_returns_stable_safety_shape():
    response = client.post(
        "/api/optical-language/diagnose",
        json={
            "goal": "Design an anti-reflection coating for glass at 550 nm.",
            "template_id": "thin_film_ar_coating",
            "language": "en",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["matched_template_id"] == "thin_film_ar_coating"
    assert body["safe_to_preview"] is True
    assert body["safe_to_run_solver"] is False
    assert body["external_solver_executed"] is False
    assert body["production_grade_validation_claimed"] is False


def test_optical_language_infer_empty_goal_returns_stable_error():
    response = client.post("/api/optical-language/infer", json={"goal": "   "})

    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"
    assert body["error_code"] == "invalid_workflow_request"
    assert body["external_solver_executed"] is False
