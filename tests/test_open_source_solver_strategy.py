"""Open-source-solver-first strategy documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_strategy_and_proprietary_policy_docs_exist():
    assert (ROOT / "docs" / "open_source_solver_strategy.md").exists()
    assert (ROOT / "docs" / "proprietary_solver_policy.md").exists()


def test_readmes_state_open_source_solver_first_positioning():
    readme = _read("README.md").lower()
    readme_zh = _read("README.zh-CN.md")
    assert "open-source-solver-first" in readme
    assert "开源仿真工具链优先" in readme_zh


def test_strategy_doc_sets_default_dependency_boundary():
    text = _read("docs/open_source_solver_strategy.md")
    assert "optical-spec-agent is open-source-solver-first" in text
    assert "Proprietary commercial tools are not default dependencies" in text
    assert "no proprietary license required" in text
    assert "no external solver execution by default" in text
    assert "no external LLM required by default" in text


def test_proprietary_policy_names_tools_and_default_boundaries():
    text = _read("docs/proprietary_solver_policy.md")
    for name in ["Zemax", "Lumerical", "COMSOL", "proprietary Ansys optics tools"]:
        assert name in text
    assert "Proprietary tools are not required for default tests" in text
    assert "Proprietary tools are not required for `scripts/smoke_release.sh`" in text
    assert "Proprietary tools are not required for GitHub prerelease validation" in text
    assert "export-only" in text


def test_external_solver_policy_keeps_solver_execution_non_default():
    text = _read("docs/external_solver_policy.md")
    assert "External solvers are not run by default" in text
    assert "open-source-solver-first" in text
    assert "No proprietary license is required" in text
    assert "Closed-source" in text
    assert "commercial solver validation must be explicit, manual, non-default" in text
