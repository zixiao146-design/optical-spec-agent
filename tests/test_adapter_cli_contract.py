"""Adapter CLI listing and support-matrix consistency checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from optical_spec_agent.adapters.registry import list_adapters


ROOT = Path(__file__).resolve().parents[1]


def test_adapter_list_json_matches_registry_and_docs():
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
    payload = json.loads(result.stdout)
    cli_adapters = {item["tool_name"]: item for item in payload["adapters"]}
    registry_adapters = {item.tool_name: item for item in list_adapters()}
    matrix = (ROOT / "docs" / "adapter_support_matrix.md").read_text(encoding="utf-8")

    assert set(cli_adapters) == set(registry_adapters) == {"meep", "mpb", "gmsh", "elmer", "optiland"}
    for name, metadata in cli_adapters.items():
        assert f"`{name}`" in matrix
        for key in [
            "tool_name",
            "display_name",
            "solver_family",
            "output_language",
            "output_extension",
            "supported_solver_methods",
            "supported_physical_systems",
            "current_status",
            "limitations",
            "consumed_fields",
        ]:
            assert key in metadata
        assert metadata["current_status"] == registry_adapters[name].current_status
        assert any("does not run" in item.lower() or "execution is explicit" in item.lower() for item in metadata["limitations"])


def test_adapter_cli_listing_is_offline_contract():
    matrix = (ROOT / "docs" / "adapter_support_matrix.md").read_text(encoding="utf-8")
    assert "External solvers are not run by default" in matrix
    assert "External LLM" in matrix
    assert "no production-grade physical validation" in matrix.lower()
    assert "PyPI/TestPyPI remain unpublished" in matrix

