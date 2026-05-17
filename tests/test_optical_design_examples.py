import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "optical_design"
EXAMPLE_IDS = [
    "nanoparticle_plasmonics",
    "thin_film_coating",
    "waveguide_mode",
    "photonic_crystal_band",
    "dielectric_metasurface_preview",
    "lens_raytrace_preview",
]


def test_optical_design_examples_exist_and_preserve_safety_boundaries():
    for example_id in EXAMPLE_IDS:
        folder = EXAMPLES / example_id
        spec_path = folder / "spec.json"
        readme_path = folder / "README.md"
        trace_path = folder / "expected_agent_trace.json"
        assert spec_path.exists()
        assert readme_path.exists()
        assert trace_path.exists()
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        assert spec["safety"]["external_solver_executed"] is False
        assert spec["safety"]["external_llm_required"] is False
        assert spec["safety"]["production_grade_validation_claimed"] is False
        assert spec["safety"]["formal_convergence_proof_claimed"] is False
        readme = readme_path.read_text(encoding="utf-8")
        assert "No solver is executed by default." in readme
        assert "No production-grade physical validation is claimed." in readme
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        assert "MaterialAgent" in trace["expected_agents"]
        assert "SafetyAgent" in trace["expected_agents"]
