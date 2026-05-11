"""API tests for workflow endpoints."""

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


client = TestClient(app)


def test_workflow_plan_endpoint():
    response = client.post(
        "/workflow/plan",
        json={"text": "用 MPB 计算二维光子晶体 band diagram。", "parser": "hybrid", "tool": "mpb"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["selected_tool"] == "mpb"


def test_workflow_run_endpoint_defaults_no_execution(tmp_path):
    response = client.post(
        "/workflow/run",
        json={
            "text": "用 MPB 计算二维光子晶体 band diagram。",
            "parser": "hybrid",
            "llm_provider": "mock",
            "tool": "mpb",
            "output_dir": str(tmp_path),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["selected_tool"] == "mpb"
    assert data["status"] in {"success", "warning"}


def test_workflow_report_endpoint(tmp_path):
    run_response = client.post(
        "/workflow/run",
        json={
            "text": "用 MPB 计算二维光子晶体 band diagram。",
            "parser": "hybrid",
            "llm_provider": "mock",
            "tool": "mpb",
            "output_dir": str(tmp_path),
        },
    )
    workflow = run_response.json()
    response = client.post(
        "/workflow/report",
        json={"workflow_run": workflow, "format": "markdown"},
    )
    assert response.status_code == 200
    assert "Workflow Report" in response.json()["content"]


def test_workflow_run_unsupported_provider_records_error(tmp_path):
    response = client.post(
        "/workflow/run",
        json={
            "text": "用 MPB 计算 band diagram。",
            "parser": "hybrid",
            "llm_provider": "unsupported",
            "tool": "mpb",
            "output_dir": str(tmp_path),
            "strict": True,
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "error"
