"""Tests for Gmsh adapter MVP."""

from optical_spec_agent.adapters.gmsh import GmshAdapter
from optical_spec_agent.services.spec_service import SpecService


def test_gmsh_can_handle_waveguide_mesh_spec():
    spec = SpecService().process(
        "用 Gmsh 为 Si3N4 脊波导横截面生成 FEM 网格，SiO2 下包层。"
    )
    assert GmshAdapter().can_handle(spec)


def test_gmsh_waveguide_geo_contains_physical_groups():
    spec = SpecService().process(
        "用 Gmsh 为 Si3N4 脊波导横截面生成 FEM 网格，SiO2 下包层。"
    )
    result = GmshAdapter().generate(spec)
    assert result.tool == "gmsh"
    assert result.language == "geo"
    assert 'SetFactory("OpenCASCADE");' in result.content
    assert "Physical Surface" in result.content
    assert "Physical Volume" in result.content


def test_gmsh_nanoparticle_on_film_mentions_sphere_film_gap():
    spec = SpecService().process(
        "用 Gmsh 为 80 nm Au sphere on a 100 nm Au film with a SiO2 gap of 5 nm 生成几何网格。"
    )
    result = GmshAdapter().generate(spec)
    assert "nanoparticle-on-film" in result.content
    assert "Sphere" in result.content
    assert "film" in result.content
    assert "gap" in result.content


def test_gmsh_missing_geometry_reports_missing_required():
    spec = SpecService().process("用 Gmsh 生成一个网格。")
    result = GmshAdapter().generate(spec)
    assert "geometry_material.geometry_definition" in result.missing_required
    assert any("geometry_definition" in warning for warning in result.warnings)
