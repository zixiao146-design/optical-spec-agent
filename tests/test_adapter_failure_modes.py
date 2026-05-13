"""Adapter failure/default-mode coverage without external solver execution."""

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


def test_unsupported_adapter_name_is_structured_error():
    result = _run("adapter-generate", "examples/specs/gmsh_preview.json", "--tool", "missing-adapter", "--json")
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert payload["selected_adapter"] == "missing-adapter"
    assert any("unknown adapter" in error.lower() for error in payload["errors"])


def test_malformed_adapter_input_is_structured_error(tmp_path: Path):
    bad = tmp_path / "bad_adapter_input.json"
    bad.write_text('{"not_task": {}}', encoding="utf-8")
    result = _run("adapter-generate", str(bad), "--tool", "gmsh", "--json")
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert any("missing 'task' section" in error for error in payload["errors"])


def test_missing_required_fields_report_scaffold_warning():
    result = _run("adapter-generate", "examples/specs/minimal_nanoparticle.json", "--tool", "elmer", "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["selected_adapter"] == "elmer"
    assert payload["status"] == "warning"
    assert "mesh" in payload["missing_required"]
    assert any("mesh" in warning.lower() for warning in payload["warnings"])
    assert any("does not run ElmerSolver" in item for item in payload["limitations"])


def test_missing_optional_physical_fields_produce_adapter_defaults():
    result = _run("adapter-generate", "examples/specs/mpb_preview.json", "--tool", "mpb", "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["selected_adapter"] == "mpb"
    assert "k_points: Gamma-X-M-Gamma path" in payload["defaults_applied"]
    assert "num_bands: 8" in payload["defaults_applied"]
    assert payload["output_path"] is None
