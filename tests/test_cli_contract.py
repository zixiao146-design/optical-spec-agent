"""Regression tests for the documented public CLI contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
    schema_path = tmp_path / "schema.json"
    schema = _run_cli("schema", "--output", str(schema_path))
    assert schema.returncode == 0, schema.stdout + schema.stderr
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
    assert {"task", "physics", "simulation", "output"} <= set(schema_data["properties"])

    adapters = _run_cli("adapter-list", "--json")
    assert adapters.returncode == 0, adapters.stdout + adapters.stderr
    adapter_data = json.loads(adapters.stdout)
    assert "adapters" in adapter_data
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
    assert {
        "schema_version",
        "planned_steps",
        "selected_tool",
        "execute_policy",
        "expected_artifacts",
        "limitations",
    } <= set(plan_data)
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
