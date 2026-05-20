"""Schema compatibility policy evidence and deterministic validation checks."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from optical_spec_agent.cli.main import _load_spec_file
from optical_spec_agent.validators.spec_validator import SpecValidator


ROOT = Path(__file__).resolve().parents[1]
VALID_SPEC = ROOT / "examples" / "specs" / "minimal_nanoparticle.json"


def test_schema_compatibility_policy_exists_and_sets_boundaries():
    text = (ROOT / "docs" / "schema_compatibility_policy.md").read_text(encoding="utf-8")
    for phrase in [
        "Current main release draft: `0.9.0rc8`",
        "Current public prerelease: `v0.9.0rc7`",
        "Public fields",
        "Preview/scaffold fields",
        "Migration notes",
        "Validation errors should remain deterministic",
        "must not require an external LLM",
        "must not require an external solver",
    ]:
        assert phrase in text


def test_fixed_valid_spec_validation_passes():
    spec = _load_spec_file(VALID_SPEC)
    validated = SpecValidator().validate(spec)
    assert validated.validation_status.is_executable is True
    assert validated.validation_status.errors == []


def test_fixed_invalid_spec_validation_is_deterministic(tmp_path: Path):
    data = json.loads(VALID_SPEC.read_text(encoding="utf-8"))
    invalid = copy.deepcopy(data)
    invalid["simulation"]["source_setting"] = {
        "value": None,
        "status": "missing",
        "note": "Intentional invalid fixture",
    }
    invalid_path = tmp_path / "missing_source_setting.json"
    invalid_path.write_text(json.dumps(invalid, indent=2), encoding="utf-8")

    first = SpecValidator().validate(_load_spec_file(invalid_path)).validation_status
    second = SpecValidator().validate(_load_spec_file(invalid_path)).validation_status
    assert first.is_executable is False
    assert first.errors == second.errors
    assert any("simulation.source_setting" in error for error in first.errors)
