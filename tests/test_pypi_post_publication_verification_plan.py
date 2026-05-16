"""PyPI post-publication verification plan checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pypi_post_publication_verification_plan_covers_clean_install_and_cli():
    path = ROOT / "docs" / "pypi_post_publication_verification_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "clean virtual environment" in text
    assert "python -m pip install optical-spec-agent==<version>" in text
    assert "Import version check" in text
    assert "optical-spec --help" in text
    assert "optical-spec adapter-list --json" in text
    assert "optical-spec validate examples/specs/minimal_nanoparticle.json" in text
    assert "optical-spec parse examples/specs/minimal_nanoparticle.json --json" in text
    assert "optical-spec workflow-plan examples/workflows/local_preview_request.json --json" in text
    assert "post-publication status doc" in text


def test_pypi_post_publication_verification_plan_bounds_claims_and_yank_policy():
    text = (ROOT / "docs" / "pypi_post_publication_verification_plan.md").read_text(
        encoding="utf-8"
    )

    assert "not approval to publish PyPI" in text
    assert "Yanking may reduce accidental installs" in text
    assert "PyPI publication does not imply production-grade physical validation" in text
    assert "formal\nconvergence proof" in text
    assert "default external solver\nexecution" in text
