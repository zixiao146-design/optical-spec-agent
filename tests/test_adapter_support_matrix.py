"""Keep adapter support matrix documentation aligned with the registry."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from optical_spec_agent.adapters.registry import list_adapters
from optical_spec_agent.cli.main import app


ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_adapter_support_matrix_mentions_registered_adapters():
    text = (ROOT / "docs" / "adapter_support_matrix.md").read_text(encoding="utf-8").lower()
    for metadata in list_adapters():
        assert f"`{metadata.tool_name}`" in text
        assert metadata.current_status in text
    assert "external solvers are not run by default" in text
    assert "production-grade physical validation" in text


def test_adapter_list_json_matches_registry_tools():
    result = runner.invoke(app, ["adapter-list", "--json"])
    assert result.exit_code == 0
    cli_tools = {item["tool_name"] for item in json.loads(result.output)["adapters"]}
    registry_tools = {metadata.tool_name for metadata in list_adapters()}
    assert cli_tools == registry_tools == {"meep", "mpb", "gmsh", "elmer", "optiland"}


def test_adapter_metadata_declares_no_default_external_execution():
    for metadata in list_adapters():
        limitations = " ".join(metadata.limitations).lower()
        assert any(
            phrase in limitations
            for phrase in [
                "does not run",
                "execution is explicit",
                "scaffold only",
                "generates scripts only",
            ]
        ), metadata
