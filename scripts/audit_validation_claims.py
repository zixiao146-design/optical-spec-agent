#!/usr/bin/env python3
"""Audit repo text for validation overclaim language.

The audit is local-only and conservative. It flags risky validation phrases
unless the surrounding line clearly states that the claim is not made.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATHS = [
    ROOT / "docs",
    ROOT / "src",
    ROOT / "tests",
    ROOT / "examples",
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
]
SKIP_PARTS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "frontend/dist",
    "frontend/build",
    "frontend/test-results",
    "frontend/playwright-report",
}
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".json",
    ".txt",
    ".toml",
    ".yml",
    ".yaml",
    ".sh",
}
RISKY_PHRASES = [
    "production-grade physical validation",
    "formal convergence proof",
    "production-grade optical constants",
    "real solver result",
    "solver monitor result",
    "physically validated",
    "guaranteed accuracy",
]
SAFE_NEGATIONS = [
    "no ",
    "not ",
    "not a ",
    "not an ",
    "not claimed",
    "not prove",
    "not imply",
    "must not",
    "should not",
    "does not claim",
    "does not prove",
    "do not claim",
    "is not claimed",
    "are not claimed",
    "without claiming",
    "without",
    "absence",
    "non-goal",
    "non goal",
    "out of",
    "overread",
    "blocked",
    "unsupported",
    "non_goals",
    "frozen_non_goals",
    "claiming",
    "claim",
    "claimed",
    "claims",
    "false",
    "deferred",
    "preview",
    "still preview",
    "not frozen",
    "supported: no",
    "不",
]


@dataclass(frozen=True)
class Finding:
    path: Path
    line_number: int
    phrase: str
    line: str


def _iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file():
                continue
            rel = candidate.relative_to(ROOT) if candidate.is_relative_to(ROOT) else candidate
            if any(part in SKIP_PARTS for part in rel.parts):
                continue
            if candidate.suffix in TEXT_SUFFIXES:
                files.append(candidate)
    return sorted(set(files))


def _line_is_safe(line: str, phrase: str, context: str = "") -> bool:
    stripped = line.lstrip()
    if stripped.startswith("#") or stripped.startswith("|"):
        return True
    if (
        "assert " in line
        or "required =" in line
        or " in text" in line
        or stripped.startswith(("\"", "'"))
    ):
        return True
    lowered = (context or line).lower()
    index = lowered.find(phrase)
    if index < 0:
        return True
    if any(marker in lowered for marker in SAFE_NEGATIONS):
        return True
    window = lowered[max(0, index - 160) : index + len(phrase) + 160]
    if any(marker in window for marker in SAFE_NEGATIONS):
        return True
    if phrase in {"real solver result", "solver monitor result"} and "requires" in window:
        return True
    return False


def audit_paths(paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_files(paths):
        if "production_grade_validation_request" in path.parts:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            context = "\n".join(
                lines[max(0, line_number - 12) : min(len(lines), line_number + 8)]
            )
            lowered = line.lower()
            for phrase in RISKY_PHRASES:
                if phrase in lowered and not _line_is_safe(line, phrase, context):
                    findings.append(
                        Finding(
                            path=path,
                            line_number=line_number,
                            phrase=phrase,
                            line=line.strip(),
                        )
                    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional files or directories to audit. Defaults to repo docs/src/tests/examples/README.",
    )
    args = parser.parse_args()
    paths = [path if path.is_absolute() else ROOT / path for path in args.paths]
    findings = audit_paths(paths or DEFAULT_PATHS)
    if findings:
        print("VALIDATION CLAIM AUDIT FAILED")
        for finding in findings:
            try:
                display = finding.path.relative_to(ROOT)
            except ValueError:
                display = finding.path
            print(
                f"{display}:{finding.line_number}: unsafe '{finding.phrase}' claim: "
                f"{finding.line}"
            )
        return 1
    print("VALIDATION CLAIM AUDIT PASSED")
    print("NO SOLVER EXECUTION PERFORMED")
    print("NO EXTERNAL LLM CALLED")
    print("NO UPLOAD PERFORMED")
    print("NO TAG CREATED")
    print("NO RELEASE CREATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
