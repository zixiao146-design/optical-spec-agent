from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_frontend_mvp_script_exists_and_is_safe():
    path = ROOT / "scripts" / "smoke_frontend_mvp.sh"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "npm run typecheck",
        "npm run build",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO PROPRIETARY SOLVER REQUIRED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
        "rm -rf node_modules dist build",
    ]:
        assert phrase in text
    lowered = text.lower()
    for phrase in ["twine upload", "gh release create", "git tag", "git push"]:
        assert phrase not in lowered


def test_smoke_frontend_mvp_script_runs_when_npm_is_available():
    if shutil.which("npm") is None:
        return
    result = subprocess.run(
        ["./scripts/smoke_frontend_mvp.sh"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "npm run typecheck: passed" in result.stdout
    assert "npm run build: passed" in result.stdout
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert not (ROOT / "frontend" / "node_modules").exists()
    assert not (ROOT / "frontend" / "dist").exists()
    assert not (ROOT / "frontend" / "build").exists()
