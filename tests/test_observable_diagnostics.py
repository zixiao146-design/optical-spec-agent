"""Observable diagnostic taxonomy tests."""

from __future__ import annotations

from optical_spec_agent.optical_language import (
    diagnose_observable,
    infer_source_monitor_from_goal,
)


def _diagnostic_kinds(template_id: str, goal: str) -> set[str]:
    inference = infer_source_monitor_from_goal(goal, template_id=template_id)
    diagnostics = diagnose_observable(
        inference.source_model,
        inference.monitor_model,
        template_id=template_id,
    )
    for diagnostic in diagnostics:
        assert diagnostic.preview_supported is True
        assert diagnostic.production_grade_validation_claimed is False
        assert diagnostic.formal_convergence_proof_claimed is False
        assert diagnostic.required_inputs
        assert diagnostic.default_assumptions
        assert diagnostic.adapter_compatibility
    return {diagnostic.observable_kind for diagnostic in diagnostics}


def test_observable_diagnostics_cover_key_templates():
    assert {
        "scattering_spectrum",
        "extinction_spectrum",
    }.issubset(
        _diagnostic_kinds(
            "nanoparticle_plasmonics",
            "silver nanoparticle scattering preview",
        )
    )
    assert {
        "reflectance",
        "transmittance",
    }.issubset(
        _diagnostic_kinds(
            "thin_film_ar_coating",
            "anti-reflection coating preview",
        )
    )
    assert "focal_spot" in _diagnostic_kinds(
        "gaussian_beam_focus",
        "Gaussian beam focus preview",
    )
    assert "band_structure" in _diagnostic_kinds(
        "photonic_crystal_band_preview",
        "photonic crystal band preview",
    )


def test_real_observable_results_require_solver_where_appropriate():
    inference = infer_source_monitor_from_goal(
        "silver nanoparticle scattering preview",
        template_id="nanoparticle_plasmonics",
    )
    diagnostics = diagnose_observable(
        inference.source_model,
        inference.monitor_model,
        template_id="nanoparticle_plasmonics",
    )
    assert any(item.solver_execution_required_for_real_result for item in diagnostics)
    assert any("preview" in " ".join(item.notes).lower() for item in diagnostics)


def test_mesh_region_observable_can_support_gmsh_golden_case():
    inference = infer_source_monitor_from_goal("mesh region physical group preview")
    monitor = inference.monitor_model.model_copy(
        update={
            "monitor_type": "unknown",
            "observable": "mesh region / physical group preview",
            "region": "source and monitor physical groups",
        }
    )
    diagnostics = diagnose_observable(inference.source_model, monitor)
    assert {item.observable_kind for item in diagnostics} == {"mesh_region"}
