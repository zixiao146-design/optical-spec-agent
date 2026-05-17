"""Agent Studio frontend roadmap documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_studio_frontend_roadmap_exists_and_is_future_work():
    path = ROOT / "docs" / "agent_studio_frontend_roadmap.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Not part of v1.0.0 release criteria" in text
    assert "Should follow API readiness" in text
    assert "API response models exist" in text
    assert "examples/api/" in text
    assert "docs/frontend_mvp_product_spec.md" in text
    assert "docs/frontend_information_architecture.md" in text
    assert "docs/frontend_api_mapping.md" in text
    assert "docs/frontend_mvp_acceptance_criteria.md" in text
    assert "docs/frontend_safety_policy.md" in text
    assert "docs/frontend_mvp_implementation_plan.md" in text
    assert "Frontend MVP implementation exists under `frontend/`" in text
    assert "docs/frontend_mvp_runbook.md" in text
    assert "docs/frontend_mvp_qa_checklist.md" in text
    assert "scripts/smoke_frontend_mvp.sh" in text
    assert "docs/agent_studio_demo_feedback.md" in text
    assert "docs/frontend_hardening_backlog.md" in text
    assert "Loading, empty, error, API disconnected, and demo fixture states" in text
    assert "React + Vite + TypeScript MVP scaffold exists" in text
    assert "Spec input" in text
    assert "Adapter matrix" in text
    assert "Workflow plan" in text
    assert "Artifact preview" in text
    assert "Validation evidence view" in text
    assert "Dashboard/readiness and system status views" in text
    assert "No default solver execution" in text
    assert "No cloud requirement" in text
    assert "No formal convergence proof claim" in text
