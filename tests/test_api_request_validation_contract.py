"""Documentation tests for Local Agent API request validation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_api_request_validation_contract_documents_stable_errors():
    text = (ROOT / "docs/api_request_validation_contract.md").read_text(encoding="utf-8")
    assert "Unknown request fields should be rejected" in text
    assert "Invalid adapter/tool names should produce `unsupported_adapter`" in text
    assert "Invalid spec payloads should produce `invalid_spec`" in text
    assert "Invalid workflow requests should produce `invalid_workflow_request`" in text
    assert "Solver execution requests are not enabled by default" in text
    assert '`api_contract_version: "0.1"`' in text
    assert "`external_solver_executed: false`" in text
    assert "`external_llm_required: false`" in text
    assert "`production_grade_validation_claimed: false`" in text
    assert "`formal_convergence_proof_claimed: false`" in text
