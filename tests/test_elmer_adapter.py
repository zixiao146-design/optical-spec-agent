"""Tests for Elmer adapter MVP."""

from optical_spec_agent.adapters.elmer import ElmerAdapter
from optical_spec_agent.services.spec_service import SpecService


def test_elmer_can_handle_fem_waveguide_spec():
    spec = SpecService().process(
        "用 Elmer 做 Si3N4 波导 FEM 模式分析，输出有效折射率和模场。"
    )
    assert ElmerAdapter().can_handle(spec)


def test_elmer_generates_sif_sections():
    spec = SpecService().process(
        "用 Elmer 做 Si3N4 波导 FEM 模式分析，输出有效折射率和模场。"
    )
    result = ElmerAdapter().generate(spec, mesh_path="outputs/waveguide.msh")
    assert result.tool == "elmer"
    assert result.language == "sif"
    assert "Header" in result.content
    assert "Simulation" in result.content
    assert "Material 1" in result.content
    assert "Solver 1" in result.content
    assert "Boundary Condition" in result.content
    assert "outputs/waveguide.msh" in result.content


def test_elmer_missing_mesh_warns():
    spec = SpecService().process("用 Elmer FEM 做波导模式分析。")
    result = ElmerAdapter().generate(spec)
    assert "mesh" in result.missing_required
    assert any("mesh" in warning.lower() for warning in result.warnings)
