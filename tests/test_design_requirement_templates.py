"""Design requirement template tests."""

from __future__ import annotations

import json
from pathlib import Path

from optical_spec_agent.examples.requirements import list_requirement_templates


ROOT = Path(__file__).resolve().parents[1]


def test_all_design_requirement_templates_exist_and_are_safe():
    templates = {item.template_id: item for item in list_requirement_templates()}
    assert set(templates) == {
        "thin_film_ar_coating",
        "gaussian_beam_focus",
        "slab_waveguide_single_mode",
        "paraxial_lens_imaging",
        "photonic_crystal_band_preview",
        "dielectric_metasurface_preview",
        "nanoparticle_plasmonics",
    }
    for template in templates.values():
        assert template.natural_language_goal_en
        assert template.natural_language_goal_zh
        assert template.expected_tool_calls
        assert "requirements.match_template" in template.expected_tool_calls
        assert "requirements.extract_optical_intent" in template.expected_tool_calls
        assert template.safety.no_solver_by_default is True
        assert template.safety.no_external_llm is True
        assert template.safety.production_grade_validation_claimed is False
        assert template.safety.formal_convergence_proof_claimed is False


def test_design_requirement_example_files_exist():
    examples_dir = ROOT / "examples" / "design_requirements"
    for template in list_requirement_templates():
        folder = examples_dir / template.template_id
        for filename in [
            "requirement.json",
            "goal_en.txt",
            "goal_zh.txt",
            "expected_tool_calls.json",
            "README.md",
        ]:
            assert (folder / filename).exists(), f"{template.template_id}/{filename}"
        requirement = json.loads((folder / "requirement.json").read_text(encoding="utf-8"))
        expected = json.loads((folder / "expected_tool_calls.json").read_text(encoding="utf-8"))
        assert requirement["template_id"] == template.template_id
        assert expected["expected_tool_calls"]
        assert expected["external_solver_executed"] is False
        assert expected["external_llm_required"] is False

