from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "frontend" / "src" / "api" / "client.ts"


def test_frontend_api_client_is_local_api_only():
    text = CLIENT.read_text(encoding="utf-8")
    assert '"/api/health"' in text
    assert '"/api/version"' in text
    assert '"/api/adapters"' in text
    assert '"/api/schema"' in text
    assert '"/api/parse"' in text
    assert '"/api/validate"' in text
    assert '"/api/workflow-plan"' in text
    assert '"/api/adapter-preview"' in text
    assert '"/api/validation-evidence"' in text
    assert '"/api/readiness"' in text
    assert '"/api/materials"' in text
    assert '"/api/materials/suggest"' in text
    assert '"/api/agent-trace"' in text
    assert '"/api/examples"' in text
    assert "/agent-trace" in text
    assert "http://127.0.0.1:8000" in text
    assert "path.startsWith(\"/api/\")" in text


def test_frontend_api_client_has_no_external_operation_endpoints():
    text = CLIENT.read_text(encoding="utf-8").lower()
    forbidden = [
        "test.pypi.org",
        "pypi.org",
        "api.github.com",
        "gh release",
        "twine",
        "/upload",
        "/publish",
        "/release",
        "/tag",
        "/solver-run",
    ]
    for phrase in forbidden:
        assert phrase not in text
