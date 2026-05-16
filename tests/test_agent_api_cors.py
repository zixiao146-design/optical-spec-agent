from fastapi.testclient import TestClient

from optical_spec_agent.api.app import LOCAL_FRONTEND_ORIGINS, app


def test_local_frontend_cors_origin_is_allowed():
    client = TestClient(app)
    response = client.options(
        "/api/health",
        headers={
            "Origin": LOCAL_FRONTEND_ORIGINS[0],
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == LOCAL_FRONTEND_ORIGINS[0]
