"""Run documented offline CLI examples without external solvers or LLM providers."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["optical-spec", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )


def test_documented_help_and_adapter_list_examples():
    help_result = _run("--help")
    assert help_result.returncode == 0, help_result.stdout + help_result.stderr
    assert "adapter-list" in help_result.stdout

    adapters = _run("adapter-list", "--json")
    assert adapters.returncode == 0, adapters.stdout + adapters.stderr
    data = json.loads(adapters.stdout)
    assert {"meep", "mpb", "gmsh", "elmer", "optiland"} <= {
        item["tool_name"] for item in data["adapters"]
    }


def test_documented_schema_parse_validate_examples(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema = _run("schema", "--output", str(schema_path))
    assert schema.returncode == 0, schema.stdout + schema.stderr
    assert "task" in json.loads(schema_path.read_text(encoding="utf-8"))["properties"]

    spec_path = tmp_path / "quickstart_spec.json"
    parse = _run(
        "parse",
        "用 Meep FDTD 仿真金纳米球散射。",
        "--parser",
        "rule",
        "--output",
        str(spec_path),
    )
    assert parse.returncode == 0, parse.stdout + parse.stderr
    assert spec_path.exists()

    validate = _run("validate", str(spec_path))
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "Optical Spec Agent" in validate.stdout


def test_documented_workflow_plan_example_is_offline_json():
    result = _run(
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
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["selected_tool"] == "mpb"
    assert data["execute_policy"] == "no_execute_by_default"
    assert "Workflow v0.9 is synchronous/local orchestration only." in data["limitations"]
