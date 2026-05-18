"""Adapter-native source/monitor preview mapping tests."""

from __future__ import annotations

from optical_spec_agent.optical_language import (
    diagnose_observable,
    infer_source_monitor_from_goal,
    map_source_monitor_to_adapter,
)


def _mapping(adapter_name: str, template_id: str, goal: str):
    inference = infer_source_monitor_from_goal(goal, template_id=template_id)
    diagnostics = diagnose_observable(
        inference.source_model,
        inference.monitor_model,
        template_id=template_id,
    )
    return map_source_monitor_to_adapter(
        adapter_name,
        inference.source_model,
        inference.monitor_model,
        diagnostics,
    )


def test_meep_mapping_includes_source_flux_and_dft_preview_metadata():
    mapping = _mapping("meep", "nanoparticle_plasmonics", "nanoparticle scattering")
    assert mapping.adapter_name == "meep"
    assert any("GaussianSource" in term for term in mapping.native_source_terms)
    assert any("flux" in term.lower() for term in mapping.native_monitor_terms)
    assert "scattering_spectrum" in mapping.supported_observables
    assert mapping.external_solver_executed is False
    assert mapping.preview_only is True


def test_mpb_mapping_includes_band_and_k_point_metadata():
    mapping = _mapping("mpb", "photonic_crystal_band_preview", "photonic crystal band")
    assert mapping.adapter_name == "mpb"
    assert any("k-point" in term.lower() for term in mapping.native_monitor_terms)
    assert "band_structure" in mapping.supported_observables
    assert mapping.requires_solver_for_real_result is True


def test_gmsh_mapping_explains_no_optical_observable_is_computed():
    mapping = _mapping("gmsh", "dielectric_metasurface_preview", "metasurface mesh")
    assert mapping.adapter_name == "gmsh"
    assert mapping.supported_observables == []
    assert any("No optical observable is computed" in warning for warning in mapping.warnings)
    assert mapping.external_solver_executed is False


def test_elmer_mapping_uses_fem_placeholders():
    mapping = _mapping("elmer", "waveguide_single_mode", "waveguide mode preview")
    assert mapping.adapter_name == "elmer"
    assert any("placeholder" in term.lower() for term in mapping.native_source_terms)
    assert any("ElmerSolver" in warning for warning in mapping.warnings)


def test_optiland_mapping_includes_ray_bundle_and_image_plane():
    mapping = _mapping("optiland", "paraxial_lens_imaging", "lens imaging preview")
    assert mapping.adapter_name == "optiland"
    assert any("ray bundle" in term.lower() for term in mapping.native_source_terms)
    assert any("image plane" in term.lower() for term in mapping.native_monitor_terms)


def test_unknown_adapter_mapping_returns_stable_diagnostics():
    mapping = _mapping("unknown_tool", "nanoparticle_plasmonics", "nanoparticle scattering")
    assert mapping.adapter_name == "unknown_tool"
    assert mapping.supported_observables == []
    assert mapping.unsupported_observables
    assert any("adapter" in item.lower() for item in mapping.diagnostics)
    assert mapping.external_solver_executed is False
