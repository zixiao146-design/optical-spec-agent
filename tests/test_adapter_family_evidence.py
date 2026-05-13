"""Offline evidence regression for registered adapter families."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CASES = {
    "gmsh": {
        "spec": "examples/specs/gmsh_preview.json",
        "language": "geo",
        "status": "success",
    },
    "elmer": {
        "spec": "examples/specs/elmer_preview.json",
        "language": "sif",
        "status": "success",
        "extra": ["--mesh", "examples/meshes/waveguide.msh"],
    },
    "mpb": {
        "spec": "examples/specs/mpb_preview.json",
        "language": "python",
        "status": "success",
    },
    "optiland": {
        "spec": "examples/specs/optiland_preview.json",
        "language": "python",
        "status": "warning",
    },
}


def _adapter_generate(tool: str, spec: str, extra: list[str] | None = None) -> dict:
    args = ["optical-spec", "adapter-generate", spec, "--tool", tool, "--json"]
    if extra:
        args.extend(extra)
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def _expected_fragments(tool: str) -> list[str]:
    path = ROOT / "tests" / "fixtures" / "adapter_golden" / tool / "expected_fragments.txt"
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _expected_metadata_keys(tool: str) -> list[str]:
    path = ROOT / "tests" / "fixtures" / "adapter_golden" / tool / "expected_metadata_keys.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_adapter_family_golden_fragments_are_stable():
    for tool, case in CASES.items():
        payload = _adapter_generate(tool, case["spec"], case.get("extra"))
        assert payload["selected_adapter"] == tool
        assert payload["language"] == case["language"]
        assert payload["status"] == case["status"]
        assert payload["generated_content"]
        assert payload["output_path"] is None
        assert any("does not run" in item.lower() for item in payload["limitations"])

        content = payload["generated_content"]
        for fragment in _expected_fragments(tool):
            assert fragment in content or fragment in "\n".join(payload["limitations"])


def test_adapter_family_metadata_keys_are_cli_visible():
    adapters = subprocess.run(
        ["optical-spec", "adapter-list", "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert adapters.returncode == 0, adapters.stdout + adapters.stderr
    by_tool = {item["tool_name"]: item for item in json.loads(adapters.stdout)["adapters"]}

    for tool in CASES:
        metadata = by_tool[tool]
        for key in _expected_metadata_keys(tool):
            assert key in metadata
        assert metadata["current_status"] in {"preview", "mvp"}
        assert metadata["output_language"]
        assert metadata["output_extension"]

