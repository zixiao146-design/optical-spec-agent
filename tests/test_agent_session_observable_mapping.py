"""Agent session observable diagnostics and adapter mapping tests."""

from __future__ import annotations

from optical_spec_agent.agents.task_session import build_agent_task_session


def test_agent_session_includes_observable_diagnostics_and_adapter_mapping():
    session = build_agent_task_session(
        "Create a local preview workflow for a silver nanoparticle scattering case.",
        example_id="nanoparticle_plasmonics",
    )
    assert session.observable_diagnostics
    assert {
        diagnostic.observable_kind for diagnostic in session.observable_diagnostics
    } >= {"scattering_spectrum", "extinction_spectrum"}
    assert session.adapter_source_monitor_mapping is not None
    assert session.adapter_source_monitor_mapping.adapter_name == "meep"
    assert session.adapter_source_monitor_mapping.external_solver_executed is False
    ledger = {entry.tool_name: entry for entry in session.tool_call_ledger}
    assert ledger["optical_language.diagnose_observable"].executed is True
    assert ledger["optical_language.map_source_monitor_to_adapter"].executed is True
    assert any(artifact.artifact_id == "observable-diagnostics" for artifact in session.artifacts)
    assert any(
        artifact.artifact_type == "adapter_preview"
        and artifact.artifact_id == "adapter-native-source-monitor-preview"
        for artifact in session.artifacts
    )
    assert "observable" in " ".join(session.recommended_next_actions).lower()
