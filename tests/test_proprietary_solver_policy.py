"""Guard against making proprietary solvers default dependencies."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMERCIAL_NAMES = ("Zemax", "Lumerical", "COMSOL", "proprietary Ansys")
PROPRIETARY_TOOL_NAMES = {"zemax", "lumerical", "comsol", "ansys"}


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_default_quickstart_does_not_require_proprietary_tools():
    readme = _read("README.md")
    readme_zh = _read("README.zh-CN.md")
    combined = f"{readme}\n{readme_zh}"
    assert "Default quickstart and release validation do not require Zemax" in readme
    assert "默认 quickstart 不要求 Zemax" in readme_zh
    for dangerous in [
        "install Zemax",
        "install Lumerical",
        "install COMSOL",
        "requires Zemax",
        "requires Lumerical",
        "requires COMSOL",
        "需要 Zemax",
        "需要 Lumerical",
        "需要 COMSOL",
    ]:
        assert dangerous not in combined


def test_smoke_release_has_no_proprietary_command_dependency():
    text = _read("scripts/smoke_release.sh").lower()
    for name in ["zemax", "lumerical", "comsol", "ansys"]:
        assert name not in text


def test_tests_do_not_require_proprietary_tools_by_default():
    for path in (ROOT / "tests").glob("test_*.py"):
        if path.name == "test_proprietary_solver_policy.py":
            continue
        text = path.read_text(encoding="utf-8").lower()
        for phrase in [
            "subprocess.run([\"zemax\"",
            "subprocess.run([\"lumerical\"",
            "subprocess.run([\"comsol\"",
            "subprocess.run([\"ansys\"",
            "pytest.importorskip(\"zemax\"",
            "pytest.importorskip(\"lumerical\"",
            "pytest.importorskip(\"comsol\"",
            "pytest.importorskip(\"ansys\"",
        ]:
            assert phrase not in text, f"{path} contains default proprietary dependency: {phrase}"


def test_adapter_list_does_not_register_proprietary_default_adapters():
    result = subprocess.run(
        ["optical-spec", "adapter-list", "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    tools = {item["tool_name"].lower() for item in json.loads(result.stdout)["adapters"]}
    assert tools.isdisjoint(PROPRIETARY_TOOL_NAMES)


def test_commercial_names_only_have_policy_or_non_default_context_in_key_docs():
    docs = [
        "README.md",
        "README.zh-CN.md",
        "docs/adapter_support_matrix.md",
        "docs/external_solver_policy.md",
        "docs/open_source_solver_strategy.md",
        "docs/proprietary_solver_policy.md",
    ]
    combined = "\n".join(_read(path) for path in docs)
    normalized = " ".join(combined.split())
    for name in COMMERCIAL_NAMES:
        assert name in combined
    required_contexts = [
        "not default dependencies",
        "not default",
        "export-only",
        "not required for tests",
        "not required for smoke validation",
        "not required for release validation",
    ]
    for context in required_contexts:
        assert context in normalized
