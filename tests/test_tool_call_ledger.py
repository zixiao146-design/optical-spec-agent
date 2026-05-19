"""Tool-call ledger tests."""

from __future__ import annotations

from optical_spec_agent.agents.task_session import build_agent_task_session


def test_agent_session_includes_tool_call_ledger():
    session = build_agent_task_session(
        "Plan a thin film coating preview without external solver execution.",
        example_id="thin_film_coating",
    )
    ledger = {entry.tool_name: entry for entry in session.tool_call_ledger}

    for internal in [
        "requirements.match_template",
        "requirements.extract_optical_intent",
        "requirements.match_ambiguity_check",
        "optical_language.generate_disambiguation_questions",
        "optical_language.infer_source_monitor",
        "optical_language.diagnose_missing_inputs",
        "optical_language.diagnose_observable",
        "optical_language.map_source_monitor_to_adapter",
        "material_catalog.suggest",
        "example_registry.load",
        "agent_trace.build",
        "workflow_plan.preview",
        "adapter_preview.generate",
        "optics.thin_film.spectrum",
    ]:
        assert ledger[internal].executed is True
        assert ledger[internal].default_allowed is True
        assert ledger[internal].status == "executed"
        assert ledger[internal].safety_note

    for blocked in [
        "external_solver.meep",
        "external_solver.gmsh",
        "external_solver.mpb",
        "external_solver.elmer",
        "external_solver.optiland",
        "external_llm",
        "testpypi_upload",
        "pypi_publish",
        "git_tag_create",
        "github_release_create",
    ]:
        assert ledger[blocked].executed is False
        assert ledger[blocked].default_allowed is False
        assert ledger[blocked].status in {"blocked", "requires_explicit_approval"}
        assert ledger[blocked].safety_note


def test_calculator_ledger_entries_are_intent_dependent():
    waveguide = build_agent_task_session("Plan a local waveguide V-number preview.")
    names = {entry.tool_name for entry in waveguide.tool_call_ledger}
    assert "optics.waveguide.sweep" in names

    lens = build_agent_task_session("Plan a paraxial lens imaging preview.")
    names = {entry.tool_name for entry in lens.tool_call_ledger}
    assert "optics.paraxial.two_lens_relay" in names

    gaussian = build_agent_task_session("Plan a Gaussian beam propagation preview.")
    names = {entry.tool_name for entry in gaussian.tool_call_ledger}
    assert "optics.gaussian_beam.series" in names


def test_backend_report_and_cross_checks_reflect_ledger_reality():
    from optical_spec_agent.agents.capability_report import generate_backend_capability_report

    report = generate_backend_capability_report()
    assert any(tool.tool_name == "optical_calculators" for tool in report.internal_tools)
    assert any(tool.tool_name == "source_monitor_inference" for tool in report.internal_tools)
    assert any(tool.tool_name == "missing_input_diagnostics" for tool in report.internal_tools)
    assert any(tool.tool_name == "observable_diagnostics" for tool in report.internal_tools)
    assert any(tool.tool_name == "adapter_native_mapping" for tool in report.internal_tools)
    assert any(tool.tool_name == "adapter_native_golden_coverage" for tool in report.internal_tools)
    assert report.adapter_native_golden_coverage.status == "ok"
    assert all(action.executed is False for action in report.blocked_external_actions)
    assert any(
        check.example_id == "thin_film_coating"
        and check.status == "pass"
        and check.expected_calculator == "optics.thin_film"
        for check in report.design_case_cross_checks
    )
