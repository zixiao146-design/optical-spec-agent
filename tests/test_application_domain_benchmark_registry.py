"""Application-domain benchmark registry tests."""

from __future__ import annotations

from optical_spec_agent.examples.domain_benchmarks import list_domain_scenarios


def test_application_domain_benchmark_registry_has_required_scenarios():
    scenarios = list_domain_scenarios()
    ids = {scenario.scenario_id for scenario in scenarios}
    assert len(scenarios) >= 19
    for required in {
        "nanoparticle_plasmonics_positive",
        "thin_film_coating_positive",
        "slab_waveguide_positive",
        "photonic_crystal_positive",
        "dielectric_metasurface_positive",
        "lens_ray_optics_positive",
        "gaussian_beam_focusing_positive",
        "imaging_system_preview_positive",
        "fiber_coupling_preview_positive",
        "polarization_optics_preview_positive",
        "waveguide_or_coating_ambiguous",
        "lens_or_gaussian_focus_ambiguous",
        "generic_optical_system_ambiguous",
        "lens_missing_focal_length",
        "nanoparticle_missing_radius_material",
        "waveguide_missing_core_thickness",
        "full_zemax_optimization_request",
        "full_lumerical_fdtd_request",
        "production_grade_validation_request",
    }:
        assert required in ids


def test_application_domain_benchmark_registry_covers_scenario_types_and_safety():
    scenarios = list_domain_scenarios()
    types = {scenario.scenario_type for scenario in scenarios}
    assert {"positive", "ambiguous", "underconstrained", "unsupported", "unsafe_or_blocked"} <= types
    assert sum(1 for scenario in scenarios if scenario.scenario_type == "positive") >= 10
    assert sum(1 for scenario in scenarios if scenario.scenario_type == "ambiguous") >= 3
    assert sum(1 for scenario in scenarios if scenario.scenario_type == "underconstrained") >= 3
    assert sum(
        1 for scenario in scenarios if scenario.scenario_type in {"unsupported", "unsafe_or_blocked"}
    ) >= 3
    for scenario in scenarios:
        assert scenario.goal_en
        assert scenario.goal_zh
        assert scenario.preview_only is True
        assert scenario.production_grade_validation_claimed is False
        assert scenario.formal_convergence_proof_claimed is False
