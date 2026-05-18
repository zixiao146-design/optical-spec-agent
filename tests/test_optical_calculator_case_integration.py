"""Agent session integration tests for optical calculator case helpers."""

from __future__ import annotations

from optical_spec_agent.agents.task_session import build_agent_task_session


def _ledger_names(goal: str, example_id: str | None = None) -> set[str]:
    session = build_agent_task_session(goal, example_id=example_id)
    return {entry.tool_name for entry in session.tool_call_ledger if entry.executed}


def test_thin_film_case_records_spectrum_calculator():
    names = _ledger_names(
        "Plan a local thin film coating preview.",
        example_id="thin_film_coating",
    )
    assert "optics.thin_film.spectrum" in names


def test_waveguide_case_records_sweep_calculator():
    names = _ledger_names(
        "Plan a local waveguide mode preview.",
        example_id="waveguide_mode",
    )
    assert "optics.waveguide.sweep" in names


def test_lens_case_records_paraxial_relay_calculator():
    names = _ledger_names(
        "Plan a local lens ray tracing preview.",
        example_id="lens_raytrace_preview",
    )
    assert "optics.paraxial.two_lens_relay" in names


def test_gaussian_beam_goal_records_series_calculator():
    names = _ledger_names("Plan a Gaussian beam waist and focus preview.")
    assert "optics.gaussian_beam.series" in names


def test_case_artifacts_include_calculator_result_summary():
    session = build_agent_task_session(
        "Plan a local thin film coating preview.",
        example_id="thin_film_coating",
    )
    artifacts = {artifact.artifact_id: artifact for artifact in session.artifacts}
    assert "calculator-preview" in artifacts
    assert artifacts["calculator-preview"].production_grade is False
    assert "Preview sweep" in artifacts["calculator-preview"].summary
