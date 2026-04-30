"""Minimal Meep execution harness.

This module intentionally keeps execution optional. It can check whether a
Python environment has Meep importable, run an already-generated script, and
collect the expected v0.4 research-preview output files.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


MEEP_OUTPUT_FILES = (
    "scattering_spectrum.csv",
    "postprocess_results.json",
    "scattering_spectrum.png",
)


@dataclass(slots=True)
class ExecutionResult:
    """Structured result for optional solver execution."""

    success: bool
    available: bool
    command: list[str]
    workdir: str
    returncode: int | None
    stdout: str = ""
    stderr: str = ""
    outputs: dict[str, str] = field(default_factory=dict)
    postprocess_results: dict[str, Any] | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)


def _meep_python_candidates() -> list[list[str]]:
    candidates = [[sys.executable]]
    if shutil.which("micromamba"):
        candidates.append(["micromamba", "run", "-n", "meep", "python"])
    return candidates


def _decode_process_output(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value


def _probe_meep_import(command_prefix: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command_prefix + ["-c", "import meep"],
        capture_output=True,
        text=True,
        timeout=30,
    )


def find_meep_python() -> list[str] | None:
    """Return a Python command prefix with Meep importable, or None."""
    for candidate in _meep_python_candidates():
        try:
            result = _probe_meep_import(candidate)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
        if result.returncode == 0:
            return candidate
    return None


def check_meep_available() -> ExecutionResult:
    """Check whether Meep can be imported without running a simulation."""
    warnings: list[str] = []
    last_command: list[str] = []
    last_returncode: int | None = None
    last_stdout = ""
    last_stderr = ""

    for candidate in _meep_python_candidates():
        command = candidate + ["-c", "import meep"]
        last_command = command
        try:
            result = _probe_meep_import(candidate)
        except subprocess.TimeoutExpired as exc:
            last_returncode = None
            last_stdout = _decode_process_output(exc.stdout)
            last_stderr = _decode_process_output(exc.stderr)
            warnings.append(f"{' '.join(command)} timed out while importing Meep")
            continue
        except FileNotFoundError as exc:
            last_returncode = None
            last_stdout = ""
            last_stderr = str(exc)
            warnings.append(f"{' '.join(command)} failed: {exc}")
            continue

        last_returncode = result.returncode
        last_stdout = result.stdout
        last_stderr = result.stderr
        if result.returncode == 0:
            return ExecutionResult(
                success=True,
                available=True,
                command=command,
                workdir=str(Path.cwd()),
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                warnings=warnings,
            )

        detail = result.stderr.strip() or result.stdout.strip() or f"return code {result.returncode}"
        warnings.append(f"{' '.join(command)} failed: {detail}")

    if not shutil.which("micromamba"):
        warnings.append("micromamba not found; skipped micromamba env probe")

    return ExecutionResult(
        success=False,
        available=False,
        command=last_command,
        workdir=str(Path.cwd()),
        returncode=last_returncode,
        stdout=last_stdout,
        stderr=last_stderr,
        errors=["Meep is not available"],
        warnings=warnings,
    )


def collect_meep_outputs(workdir: Path) -> tuple[dict[str, str], dict[str, Any] | None]:
    """Collect known Meep output files and parsed postprocess JSON, if present."""
    run_dir = Path(workdir)
    outputs: dict[str, str] = {}

    for filename in MEEP_OUTPUT_FILES:
        path = run_dir / filename
        if path.exists():
            outputs[filename] = str(path)

    postprocess_path = run_dir / "postprocess_results.json"
    postprocess_results: dict[str, Any] | None = None
    if postprocess_path.exists():
        parsed = json.loads(postprocess_path.read_text(encoding="utf-8"))
        postprocess_results = parsed if isinstance(parsed, dict) else {"value": parsed}

    return outputs, postprocess_results


def run_meep_script(
    script_path: Path,
    workdir: Path | None = None,
    timeout: int = 300,
) -> ExecutionResult:
    """Run an existing Meep script when Meep is available."""
    script = Path(script_path).expanduser()
    if not script.exists():
        return ExecutionResult(
            success=False,
            available=False,
            command=[],
            workdir=str(Path(workdir).expanduser() if workdir else Path.cwd()),
            returncode=None,
            errors=[f"File not found: {script}"],
            warnings=["Meep availability was not checked because the script file was missing."],
        )

    script = script.resolve()
    run_dir = Path(workdir).expanduser() if workdir else script.parent
    run_dir.mkdir(parents=True, exist_ok=True)

    meep_python = find_meep_python()
    command = (meep_python or []) + [str(script)]
    if meep_python is None:
        return ExecutionResult(
            success=False,
            available=False,
            command=command,
            workdir=str(run_dir),
            returncode=None,
            errors=["Meep is not available"],
        )

    try:
        result = subprocess.run(
            command,
            cwd=str(run_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        outputs, postprocess_results = _safe_collect_outputs(run_dir)
        return ExecutionResult(
            success=False,
            available=True,
            command=command,
            workdir=str(run_dir),
            returncode=None,
            stdout=_decode_process_output(exc.stdout),
            stderr=_decode_process_output(exc.stderr),
            outputs=outputs,
            postprocess_results=postprocess_results,
            errors=[f"Meep script timed out after {timeout} seconds"],
        )
    except FileNotFoundError as exc:
        return ExecutionResult(
            success=False,
            available=False,
            command=command,
            workdir=str(run_dir),
            returncode=None,
            errors=[str(exc)],
        )

    warnings: list[str] = []
    try:
        outputs, postprocess_results = collect_meep_outputs(run_dir)
    except (OSError, json.JSONDecodeError) as exc:
        outputs = {}
        postprocess_results = None
        warnings.append(f"Could not collect Meep outputs: {exc}")

    errors: list[str] = []
    if result.returncode != 0:
        errors.append(f"Meep script failed with return code {result.returncode}")

    return ExecutionResult(
        success=result.returncode == 0,
        available=True,
        command=command,
        workdir=str(run_dir),
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
        outputs=outputs,
        postprocess_results=postprocess_results,
        errors=errors,
        warnings=warnings,
    )


def _safe_collect_outputs(workdir: Path) -> tuple[dict[str, str], dict[str, Any] | None]:
    try:
        return collect_meep_outputs(workdir)
    except (OSError, json.JSONDecodeError):
        return {}, None
