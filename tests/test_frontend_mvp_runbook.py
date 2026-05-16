from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "frontend_mvp_runbook.md"


def test_frontend_mvp_runbook_documents_local_start_and_safety():
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "python -m uvicorn optical_spec_agent.api.app:app" in text
    assert "npm run dev" in text
    assert "npm run build" in text
    assert "./scripts/smoke_frontend_mvp.sh" in text
    assert "VITE_API_BASE_URL" in text
    assert "Demo fixture mode" in text
    assert "not live validation" in text
    assert "No solver execution" in text
    assert "No external LLM" in text
    assert "No upload controls" in text
    assert "No release controls" in text
    assert "production-grade" in text
    assert "formal convergence proof" in text
