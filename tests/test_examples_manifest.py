"""Examples manifest compatibility checks."""

from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_manifest() -> dict:
    path = ROOT / "examples" / "examples_manifest.json"
    assert path.exists()
    return json.loads(path.read_text(encoding="utf-8"))


def test_examples_manifest_lists_existing_offline_examples():
    manifest = _load_manifest()
    public_contract = json.loads((ROOT / "docs" / "public_contract_manifest.json").read_text(encoding="utf-8"))
    assert manifest["version_scope"] == "0.9.0rc9.dev0"
    assert manifest["current_public_prerelease"] == "v0.9.0rc8"
    examples = manifest["examples"]
    listed = {item["path"] for item in examples}
    expected = {
        "examples/specs/minimal_nanoparticle.json",
        "examples/specs/missing_wavelength_meep_preview.json",
        "examples/workflows/local_preview_request.json",
        "examples/e2e/local_optical_workflow.json",
        "examples/e2e/README.md",
        "examples/specs/gmsh_preview.json",
        "examples/specs/elmer_preview.json",
        "examples/specs/mpb_preview.json",
        "examples/specs/optiland_preview.json",
        "examples/api/README.md",
        "examples/api/frontend_fixture_manifest.json",
        "examples/quickstart/README.md",
        "examples/quickstart/nanoparticle_demo_spec.json",
        "examples/quickstart/quickstart_workflow_request.json",
        "examples/quickstart/zh_nanoparticle_prompt.txt",
        "examples/quickstart/zh_quickstart_notes.md",
    }
    assert expected <= listed
    contract_examples = {item["path"] for item in public_contract["examples"]}
    assert contract_examples <= listed
    for item in examples:
        assert (ROOT / item["path"]).exists(), item["path"]
        assert item["requires_network"] is False
        assert item["requires_external_solver"] is False
        assert item["requires_external_llm"] is False
        assert item["requires_proprietary_solver"] is False
    for item in public_contract["examples"]:
        assert item["requires_network"] is False
        assert item["requires_external_solver"] is False
        assert item["requires_external_llm"] is False
        assert item["requires_proprietary_solver"] is False


def test_examples_manifest_commands_are_parseable_and_offline_for_runnable_examples():
    manifest = _load_manifest()
    runnable = [
        command
        for item in manifest["examples"]
        for command in item["commands"]
    ]
    assert runnable
    for command in runnable:
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
