"""Basic CLI failure-mode regression coverage."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_SPEC = ROOT / "examples" / "specs" / "minimal_nanoparticle.json"


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


def test_validate_invalid_json_fails_with_stable_category(tmp_path: Path):
    bad = tmp_path / "invalid.json"
    bad.write_text("{not-json", encoding="utf-8")
    result = _run("validate", str(bad))
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "JSONDecodeError" in combined or "Expecting property name" in combined


def test_validate_missing_required_field_reports_not_executable(tmp_path: Path):
    data = json.loads(VALID_SPEC.read_text(encoding="utf-8"))
    data["simulation"]["source_setting"] = {
        "value": None,
        "status": "missing",
        "note": "Intentional failure-mode fixture",
    }
    path = tmp_path / "missing_required.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    result = _run("validate", str(path))
    assert result.returncode == 0
    assert "NOT EXECUTABLE" in result.stdout
    assert "simulation.source_setting" in result.stdout


def test_unsupported_adapter_name_returns_structured_error():
    result = _run("adapter-generate", str(VALID_SPEC.relative_to(ROOT)), "--tool", "not-a-tool", "--json")
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert payload["selected_adapter"] == "not-a-tool"
    assert any("not_a_tool" in error for error in payload["errors"])


def test_workflow_plan_invalid_local_request_file_fails(tmp_path: Path):
    request = tmp_path / "workflow_request.json"
    request.write_text("{}", encoding="utf-8")
    result = _run("workflow-plan", str(request), "--json")
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert any("text field" in error for error in payload["errors"])


def test_default_offline_parse_path_does_not_require_external_llm():
    result = _run("parse", str(VALID_SPEC.relative_to(ROOT)), "--json")
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["simulation"]["software_tool"]["value"] == "meep"
