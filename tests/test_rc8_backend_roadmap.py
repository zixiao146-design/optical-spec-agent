"""rc8 backend roadmap and capability gap audit checks."""

from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_current_versions_remain_post_rc8_dev_state():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    init_text = _read("src/optical_spec_agent/__init__.py")
    readiness = _read("docs/release_readiness_current.md")
    assert pyproject["project"]["version"] == "0.9.0rc9.dev0"
    assert '__version__ = "0.9.0rc9.dev0"' in init_text
    assert "Current public prerelease: `v0.9.0rc8`" in readiness
    assert "Current main development version: `0.9.0rc9.dev0`" in readiness
    assert "`0.9.0rc9.dev0` is not a public release" in readiness
    assert "`v0.9.0rc9` tag has not been created" in readiness
    assert "`v1.0.0` tag has not been created" in readiness
    assert "PyPI published: no" in readiness
    assert "TestPyPI upload for `0.9.0rc9.dev0`: not performed" in readiness


def test_git_tags_for_future_releases_are_absent_when_git_metadata_is_available():
    if not (ROOT / ".git").exists():
        return
    for tag in ["v0.9.0rc9", "v1.0.0"]:
        result = subprocess.run(
            ["git", "tag", "--list", tag],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == ""


def test_rc8_backend_roadmap_exists_and_classifies_capabilities():
    text = _read("docs/rc8_backend_roadmap.md")
    required = [
        "Current public prerelease: `v0.9.0rc8`",
        "Current main development version: `0.9.0rc9.dev0`",
        "`0.9.0rc9.dev0` is not a public release",
        "`v0.9.0rc9` tag has not been created",
        "`v1.0.0` tag has not been created",
        "PyPI remains unpublished",
        "Done / stable enough",
        "Needs backend hardening",
        "Deferred / non-blocker",
        "Future / Phase 2",
        "Not a Goal",
        "Sub-agent reality",
        "Tool-call ledger",
        "Material library",
        "Optical calculators",
        "Source/monitor diagnostics",
        "Observable diagnostics",
        "Adapter-native mappings",
        "Adapter golden coverage",
        "Design requirement templates",
        "Natural-language to optical-language matching",
        "Frontend Agent Studio",
        "PyPI publication",
        "v1.0.0 release criteria",
        "Elmer remains Level 2 + Level-3-ready",
    ]
    for phrase in required:
        assert phrase in text
    assert "No production-grade physical validation is claimed" in text
    assert "No formal convergence proof is claimed" in text


def test_rc8_capability_gap_audit_exists_and_keeps_boundaries():
    text = _read("docs/rc8_capability_gap_audit.md")
    required = [
        "Current public prerelease: `v0.9.0rc8`",
        "Current main development version: `0.9.0rc9.dev0`",
        "`v0.9.0rc9` tag: not created",
        "`v1.0.0` tag: not created",
        "PyPI: not published",
        "PyPI publication approval: not granted",
        "TestPyPI upload for `0.9.0rc9.dev0`: not performed",
        "Gap Matrix",
        "Capability Gaps Found",
        "Calculator depth remains preview-oriented",
        "Material provenance should be strengthened",
        "Natural-language matching should add negative and ambiguous examples",
        "Adapter-native mapping evidence is metadata-only",
        "Elmer remains explicitly deferred",
    ]
    for phrase in required:
        assert phrase in text
    assert "not production-grade physical validation" in text
    assert "Formal convergence proof: not claimed" in text
    assert "Elmer Level 3: deferred" in text


def test_rc8_to_v1_0_decision_path_exists_and_blocks_release_actions():
    text = _read("docs/rc8_to_v1_0_decision_path.md")
    required = [
        "Current public prerelease: `v0.9.0rc8`",
        "Current main development version: `0.9.0rc9.dev0`",
        "Gate 1: Continue rc9 Backend Engineering",
        "Gate 2: Decide Whether to Prepare a Future v0.9.0rc9 Draft",
        "Gate 3: Decide PyPI Publication Separately",
        "Gate 4: Decide v1.0.0 Planning",
        "Creating `v0.9.0rc9` tag",
        "Creating any GitHub release",
        "Uploading TestPyPI",
        "Publishing PyPI",
        "Creating `v1.0.0` tag or release",
        "Marking Elmer as Level 3",
        "Do not claim production-grade physical validation",
        "Do not claim formal convergence proof",
    ]
    for phrase in required:
        assert phrase in text


def test_readme_and_status_docs_link_rc8_backend_audit_package():
    for path in [
        "README.md",
        "README.zh-CN.md",
        "docs/README.md",
        "docs/release_readiness_current.md",
        "docs/v1_0_readiness_scorecard.md",
        "docs/backend_functionality_status.md",
    ]:
        text = _read(path)
        assert "rc8_backend_roadmap.md" in text
        assert "rc8_capability_gap_audit.md" in text
        assert "rc8_to_v1_0_decision_path.md" in text
