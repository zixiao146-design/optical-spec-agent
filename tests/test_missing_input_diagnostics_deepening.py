"""Critical/optional missing-input diagnostic tests."""

from optical_spec_agent.agents.task_session import build_agent_task_session
from optical_spec_agent.optical_language import diagnose_missing_inputs


def test_underconstrained_lens_goal_asks_for_lens_inputs():
    session = build_agent_task_session("Help me optimize a lens.")
    assert session.match_confidence == "medium"
    assert "focal_length" in session.missing_critical_inputs
    assert "object_distance" in session.missing_critical_inputs
    assert "aperture" in session.missing_optional_inputs
    assert "field_of_view" in session.missing_optional_inputs
    assert session.recommended_questions
    assert session.optical_language_diagnostics.safe_to_preview is True
    assert session.optical_language_diagnostics.safe_to_run_solver is False


def test_nanoparticle_goal_reports_particle_and_film_context_when_absent():
    session = build_agent_task_session("请为银纳米颗粒散射生成本地预览工作流")
    assert session.requirement_template_id == "nanoparticle_plasmonics"
    assert "particle_radius_or_diameter" in session.missing_critical_inputs
    assert "film_thickness" in session.missing_critical_inputs or "film_thickness" in session.missing_optional_inputs
    assert session.optical_language_diagnostics.safe_to_preview is True
    assert session.optical_language_diagnostics.safe_to_run_solver is False


def test_unknown_goal_diagnostics_keep_solver_blocked():
    diagnostics = diagnose_missing_inputs(goal="Design an optical system.", template_id=None)
    assert "optical_application" in diagnostics.missing_critical_inputs
    assert diagnostics.safe_to_preview is True
    assert diagnostics.safe_to_run_solver is False
