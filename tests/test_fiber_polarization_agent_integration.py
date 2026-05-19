"""Agent session integration for fiber and polarization preview calculators."""

from __future__ import annotations

from optical_spec_agent.agents.task_session import build_agent_task_session


def _executed_tools(goal: str) -> set[str]:
    session = build_agent_task_session(goal)
    return {entry.tool_name for entry in session.tool_call_ledger if entry.executed}


def test_fiber_coupling_goal_triggers_fiber_calculator_and_artifact():
    goal = "Preview fiber coupling with mode overlap and Gaussian beam assumptions."
    session = build_agent_task_session(goal)
    tools = _executed_tools(goal)
    assert session.application_domain_id == "fiber_coupling_preview"
    assert session.domain_cross_check_status == "pass"
    assert "optics.fiber_coupling.gaussian_mode_overlap" in tools
    assert any(
        artifact.source_endpoint == "/api/optics/fiber-coupling"
        for artifact in session.artifacts
    )
    assert session.external_solver_executed is False


def test_polarization_goal_triggers_jones_calculator_and_artifact():
    goal = "Create a polarization waveplate preview with input polarization and retardance questions."
    session = build_agent_task_session(goal)
    tools = _executed_tools(goal)
    assert session.application_domain_id == "polarization_optics_preview"
    assert session.domain_cross_check_status == "pass"
    assert "optics.polarization.jones" in tools
    assert any(
        artifact.source_endpoint == "/api/optics/polarization-jones"
        for artifact in session.artifacts
    )
    assert session.external_solver_executed is False
