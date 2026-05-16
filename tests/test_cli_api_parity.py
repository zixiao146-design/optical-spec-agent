"""CLI/API parity documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cli_api_parity_doc_maps_major_cli_surface_to_api():
    path = ROOT / "docs" / "cli_api_parity.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "optical-spec --help",
        "GET /api/health",
        "GET /api/version",
        "adapter-list --json",
        "GET /api/adapters",
        "GET /api/schema",
        "POST /api/parse",
        "POST /api/validate",
        "POST /api/workflow-plan",
        "POST /api/adapter-preview",
        "External solvers are not run by default",
        "External LLM access is not required by default",
        "Proprietary solvers are not required by default",
        "Production-grade physical validation is not claimed",
        "Formal convergence proof is not claimed",
        "implemented local MVP lives under `frontend/`",
        "frontend MVP uses this API as its backend surface",
        "does not shell out",
        "without uploading, publishing",
        "creating tags, or creating releases",
        "docs/frontend_mvp_runbook.md",
        "src/optical_spec_agent/api/models.py",
        "examples/api/",
        "api_contract_version",
        "frontend-readiness / candidate API",
        "docs/api_versioning_policy.md",
        "docs/api_request_validation_contract.md",
        "docs/api_migration_notes.md",
        "docs/api_local_launch_guide.md",
        "docs/frontend_handoff_spec.md",
        "docs/api_curl_examples.md",
        "scripts/smoke_agent_api.sh",
        "scripts/check_api_fixtures.py",
    ]
    for phrase in required:
        assert phrase in text
