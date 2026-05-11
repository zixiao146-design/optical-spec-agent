"""Tests for Optiland adapter MVP."""

from optical_spec_agent.adapters.optiland import OptilandAdapter
from optical_spec_agent.services.spec_service import SpecService


def test_optiland_can_handle_ray_tracing_spec():
    spec = SpecService().process(
        "Use Optiland for ray tracing of a simple singlet lens imaging system "
        "and calculate spot diagram."
    )
    assert OptilandAdapter().can_handle(spec)


def test_optiland_forced_scaffold_reports_missing_lens_data():
    spec = SpecService().process("计算一个普通光学任务。")
    result = OptilandAdapter().generate(spec)
    assert result.tool == "optiland"
    assert result.language == "python"
    assert "import optiland" in result.content
    assert "lens_surface_sequence" in result.content
    assert any("lens_surface_sequence" in item for item in result.missing_required)
    assert result.limitations


def test_optiland_scaffold_is_guarded_import():
    spec = SpecService().process("用 Optiland 设计一个成像系统，计算 MTF。")
    result = OptilandAdapter().generate(spec)
    assert "try:" in result.content
    assert "except ImportError" in result.content
    assert "Optiland scaffold" in result.content
