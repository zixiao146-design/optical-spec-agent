"""Regression tests for the documented public CLI contract."""

from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_public_contract_manifest() -> dict:
    path = ROOT / "docs" / "public_contract_manifest.json"
    assert path.exists()
    return json.loads(path.read_text(encoding="utf-8"))


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["optical-spec", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )


def test_optical_spec_help_lists_public_commands():
    result = _run_cli("--help")
    assert result.returncode == 0, result.stdout + result.stderr
    for command in [
        "parse",
        "validate",
        "schema",
        "adapter-list",
        "adapter-generate",
        "llm-eval",
        "workflow-plan",
        "workflow-run",
        "workflow-replay",
        "workflow-report",
    ]:
        assert command in result.stdout

    contract = (ROOT / "docs" / "cli_contract.md").read_text(encoding="utf-8")
    for command in ["parse", "validate", "schema", "adapter-list", "workflow-plan"]:
        assert f"`{command}`" in contract

    manifest = _load_public_contract_manifest()
    for command in manifest["cli"]["documented_command_names"]:
        assert command in result.stdout
        assert f"`{command}`" in contract


def test_documented_help_fragments_remain_available():
    help_checks = {
        ("parse", "--help"): ["--parser", "--llm-provider", "--json", "--output"],
        ("schema", "--help"): ["--output"],
        ("validate", "--help"): ["PATH"],
        ("adapter-list", "--help"): ["--json"],
        ("workflow-plan", "--help"): ["--parser", "--llm-provider", "--tool", "--json"],
    }
    for args, fragments in help_checks.items():
        result = _run_cli(*args)
        assert result.returncode == 0, result.stdout + result.stderr
        for fragment in fragments:
            assert fragment in result.stdout


def test_offline_json_commands_have_stable_top_level_shape(tmp_path):
    manifest = _load_public_contract_manifest()
    schema_path = tmp_path / "schema.json"
    schema = _run_cli("schema", "--output", str(schema_path))
    assert schema.returncode == 0, schema.stdout + schema.stderr
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
    assert {"task", "physics", "simulation", "output"} <= set(schema_data["properties"])

    adapters = _run_cli("adapter-list", "--json")
    assert adapters.returncode == 0, adapters.stdout + adapters.stderr
    adapter_data = json.loads(adapters.stdout)
    assert set(manifest["cli"]["json_top_level_shapes"]["adapter-list"]) <= set(adapter_data)
    assert isinstance(adapter_data["adapters"], list)
    assert {"meep", "mpb", "gmsh", "elmer", "optiland"} <= {
        item["tool_name"] for item in adapter_data["adapters"]
    }
    for item in adapter_data["adapters"]:
        assert {
            "tool_name",
            "display_name",
            "solver_family",
            "output_language",
            "output_extension",
            "current_status",
            "limitations",
        } <= set(item)

    plan = _run_cli(
        "workflow-plan",
        "用 MPB 计算二维光子晶体 band diagram。",
        "--parser",
        "hybrid",
        "--llm-provider",
        "mock",
        "--tool",
        "mpb",
        "--json",
    )
    assert plan.returncode == 0, plan.stdout + plan.stderr
    plan_data = json.loads(plan.stdout)
    assert set(manifest["cli"]["json_top_level_shapes"]["workflow-plan"]) <= set(plan_data)
    assert plan_data["schema_version"] == "workflow_plan.v0.9"
    assert plan_data["selected_tool"] == "mpb"
    assert plan_data["execute_policy"] == "no_execute_by_default"


def test_parse_rule_json_is_offline_default_path():
    result = _run_cli(
        "parse",
        "用 Meep FDTD 仿真金纳米球散射。",
        "--parser",
        "rule",
        "--json",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["simulation"]["software_tool"]["value"] == "meep"
    assert data["simulation"]["solver_method"]["value"] == "fdtd"


def test_manifest_runnable_cli_commands_exit_successfully():
    manifest = _load_public_contract_manifest()
    contract = (ROOT / "docs" / "cli_contract.md").read_text(encoding="utf-8")
    for item in manifest["cli"]["commands"]:
        command = item["name"]
        assert command.startswith("optical-spec")
        result = subprocess.run(
            shlex.split(command),
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        if item["json_output"]:
            json.loads(result.stdout)
        command_name = shlex.split(command)[1] if len(shlex.split(command)) > 1 else "--help"
        if command_name != "--help":
            assert f"`{command_name}`" in contract
