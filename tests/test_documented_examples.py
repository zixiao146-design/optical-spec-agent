"""Regression coverage for documented offline examples."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MINIMAL_SPEC = "examples/specs/minimal_nanoparticle.json"
WORKFLOW_REQUEST = "examples/workflows/local_preview_request.json"


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


def test_examples_readme_documents_offline_defaults():
    text = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    assert "offline by default" in text
    assert "no external solver" in text
    assert "external LLM" in text
    assert MINIMAL_SPEC in text
    assert WORKFLOW_REQUEST in text
    e2e = (ROOT / "examples" / "e2e" / "README.md").read_text(encoding="utf-8")
    assert "optical-spec validate examples/specs/minimal_nanoparticle.json" in e2e
    assert "optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json" in e2e
    assert "No proprietary optical software" in e2e


def test_documented_minimal_spec_validate_and_parse_examples():
    validate = _run("validate", MINIMAL_SPEC)
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "Executable: True" in validate.stdout
    assert "nanoparticle_on_film" in validate.stdout

    parse = _run("parse", MINIMAL_SPEC, "--json")
    assert parse.returncode == 0, parse.stdout + parse.stderr
    data = json.loads(parse.stdout)
    assert data["simulation"]["software_tool"]["value"] == "meep"
    assert data["simulation"]["solver_method"]["value"] == "fdtd"


def test_documented_adapter_list_and_workflow_plan_examples_are_json():
    adapters = _run("adapter-list", "--json")
    assert adapters.returncode == 0, adapters.stdout + adapters.stderr
    adapter_data = json.loads(adapters.stdout)
    assert {"meep", "mpb", "gmsh", "elmer", "optiland"} <= {
        item["tool_name"] for item in adapter_data["adapters"]
    }

    plan = _run("workflow-plan", WORKFLOW_REQUEST, "--json")
    assert plan.returncode == 0, plan.stdout + plan.stderr
    plan_data = json.loads(plan.stdout)
    assert plan_data["schema_version"] == "workflow_plan.v0.9"
    assert plan_data["parser_mode"] == "hybrid"
    assert plan_data["selected_tool"] == "mpb"
    assert plan_data["execute_policy"] == "no_execute_by_default"


def test_documented_e2e_workflow_plan_example_is_json():
    plan = _run("workflow-plan", "examples/e2e/local_optical_workflow.json", "--json")
    assert plan.returncode == 0, plan.stdout + plan.stderr
    plan_data = json.loads(plan.stdout)
    assert plan_data["schema_version"] == "workflow_plan.v0.9"
    assert plan_data["selected_tool"] == "mpb"
    assert plan_data["execute_policy"] == "no_execute_by_default"
