from __future__ import annotations

import pytest

from optical_spec_agent.examples.registry import (
    ExampleRegistryError,
    get_optical_design_example,
    list_optical_design_examples,
)


def test_example_registry_lists_bundled_optical_design_examples():
    examples = list_optical_design_examples()
    ids = {example.example_id for example in examples}
    assert {
        "nanoparticle_plasmonics",
        "thin_film_coating",
        "waveguide_mode",
        "photonic_crystal_band",
        "dielectric_metasurface_preview",
        "lens_raytrace_preview",
    }.issubset(ids)
    for example in examples:
        assert example.spec_path.startswith("examples/optical_design/")
        assert example.has_agent_trace is True
        assert example.safety.external_solver_executed is False
        assert example.safety.external_llm_required is False
        assert example.safety.production_grade_validation_claimed is False
        assert example.safety.formal_convergence_proof_claimed is False


def test_example_registry_detail_and_invalid_example_behavior():
    detail = get_optical_design_example("nanoparticle_plasmonics")
    assert detail.summary.example_id == "nanoparticle_plasmonics"
    assert detail.spec["suggested_adapter"] == "meep"
    assert "expected_agents" in detail.expected_agent_trace
    assert "No solver is executed by default." in detail.safety_boundaries

    with pytest.raises(ExampleRegistryError):
        get_optical_design_example("../not-valid")
