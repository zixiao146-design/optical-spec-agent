"""Backend functionality status docs tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backend_functionality_status_records_reality_and_boundaries():
    path = ROOT / "docs" / "backend_functionality_status.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "Installed / Callable / Executed",
        "Material library",
        "Agent task session builder",
        "Tool-call ledger",
        "Thin-film preview calculator",
        "Thin-film spectrum / quarter-wave AR helper",
        "Case Integration",
        "Calculator responses now expose `quality`",
        "optical_calculator_reference_cases.md",
        "External solvers are not run by default",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
    ]:
        assert phrase in text
