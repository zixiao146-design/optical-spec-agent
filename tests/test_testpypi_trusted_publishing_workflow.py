"""TestPyPI Trusted Publishing workflow guardrails."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "testpypi-trusted-publish.yml"
STATUS_DOC = ROOT / "docs" / "testpypi_status_v0.9.0rc6.dev0.md"


def test_testpypi_trusted_publishing_workflow_is_manual_and_scoped_to_testpypi():
    assert WORKFLOW.exists()
    text = WORKFLOW.read_text(encoding="utf-8")
    lowered = text.lower()

    assert "workflow_dispatch:" in text
    assert "push:" not in lowered
    assert "pull_request:" not in lowered
    assert "id-token: write" in text
    assert "pypa/gh-action-pypi-publish" in text
    assert "repository-url: https://test.pypi.org/legacy/" in text
    assert "UPLOAD_TESTPYPI" in text
    assert 'assert version == "0.9.0rc6.dev0"' in text


def test_testpypi_trusted_publishing_workflow_uses_no_tokens_or_release_commands():
    text = WORKFLOW.read_text(encoding="utf-8")
    lowered = text.lower()

    forbidden = [
        "twine upload",
        "password:",
        "TESTPYPI_TOKEN",
        "PYPI_TOKEN",
        "gh release create",
        "git tag",
    ]
    for phrase in forbidden:
        assert phrase.lower() not in lowered


def test_testpypi_trusted_publishing_status_links_workflow():
    assert STATUS_DOC.exists()
    text = STATUS_DOC.read_text(encoding="utf-8")
    assert ".github/workflows/testpypi-trusted-publish.yml" in text
    assert "GitHub Actions Trusted Publishing" in text
    assert "workflow_dispatch" in text
    assert "UPLOAD_TESTPYPI" in text
    assert "token used: no local token; trusted publishing/OIDC" in text
