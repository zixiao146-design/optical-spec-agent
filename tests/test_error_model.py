"""Error model documentation and offline failure behavior checks."""

from __future__ import annotations

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


def test_error_model_doc_covers_default_offline_failures():
    text = (ROOT / "docs" / "error_model.md").read_text(encoding="utf-8")
    required = [
        "Invalid JSON",
        "Invalid spec",
        "Unsupported adapter",
        "Invalid workflow request",
        "Optional external solver not installed",
        "Optional external LLM not configured",
        "Proprietary solver unavailable",
        "default offline path should fail deterministically",
        "Proprietary tools are not default requirements",
    ]
    for phrase in required:
        assert phrase in text


def test_invalid_json_failure_is_local_and_deterministic(tmp_path: Path):
    bad = tmp_path / "invalid.json"
    bad.write_text("{not-json", encoding="utf-8")
    result = _run("validate", str(bad))
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "JSONDecodeError" in combined or "Expecting property name" in combined


def test_proprietary_solver_unavailability_is_not_default_failure_mode():
    result = _run("validate", "examples/specs/minimal_nanoparticle.json")
    assert result.returncode == 0, result.stdout + result.stderr
    combined = result.stdout + result.stderr
    for proprietary_name in ["Zemax", "Lumerical", "COMSOL", "Ansys"]:
        assert proprietary_name not in combined
