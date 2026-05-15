"""End-to-end offline user journey regression checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MINIMAL_SPEC = "examples/specs/minimal_nanoparticle.json"
WORKFLOW_REQUEST = "examples/workflows/local_preview_request.json"
E2E_WORKFLOW_REQUEST = "examples/e2e/local_optical_workflow.json"


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


def test_offline_user_journey_docs_and_fixtures_exist():
    for relative in [
        "docs/offline_user_journey.md",
        "examples/e2e/README.md",
        "examples/e2e/local_optical_workflow.json",
        "examples/e2e/expected_cli_fragments.txt",
        "examples/e2e/expected_workflow_keys.json",
    ]:
        assert (ROOT / relative).exists(), relative

    text = (ROOT / "docs" / "offline_user_journey.md").read_text(encoding="utf-8")
    assert "no external solver" in text
    assert "no external LLM" in text
    assert "no proprietary" in text
    assert "0.9.0rc6.dev0" in text
    assert "v0.9.0rc5" in text


def test_offline_user_journey_core_commands_run_locally():
    help_result = _run("--help")
    assert help_result.returncode == 0, help_result.stdout + help_result.stderr
    assert "adapter-list" in help_result.stdout
    assert "workflow-plan" in help_result.stdout

    validate = _run("validate", MINIMAL_SPEC)
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "Executable: True" in validate.stdout

    parse = _run("parse", MINIMAL_SPEC, "--json")
    assert parse.returncode == 0, parse.stdout + parse.stderr
    parsed = json.loads(parse.stdout)
    assert parsed["simulation"]["software_tool"]["value"] == "meep"
    assert parsed["simulation"]["solver_method"]["value"] == "fdtd"

    adapters = _run("adapter-list", "--json")
    assert adapters.returncode == 0, adapters.stdout + adapters.stderr
    adapter_payload = json.loads(adapters.stdout)
    assert {"meep", "mpb", "gmsh", "elmer", "optiland"} <= {
        item["tool_name"] for item in adapter_payload["adapters"]
    }


def test_offline_user_journey_workflow_shapes_are_stable():
    expected = json.loads(
        (ROOT / "examples" / "e2e" / "expected_workflow_keys.json").read_text(encoding="utf-8")
    )
    for request in [WORKFLOW_REQUEST, E2E_WORKFLOW_REQUEST]:
        result = _run("workflow-plan", request, "--json")
        assert result.returncode == 0, result.stdout + result.stderr
        payload = json.loads(result.stdout)
        for key in expected["required_top_level_keys"]:
            assert key in payload
        assert payload["schema_version"] == expected["expected_schema_version"]
        assert payload["execute_policy"] == expected["expected_execute_policy"]
        assert payload["selected_tool"] == expected["expected_selected_tool"]
        assert "No external solver execution is planned by default." in payload["limitations"]
