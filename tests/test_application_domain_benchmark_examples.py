"""Application-domain benchmark example fixture tests."""

from __future__ import annotations

from pathlib import Path

from optical_spec_agent.examples.domain_benchmarks import list_domain_scenarios


ROOT = Path(__file__).resolve().parents[1]


def test_application_domain_benchmark_examples_exist_and_state_safety_boundaries():
    base = ROOT / "examples" / "application_domain_benchmarks"
    for scenario in list_domain_scenarios():
        folder = base / scenario.scenario_id
        assert (folder / "scenario.json").exists()
        assert (folder / "goal_en.txt").exists()
        assert (folder / "goal_zh.txt").exists()
        assert (folder / "expected_result.json").exists()
        readme = (folder / "README.md").read_text(encoding="utf-8")
        assert "no solver execution" in readme
        assert "calls no external LLM" in readme
        assert "preview/design-assist" in readme
        assert "claims no production-grade physical validation" in readme
        assert "formal convergence proof" in readme
