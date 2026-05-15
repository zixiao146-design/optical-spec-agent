"""TestPyPI Trusted Publishing status checks for 0.9.0rc6.dev0."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_DOC = ROOT / "docs" / "testpypi_status_v0.9.0rc6.dev0.md"


def test_testpypi_status_records_success_without_pypi_publish_or_release():
    assert STATUS_DOC.exists()
    text = STATUS_DOC.read_text(encoding="utf-8")

    assert "TestPyPI upload: completed" in text
    assert "TestPyPI uploaded: yes" in text
    assert "PyPI published: no" in text
    assert "PyPI publication approval: not granted" in text
    assert "GitHub tag created: no" in text
    assert "GitHub release created: no" in text
    assert "GitHub Actions Trusted Publishing" in text
    assert "workflow: .github/workflows/testpypi-trusted-publish.yml" in text
    assert "trigger: workflow_dispatch" in text
    assert "confirmation input: UPLOAD_TESTPYPI" in text
    assert "token used: no local token; trusted publishing/OIDC" in text


def test_testpypi_status_records_clean_install_and_dependency_caveat():
    text = STATUS_DOC.read_text(encoding="utf-8")

    assert "clean install from TestPyPI: passed" in text
    assert "import version check: passed" in text
    assert "optical_spec_agent.__version__: 0.9.0rc6.dev0" in text
    assert "optical-spec --help: passed" in text
    assert "optical-spec adapter-list --json: passed" in text
    assert "Dependency-index Note" in text
    assert "unrelated FASTAPI package" in text
    assert "installed runtime dependencies from PyPI" in text
    assert "installed optical-spec-agent from TestPyPI with --no-deps" in text


def test_testpypi_status_keeps_validation_claims_bounded():
    text = STATUS_DOC.read_text(encoding="utf-8")

    assert "no production-grade physical validation" in text
    assert "no formal convergence proof" in text
    assert "external solvers not run by default" in text
    assert "external LLM not required by default" in text
    assert "proprietary solvers not required by default" in text
    assert "This TestPyPI upload does not authorize PyPI publication" in text
    assert "This TestPyPI upload does not create a GitHub release" in text
    assert "This TestPyPI upload does not create any tag" in text
