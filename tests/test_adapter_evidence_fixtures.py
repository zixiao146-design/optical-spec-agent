"""Adapter evidence fixtures for local preview/golden behavior."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = "examples/specs/missing_wavelength_meep_preview.json"
FRAGMENTS = ROOT / "tests" / "fixtures" / "adapter_golden" / "meep_missing_wavelength_expected_fragments.txt"


def test_meep_missing_wavelength_fixture_records_preview_defaults():
    result = subprocess.run(
        ["optical-spec", "adapter-generate", SPEC, "--tool", "meep", "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    content = payload["generated_content"]

    assert payload["selected_adapter"] == "meep"
    assert payload["status"] == "warning"
    assert "wavelength_range: 400–900 nm" in payload["defaults_applied"]
    assert any("wavelength_range" in warning for warning in payload["warnings"])
    assert any("not production-grade physical validation" in item for item in payload["limitations"])

    for fragment in FRAGMENTS.read_text(encoding="utf-8").splitlines():
        if fragment.strip():
            assert fragment in content


def test_meep_adapter_evidence_fixture_does_not_run_external_solver():
    text = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    assert "It does not run Meep" in text
    assert "no external solver" in text
