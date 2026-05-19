"""Agent session requirement-template integration tests."""

from __future__ import annotations

from optical_spec_agent.agents.task_session import build_agent_task_session


def test_agent_session_includes_requirement_template_and_optical_language():
    session = build_agent_task_session(
        "Design an anti-reflection coating for glass at 550 nm and keep it local."
    )
    assert session.requirement_template_id == "thin_film_ar_coating"
    assert session.optical_language_summary["physical_system"] == "thin_film_stack"
    assert session.missing_required_inputs
    assert session.default_assumptions_applied
    ledger = {entry.tool_name: entry for entry in session.tool_call_ledger}
    assert ledger["requirements.match_template"].executed is True
    assert ledger["requirements.extract_optical_intent"].executed is True
    assert ledger["requirements.match_ambiguity_check"].executed is True
    assert ledger["optical_language.generate_disambiguation_questions"].executed is True
    assert ledger["optical_language.infer_source_monitor"].executed is True
    assert ledger["optical_language.diagnose_missing_inputs"].executed is True
    assert ledger["optics.thin_film.spectrum"].executed is True
    assert session.match_confidence in {"medium", "high"}
    assert isinstance(session.candidate_templates, list)
    assert isinstance(session.recommended_questions, list)
    assert isinstance(session.missing_critical_inputs, list)
    assert isinstance(session.missing_optional_inputs, list)
    assert "natural language" in session.plan_steps[0].title.lower()


def test_expected_calculator_ledgers_for_design_requirement_goals():
    cases = [
        (
            "Design an anti-reflection coating for glass at 550 nm.",
            "thin_film_ar_coating",
            "optics.thin_film.spectrum",
        ),
        (
            "Estimate whether a SiN waveguide is single mode at 1550 nm.",
            "slab_waveguide_single_mode",
            "optics.waveguide.sweep",
        ),
        (
            "Preview a lens imaging relay using two thin lenses.",
            "paraxial_lens_imaging",
            "optics.paraxial.two_lens_relay",
        ),
        (
            "Preview Gaussian beam waist and focus through a thin lens.",
            "gaussian_beam_focus",
            "optics.gaussian_beam.series",
        ),
    ]
    for goal, template_id, tool_name in cases:
        session = build_agent_task_session(goal)
        ledger = {entry.tool_name: entry for entry in session.tool_call_ledger}
        assert session.requirement_template_id == template_id
        assert ledger[tool_name].executed is True
        assert session.external_solver_executed is False
        assert session.external_llm_required is False
