"""Tests for the generic adapter registry."""

import pytest

from optical_spec_agent.adapters.registry import (
    AdapterRegistryError,
    dispatch_adapter,
    get_adapter,
    list_adapters,
)
from optical_spec_agent.services.spec_service import SpecService


def test_list_adapters_includes_v07_tools():
    tools = {metadata.tool_name for metadata in list_adapters()}
    assert {"meep", "mpb", "gmsh", "elmer", "optiland"} <= tools


def test_get_adapter_known_tools():
    assert get_adapter("mpb").tool_name == "mpb"
    assert get_adapter("gmsh").tool_name == "gmsh"
    assert get_adapter("elmer").tool_name == "elmer"
    assert get_adapter("optiland").tool_name == "optiland"


def test_get_adapter_unknown_tool_errors():
    with pytest.raises(AdapterRegistryError, match="Unknown adapter"):
        get_adapter("not-a-solver")


def test_auto_dispatch_meep_like_spec():
    spec = SpecService().process(
        "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
        "平面波正入射，波长范围 400-900 nm，输出散射谱。"
    )
    assert dispatch_adapter(spec).tool_name == "meep"


@pytest.mark.parametrize(
    ("text", "expected_tool"),
    [
        ("用 MPB 计算二维光子晶体的 band diagram，输出前 8 条能带。", "mpb"),
        ("用 Gmsh 为 Si3N4 脊波导横截面生成 FEM 网格。", "gmsh"),
        ("用 Elmer 做 Si3N4 波导 FEM 模式分析。", "elmer"),
        ("用 Optiland 设计一个简单单透镜成像系统，计算 spot diagram 和 MTF。", "optiland"),
    ],
)
def test_auto_dispatch_v07_adapter_intents(text, expected_tool):
    spec = SpecService().process(text)
    assert dispatch_adapter(spec).tool_name == expected_tool


def test_forced_dispatch_for_new_adapters():
    spec = SpecService().process("计算一个普通光学结构。")
    assert dispatch_adapter(spec, preferred_tool="mpb").tool_name == "mpb"
    assert dispatch_adapter(spec, preferred_tool="gmsh").tool_name == "gmsh"
    assert dispatch_adapter(spec, preferred_tool="elmer").tool_name == "elmer"
    assert dispatch_adapter(spec, preferred_tool="optiland").tool_name == "optiland"
