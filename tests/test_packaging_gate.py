"""Packaging gate tests for pre-TestPyPI / pre-PyPI readiness."""

from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _pyproject() -> dict:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_pyproject_core_packaging_metadata_present():
    project = _pyproject()["project"]
    assert project["name"] == "optical-spec-agent"
    assert project["version"] == "0.9.0rc6.dev0"
    assert project["description"]
    assert project["readme"] == "README.md"
    assert project["requires-python"].startswith(">=3.11")
    assert project["license"]["text"] == "MIT"
    assert project["scripts"]["optical-spec"] == "optical_spec_agent.cli.main:app"
    assert {"pydantic>=2.0", "fastapi>=0.110", "typer>=0.9"} <= set(project["dependencies"])


def test_test_extra_declares_pytest_and_httpx():
    test_deps = _pyproject()["project"]["optional-dependencies"]["test"]
    assert any(dep.startswith("pytest") for dep in test_deps)
    assert any(dep.startswith("httpx") for dep in test_deps)


def test_packaging_gate_docs_and_pypi_decision_are_present():
    packaging_gate = (ROOT / "docs" / "packaging_gate.md").read_text(encoding="utf-8")
    pypi_decision = (ROOT / "docs" / "pypi_publication_decision.md").read_text(encoding="utf-8")
    assert "PyPI status: not published" in packaging_gate
    assert "TestPyPI status: not published" in packaging_gate
    assert "Current package version on `main`: `0.9.0rc6.dev0`" in packaging_gate
    assert "Current public prerelease: `v0.9.0rc5`" in packaging_gate
    assert "`v0.9.0rc6` tag: not created" in packaging_gate
    assert "docs/testpypi_dry_run_gate.md" in packaging_gate
    assert "scripts/testpypi_preflight.sh" in packaging_gate
    assert "python -m twine check dist/*" in packaging_gate
    assert "does not upload, publish, create tags, or create" in packaging_gate
    assert "docs/v1_0_stability_gate.md" in packaging_gate
    assert "TestPyPI upload requires explicit maintainer approval" in packaging_gate
    assert "No automatic package publishing" in packaging_gate
    assert "Do not publish automatically from release scripts" in packaging_gate
    assert "PyPI published: no" in pypi_decision
    assert "TestPyPI uploaded: no" in pypi_decision
    assert "Current main development version: `0.9.0rc6.dev0`" in pypi_decision
    assert "explicit maintainer approval" in pypi_decision
    assert "TestPyPI upload approval status: granted for 0.9.0rc6.dev0 only" in pypi_decision
    assert "PyPI publication approval: not granted" in pypi_decision


def test_smoke_release_script_never_uploads_or_creates_releases():
    script = (ROOT / "scripts" / "smoke_release.sh").read_text(encoding="utf-8")
    forbidden = [
        "twine upload",
        "gh release create",
        "pypi upload",
        "testpypi",
    ]
    lowered = script.lower()
    for phrase in forbidden:
        assert phrase not in lowered
    assert "OSA_SMOKE_VERIFY_WHEEL" in script
    assert "OSA_SMOKE_ALLOW_PUBLISH" in script


def test_testpypi_preflight_script_never_uploads_or_creates_releases():
    script = (ROOT / "scripts" / "testpypi_preflight.sh").read_text(encoding="utf-8")
    lowered = script.lower()
    forbidden = [
        "twine upload",
        "gh release create",
        "git push",
        "pypi upload",
    ]
    for phrase in forbidden:
        assert phrase not in lowered
    assert "python -m twine check dist/*" in script
    assert "NO UPLOAD PERFORMED" in script
