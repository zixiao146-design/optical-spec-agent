"""Documentation tests for Local Agent API versioning."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_api_versioning_policy_documents_candidate_api_and_safety_bounds():
    text = (ROOT / "docs/api_versioning_policy.md").read_text(encoding="utf-8")
    assert 'api_contract_version`: "0.1"' in text
    assert 'package_version`: "0.9.0rc8"' in text
    assert "frontend-readiness / candidate API" in text
    assert "local MVP implemented under `frontend/`" in text
    assert "not yet a separately frozen v1.0 API contract" in text
    assert "scripts/smoke_frontend_mvp.sh" in text
    assert "not live validation" in text
    assert "Breaking API changes require updates to `docs/api_migration_notes.md`" in text
    assert "No external solver by default" in text
    assert "No external LLM by default" in text
    assert "No proprietary solver by default" in text
    assert "No production-grade validation claim" in text
    assert "No formal convergence proof claim" in text


def test_api_migration_notes_exist_and_record_no_breaking_migrations():
    text = (ROOT / "docs/api_migration_notes.md").read_text(encoding="utf-8")
    assert "Current `api_contract_version`: 0.1" in text
    assert "Current package version: 0.9.0rc8" in text
    assert "Local frontend MVP implementation exists under `frontend/`" in text
    assert "demo fixture mode is not live validation" in text
    assert "Breaking changes must be documented here" in text
    assert "no breaking API migrations recorded" in text
