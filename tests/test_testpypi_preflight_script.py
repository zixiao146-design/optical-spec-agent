"""No-upload TestPyPI preflight script checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_testpypi_preflight_script_exists_and_checks_local_package_readiness():
    path = ROOT / "scripts" / "testpypi_preflight.sh"
    assert path.exists()
    script = path.read_text(encoding="utf-8")
    assert "set -euo pipefail" in script
    assert "NO UPLOAD PERFORMED" in script
    assert "python -m build" in script
    assert "python -m twine check dist/*" in script
    assert "Wheel install smoke venv" in script
    assert "optical_spec_agent.__version__" in script
    assert "optical-spec\" --help" in script
    assert "OSA_TESTPYPI_PREFLIGHT_VENV" in script
    assert "OSA_TESTPYPI_WHEEL_VENV" in script


def test_testpypi_preflight_script_contains_no_upload_or_secret_handling():
    script = (ROOT / "scripts" / "testpypi_preflight.sh").read_text(encoding="utf-8")
    lowered = script.lower()
    forbidden = [
        "twine upload",
        "python -m twine upload",
        "gh release create",
        "git push",
        "__token__",
        "gh_token",
        "github_token",
        "pypi_token",
        "testpypi_token",
        "upload.pypi.org",
        "test.pypi.org/legacy",
        "pypi.org/legacy",
    ]
    for phrase in forbidden:
        assert phrase not in lowered
