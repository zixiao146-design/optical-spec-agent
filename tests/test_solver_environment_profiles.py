"""Optional solver environment profile manifest tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_solver_environment_profiles_manifest_is_portable():
    path = ROOT / "validation" / "solver_environment_profiles.json"
    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["default_executes_solver"] is False
    profiles = {item["profile_id"]: item for item in payload["profiles"]}
    assert set(profiles) == {"current", "osa-solvers", "homebrew-cli", "deferred-elmer"}
    assert profiles["current"]["python"] == "current"
    assert profiles["osa-solvers"]["python_env_var"] == "OSA_SOLVER_PYTHON"
    assert "expected_python_hint" in profiles["osa-solvers"]
    assert "not required in CI" in profiles["osa-solvers"]["path_policy"]
    assert profiles["homebrew-cli"]["command_detection_only"] is True
    assert "Elmer remains deferred" in profiles["deferred-elmer"]["description"]
    # The manifest may document a maintainer-local hint, but tests must not
    # require that local path to exist.
    assert Path(profiles["osa-solvers"]["expected_python_hint"]).is_absolute()
