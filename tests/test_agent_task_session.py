"""Agent Task Session builder tests."""

from __future__ import annotations

import pytest

from optical_spec_agent.agents.task_session import build_agent_task_session
from optical_spec_agent.examples.registry import ExampleRegistryError


def test_agent_task_session_builds_local_optical_design_session():
    session = build_agent_task_session(
        "Create a local preview workflow for silver nanoparticle scattering on a thin film.",
        example_id="nanoparticle_plasmonics",
    )

    assert session.user_goal
    assert session.requirement_template_id == "nanoparticle_plasmonics"
    assert "nanoparticle" in session.optical_intent_summary
    assert session.optical_language_summary["physical_system"] == "nanoparticle_on_film"
    assert session.selected_example_id == "nanoparticle_plasmonics"
    assert session.missing_required_inputs
    assert session.default_assumptions_applied
    assert session.plan_steps
    assert session.artifacts
    assert session.permission_gates
    assert session.tool_call_ledger
    assert session.agent_trace.agents
    assert session.final_recommendation
    assert session.recommended_next_actions
    assert session.external_solver_executed is False
    assert session.external_llm_required is False
    assert session.proprietary_solver_required is False
    assert session.production_grade_validation_claimed is False
    assert session.formal_convergence_proof_claimed is False
    assert any(entry.tool_name == "material_catalog.suggest" for entry in session.tool_call_ledger)
    assert any(entry.tool_name == "requirements.match_template" for entry in session.tool_call_ledger)
    assert any(entry.tool_name == "agent_trace.build" for entry in session.tool_call_ledger)


def test_agent_task_session_blocks_external_and_release_actions():
    session = build_agent_task_session("Plan a local waveguide mode preview.")
    gates = {gate.gate_id: gate for gate in session.permission_gates}

    for allowed in [
        "parse_local_spec",
        "read_local_material_catalog",
        "generate_workflow_plan",
        "generate_adapter_preview",
    ]:
        assert gates[allowed].status == "allowed"
        assert gates[allowed].default_allowed is True

    for blocked in [
        "run_external_solver",
        "call_external_llm",
        "upload_testpypi",
        "publish_pypi",
        "create_git_tag",
        "create_github_release",
    ]:
        assert gates[blocked].status in {"blocked", "requires_explicit_approval"}
        assert gates[blocked].default_allowed is False

    ledger = {entry.tool_name: entry for entry in session.tool_call_ledger}
    assert ledger["external_solver.meep"].executed is False
    assert ledger["external_llm"].executed is False
    assert ledger["testpypi_upload"].executed is False
    assert ledger["git_tag_create"].executed is False


def test_agent_task_session_unknown_explicit_example_is_error():
    with pytest.raises(ExampleRegistryError):
        build_agent_task_session("Plan a local preview.", example_id="missing_example")
