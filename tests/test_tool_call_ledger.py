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
        "material_catalog.suggest",
        "example_registry.load",
        "agent_trace.build",
        "workflow_plan.preview",
        "adapter_preview.generate",
        "optics.thin_film.calculate",
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
    assert "optics.waveguide.v_number" in names

    lens = build_agent_task_session("Plan a paraxial lens imaging preview.")
    names = {entry.tool_name for entry in lens.tool_call_ledger}
    assert "optics.paraxial.thin_lens" in names

    gaussian = build_agent_task_session("Plan a Gaussian beam propagation preview.")
    names = {entry.tool_name for entry in gaussian.tool_call_ledger}
    assert "optics.gaussian_beam.propagate" in names

