"""Application-domain example fixture tests."""

from __future__ import annotations

from pathlib import Path

from optical_spec_agent.examples.application_domains import list_application_domains


ROOT = Path(__file__).resolve().parents[1]


def test_application_domain_examples_exist_and_state_safety_boundaries():
    base = ROOT / "examples" / "application_domains"
    for domain in list_application_domains():
        folder = base / domain.domain_id
        assert (folder / "domain.json").exists()
        assert (folder / "goal_en.txt").exists()
        assert (folder / "goal_zh.txt").exists()
        assert (folder / "expected_cross_check.json").exists()
        readme = (folder / "README.md").read_text(encoding="utf-8")
        assert "no solver execution" in readme
        assert "calls no external LLM" in readme
        assert "claims no production-grade physical validation" in readme

