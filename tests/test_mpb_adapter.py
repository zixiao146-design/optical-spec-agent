"""Tests for MPB adapter MVP."""

from optical_spec_agent.adapters.mpb import MPBAdapter
from optical_spec_agent.services.spec_service import SpecService


def test_mpb_can_handle_photonic_crystal_spec():
    spec = SpecService().process(
        "用 MPB 计算二维光子晶体的 band diagram，输出前 8 条能带。"
    )
    assert MPBAdapter().can_handle(spec)


def test_mpb_generates_preview_script():
    spec = SpecService().process(
        "用 MPB 计算二维光子晶体的 band diagram，输出前 8 条能带。"
    )
    result = MPBAdapter().generate(spec)
    assert result.tool == "mpb"
    assert result.language == "python"
    assert "from meep import mpb" in result.content
    assert "mpb.ModeSolver" in result.content
    assert "k_points" in result.content


def test_mpb_missing_kpoints_uses_warning_defaults():
    spec = SpecService().process("Use MPB to compute a photonic crystal mode.")
    result = MPBAdapter().generate(spec)
    assert any("k_points" in item for item in result.defaults_applied)
    assert "Gamma-X-M-Gamma" in result.content


def test_mpb_waveguide_mode_spec_generates_script():
    spec = SpecService().process(
        "Use MPB mode solver to compute the eigenmode of a Si3N4 waveguide "
        "at 1550 nm and output mode profile."
    )
    result = MPBAdapter().generate(spec)
    assert "Si3N4" in result.content
    assert "MPB preview" in result.content
