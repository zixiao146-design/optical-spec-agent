"""Public contract manifest checks for the v1.0 freeze candidate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from optical_spec_agent.adapters.registry import list_adapters


ROOT = Path(__file__).resolve().parents[1]


def _load_manifest() -> dict:
    path = ROOT / "docs" / "public_contract_manifest.json"
    assert path.exists()
    return json.loads(path.read_text(encoding="utf-8"))


def test_public_contract_manifest_baseline_and_package_metadata():
    manifest = _load_manifest()
    assert manifest["version_scope"] == "0.9.0rc4.dev0"
    assert manifest["current_public_prerelease"] == "v0.9.0rc3"
    assert manifest["release_state"]["v1_0_0_released"] is False
    assert manifest["release_state"]["v0_9_0rc4_tag_created"] is False
    assert manifest["release_state"]["pypi_published"] is False
    assert manifest["release_state"]["testpypi_uploaded"] is False
    assert manifest["package"]["name"] == "optical-spec-agent"
    assert manifest["package"]["console_script"] == "optical-spec"


def test_public_contract_manifest_examples_are_local_and_existing():
    manifest = _load_manifest()
    for item in manifest["examples"]:
        assert (ROOT / item["path"]).exists(), item["path"]
        assert item["requires_network"] is False
        assert item["requires_external_solver"] is False
        assert item["requires_external_llm"] is False
        assert item["requires_proprietary_solver"] is False


def test_public_contract_manifest_adapters_match_registry_and_cli():
    manifest = _load_manifest()
    manifest_names = {item["name"] for item in manifest["adapters"]}
    registry_names = {metadata.tool_name for metadata in list_adapters()}
    assert manifest_names == registry_names == {"meep", "mpb", "gmsh", "elmer", "optiland"}
    assert all(item["requires_external_solver_by_default"] is False for item in manifest["adapters"])

    result = subprocess.run(
        ["optical-spec", "adapter-list", "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    cli_names = {item["tool_name"] for item in json.loads(result.stdout)["adapters"]}
    assert cli_names == manifest_names


def test_public_contract_manifest_non_goals_keep_claims_conservative():
    manifest = _load_manifest()
    non_goals = set(manifest["non_goals"])
    assert "production-grade physical validation" in non_goals
    assert "formal convergence proof" in non_goals
    assert "default external solver execution" in non_goals
    assert "default external LLM requirement" in non_goals
    assert "default proprietary solver dependency" in non_goals
