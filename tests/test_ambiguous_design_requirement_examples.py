"""Ambiguous design requirement example fixture tests."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AMBIGUOUS = ROOT / "examples" / "design_requirements_ambiguous"


def test_ambiguous_design_requirement_examples_exist_and_are_safe():
    cases = {
        "generic_optical_system",
        "waveguide_or_coating",
        "lens_optimization_underconstrained",
        "unknown_application",
    }
    for case in cases:
        case_dir = AMBIGUOUS / case
        assert (case_dir / "goal_en.txt").exists()
        assert (case_dir / "goal_zh.txt").exists()
        assert (case_dir / "expected_match_result.json").exists()
        readme = (case_dir / "README.md").read_text(encoding="utf-8").lower()
        assert "do not execute" in readme or "no solver" in readme
        assert "external llm" in readme
        assert "production-grade" in readme or "preview/design-assist" in readme
