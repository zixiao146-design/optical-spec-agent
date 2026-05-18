from optical_spec_agent.agents.task_session import build_agent_task_session


def test_agent_session_includes_source_monitor_and_diagnostics():
    session = build_agent_task_session(
        "Create a local preview workflow for a silver nanoparticle scattering case.",
        example_id="nanoparticle_plasmonics",
    )

    assert session.source_model is not None
    assert session.monitor_model is not None
    assert session.source_model.source_type == "plane_wave"
    assert session.monitor_model.monitor_type == "scattering_spectrum"
    assert session.optical_language_diagnostics.safe_to_preview is True
    assert session.optical_language_diagnostics.safe_to_run_solver is False
    assert "polarization" in session.source_model.defaulted_fields


def test_agent_session_ledger_records_source_monitor_tools():
    session = build_agent_task_session(
        "Design an anti-reflection coating for glass at 550 nm and run only local preview calculators."
    )
    ledger = {entry.tool_name: entry for entry in session.tool_call_ledger}

    assert ledger["optical_language.infer_source_monitor"].executed is True
    assert ledger["optical_language.diagnose_missing_inputs"].executed is True
    assert ledger["external_llm"].executed is False
    assert ledger["external_solver.meep"].executed is False
