"""v1.0 public contract non-goal checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_contract_non_goals_keep_validation_and_backend_scope_conservative():
    path = ROOT / "docs" / "v1_0_contract_non_goals.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Production-grade physical validation is not claimed" in text
    assert "Formal convergence proof is not claimed" in text
    assert "External solvers are not default dependencies" in text
    assert "External LLM is not default dependency" in text
    assert "Proprietary solvers are not default targets" in text
    assert "Generated adapter internals are not frozen" in text
    assert "Workflow internals are not frozen" in text
    assert "Elmer Level 3 is deferred" in text
    assert "PyPI publication is not yet approved" in text
    assert "`v1.0.0` final release is not yet approved" in text
    assert "The approved freeze does not convert these non-goals into supported claims" in text
