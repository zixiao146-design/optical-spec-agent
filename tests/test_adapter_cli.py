"""Tests for generic adapter CLI commands."""

import json
from pathlib import Path

from typer.testing import CliRunner

from optical_spec_agent.cli.main import app
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json


runner = CliRunner()


def _write_spec(tmp_path: Path, text: str, name: str = "spec.json") -> Path:
    spec = SpecService().process(text)
    path = tmp_path / name
    path.write_text(spec_to_json(spec), encoding="utf-8")
    return path


def test_adapter_list_human_output():
    result = runner.invoke(app, ["adapter-list"])
    assert result.exit_code == 0
    assert "mpb" in result.output
    assert "gmsh" in result.output
    assert "elmer" in result.output
    assert "optiland" in result.output


def test_adapter_list_json_output():
    result = runner.invoke(app, ["adapter-list", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    tools = {item["tool_name"] for item in data["adapters"]}
    assert {"meep", "mpb", "gmsh", "elmer", "optiland"} <= tools


def test_adapter_generate_mpb_writes_file(tmp_path):
    spec_path = _write_spec(
        tmp_path,
        "用 MPB 计算二维光子晶体的 band diagram，输出前 8 条能带。",
    )
    output = tmp_path / "mpb_band.py"
    result = runner.invoke(app, ["adapter-generate", str(spec_path), "--tool", "mpb", "--output", str(output)])
    assert result.exit_code == 0
    assert output.exists()
    assert "mpb.ModeSolver" in output.read_text(encoding="utf-8")


def test_adapter_generate_gmsh_writes_file(tmp_path):
    spec_path = _write_spec(
        tmp_path,
        "用 Gmsh 为 Si3N4 脊波导横截面生成 FEM 网格，SiO2 下包层。",
    )
    output = tmp_path / "waveguide.geo"
    result = runner.invoke(app, ["adapter-generate", str(spec_path), "--tool", "gmsh", "--output", str(output)])
    assert result.exit_code == 0
    assert output.exists()
    assert "SetFactory" in output.read_text(encoding="utf-8")


def test_adapter_generate_elmer_with_mesh_writes_file(tmp_path):
    spec_path = _write_spec(tmp_path, "用 Elmer 做 Si3N4 波导 FEM 模式分析。")
    output = tmp_path / "case.sif"
    result = runner.invoke(
        app,
        [
            "adapter-generate",
            str(spec_path),
            "--tool",
            "elmer",
            "--mesh",
            "outputs/waveguide.msh",
            "--output",
            str(output),
        ],
    )
    assert result.exit_code == 0
    assert output.exists()
    assert "outputs/waveguide.msh" in output.read_text(encoding="utf-8")


def test_adapter_generate_optiland_writes_file(tmp_path):
    spec_path = _write_spec(tmp_path, "用 Optiland 设计一个简单单透镜成像系统，计算 spot diagram 和 MTF。")
    output = tmp_path / "optiland_design.py"
    result = runner.invoke(app, ["adapter-generate", str(spec_path), "--tool", "optiland", "--output", str(output)])
    assert result.exit_code == 0
    assert output.exists()
    assert "Optiland MVP scaffold" in output.read_text(encoding="utf-8")


def test_adapter_generate_json_outputs_valid_json(tmp_path):
    spec_path = _write_spec(tmp_path, "Use MPB to compute a photonic crystal band diagram.")
    result = runner.invoke(app, ["adapter-generate", str(spec_path), "--tool", "mpb", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["selected_adapter"] == "mpb"
    assert "generated_content" in data


def test_adapter_generate_strict_fails_on_missing_required(tmp_path):
    spec_path = _write_spec(tmp_path, "用 Optiland 设计一个成像系统，计算 MTF。")
    result = runner.invoke(app, ["adapter-generate", str(spec_path), "--tool", "optiland", "--strict"])
    assert result.exit_code != 0
    assert "Missing required" in result.output or "missing_required" in result.output


def test_adapter_generate_non_strict_allows_preview_scaffold(tmp_path):
    spec_path = _write_spec(tmp_path, "用 Optiland 设计一个成像系统，计算 MTF。")
    result = runner.invoke(app, ["adapter-generate", str(spec_path), "--tool", "optiland"])
    assert result.exit_code == 0
    assert "Generated content" in result.output
    assert "Optiland MVP scaffold" in result.output


def test_existing_meep_generate_still_works(tmp_path):
    spec_path = _write_spec(
        tmp_path,
        "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
        "平面波正入射，波长范围 400-900 nm，输出散射谱。",
    )
    output = tmp_path / "smoke.py"
    result = runner.invoke(app, ["meep-generate", str(spec_path), "--mode", "smoke", "--output", str(output)])
    assert result.exit_code == 0
    assert output.exists()
    assert "SMOKE TEST PASSED" in output.read_text(encoding="utf-8")
