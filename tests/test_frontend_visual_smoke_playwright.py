"""Playwright visual smoke configuration checks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


def test_playwright_visual_smoke_files_and_scripts_exist():
    config = FRONTEND / "playwright.config.ts"
    spec = FRONTEND / "tests" / "visual" / "agent-studio-smoke.spec.ts"
    package_json = json.loads((FRONTEND / "package.json").read_text(encoding="utf-8"))

    assert config.exists()
    assert spec.exists()
    assert package_json["scripts"]["visual:smoke"] == "playwright test --project=chromium"
    assert "@playwright/test" in package_json["devDependencies"]


def test_playwright_config_is_local_only_and_ignores_generated_outputs():
    text = (FRONTEND / "playwright.config.ts").read_text(encoding="utf-8")
    assert "http://127.0.0.1:5173" in text
    assert "test-results" in text
    assert "playwright-report" in text
    assert "chromium" in text
    assert "npm run dev -- --host 127.0.0.1 --port 5173" in text
    assert "https://" not in text


def test_playwright_smoke_covers_pages_safety_and_forbidden_controls():
    text = (FRONTEND / "tests" / "visual" / "agent-studio-smoke.spec.ts").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "Dashboard",
        "Agent Command Center",
        "Spec Input",
        "Example Gallery",
        "Adapter Matrix",
        "Material Library",
        "Workflow Plan",
        "Artifact Preview",
        "Agent Collaboration",
        "Validation Evidence",
        "System Status",
        "No solver is executed by default.",
        "No external LLM is called by default.",
        "Preview artifacts are not production-grade physical validation.",
        "Formal convergence proof is not claimed.",
        "Upload to PyPI",
        "Upload to TestPyPI",
        "Create tag",
        "Create release",
        "Run solver",
        "External LLM",
        "LOCAL_HOSTS",
        "blockedbyclient",
    ]:
        assert phrase in text
