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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


MEEP_OUTPUT_FILES = (
    "scattering_spectrum.csv",
    "postprocess_results.json",
    "scattering_spectrum.png",
)
RESEARCH_PREVIEW_REQUIRED_OUTPUTS = [
    "scattering_spectrum.csv",
    "postprocess_results.json",
]
EXECUTION_RESULT_SCHEMA_VERSION = "execution_result.v0.1"


@dataclass(slots=True)
class PostprocessResult:
    """Typed view over research-preview postprocess_results.json."""

    mode: str | None = None
    resonance_wavelength_nm: float | None = None
    fwhm_nm: float | None = None
    gap_thickness_nm: float | None = None
    wavelength_min_nm: float | None = None
    wavelength_max_nm: float | None = None
    defaults_applied: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable typed postprocess result."""
        return asdict(self)


@dataclass(slots=True)
class ExecutionResult:
    """Structured result for optional solver execution."""

    success: bool
    available: bool
    command: list[str]
    workdir: str
    returncode: int | None
    schema_version: str = EXECUTION_RESULT_SCHEMA_VERSION
    run_id: str = ""
    created_at: str = ""
    script_path: str = ""
    stdout: str = ""
    stderr: str = ""
    outputs: dict[str, str] = field(default_factory=dict)
    postprocess_results: dict[str, Any] | None = None
    typed_postprocess_results: dict[str, Any] | None = None
    expected_mode: str = "auto"
    required_outputs: list[str] = field(default_factory=list)
    missing_outputs: list[str] = field(default_factory=list)
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


def _normalize_expected_mode(expected_mode: str) -> str | None:
    normalized = expected_mode.strip().lower().replace("-", "_")
    if normalized in {"auto", "smoke", "preview", "research_preview"}:
        return normalized
    return None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _make_run_id(prefix: str = "meep") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{timestamp}-{uuid4().hex[:8]}"


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
    run_id = _make_run_id(prefix="meep-check")
    created_at = _utc_now_iso()
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
                run_id=run_id,
                created_at=created_at,
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
        run_id=run_id,
        created_at=created_at,
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


def parse_postprocess_results(workdir: Path) -> Any:
    """Parse raw postprocess_results.json without compatibility wrapping."""
    postprocess_path = Path(workdir) / "postprocess_results.json"
    return json.loads(postprocess_path.read_text(encoding="utf-8"))


def parse_typed_postprocess_results(raw: dict[str, Any]) -> PostprocessResult:
    """Build a typed view over a raw postprocess result dict."""
    return PostprocessResult(
        mode=_optional_str(raw.get("mode")),
        resonance_wavelength_nm=_optional_float(raw.get("resonance_wavelength_nm")),
        fwhm_nm=_optional_float(raw.get("fwhm_nm")),
        gap_thickness_nm=_optional_float(raw.get("gap_thickness_nm")),
        wavelength_min_nm=_optional_float(raw.get("wavelength_min_nm")),
        wavelength_max_nm=_optional_float(raw.get("wavelength_max_nm")),
        defaults_applied=_string_list(raw.get("defaults_applied")),
        limitations=_string_list(raw.get("limitations")),
        raw=raw,
    )


def run_meep_script(
    script_path: Path,
    workdir: Path | None = None,
    timeout: int = 300,
    expected_mode: str = "auto",
    save_artifacts: bool = True,
    run_id: str | None = None,
) -> ExecutionResult:
    """Run an existing Meep script when Meep is available."""
    resolved_run_id = run_id or _make_run_id()
    created_at = _utc_now_iso()
    normalized_mode = _normalize_expected_mode(expected_mode)
    if normalized_mode is None:
        failure = ExecutionResult(
            success=False,
            available=False,
            command=[],
            workdir=str(Path(workdir).expanduser() if workdir else Path.cwd()),
            returncode=None,
            run_id=resolved_run_id,
            created_at=created_at,
            script_path=str(Path(script_path).expanduser()),
            expected_mode=expected_mode,
            errors=[f"Unsupported expected_mode: {expected_mode}"],
        )
        _write_early_failure_artifacts(failure, workdir=workdir, save_artifacts=save_artifacts)
        return failure

    required_outputs = _required_outputs_for_mode(normalized_mode)
    script = Path(script_path).expanduser()
    if not script.exists():
        failure = ExecutionResult(
            success=False,
            available=False,
            command=[],
            workdir=str(Path(workdir).expanduser() if workdir else Path.cwd()),
            returncode=None,
            run_id=resolved_run_id,
            created_at=created_at,
            script_path=str(script),
            expected_mode=normalized_mode,
            required_outputs=required_outputs,
            missing_outputs=required_outputs.copy(),
            errors=[f"File not found: {script}"],
            warnings=["Meep availability was not checked because the script file was missing."],
        )
        _write_early_failure_artifacts(failure, workdir=workdir, save_artifacts=save_artifacts)
        return failure

    script = script.resolve()
    run_dir = Path(workdir).expanduser() if workdir else script.parent
    run_dir.mkdir(parents=True, exist_ok=True)
    script_path_str = str(script)

    meep_python = find_meep_python()
    command = (meep_python or []) + [str(script)]
    if meep_python is None:
        failure = ExecutionResult(
            success=False,
            available=False,
            command=command,
            workdir=str(run_dir),
            returncode=None,
            run_id=resolved_run_id,
            created_at=created_at,
            script_path=script_path_str,
            expected_mode=normalized_mode,
            required_outputs=required_outputs,
            missing_outputs=required_outputs.copy(),
            errors=["Meep is not available"],
        )
        _write_execution_artifacts(failure, save_artifacts=save_artifacts)
        return failure

    try:
        result = subprocess.run(
            command,
            cwd=str(run_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        outputs, postprocess_results, collect_errors = _safe_collect_outputs(run_dir)
        missing_outputs = _missing_required_outputs(outputs, required_outputs)
        timeout_result = ExecutionResult(
            success=False,
            available=True,
            command=command,
            workdir=str(run_dir),
            returncode=None,
            run_id=resolved_run_id,
            created_at=created_at,
            script_path=script_path_str,
            stdout=_decode_process_output(exc.stdout),
            stderr=_decode_process_output(exc.stderr),
            outputs=outputs,
            postprocess_results=postprocess_results,
            typed_postprocess_results=_typed_postprocess_dict(postprocess_results),
            expected_mode=normalized_mode,
            required_outputs=required_outputs,
            missing_outputs=missing_outputs,
            errors=[f"Meep script timed out after {timeout} seconds", *collect_errors],
        )
        _write_execution_artifacts(timeout_result, save_artifacts=save_artifacts)
        return timeout_result
    except FileNotFoundError as exc:
        return ExecutionResult(
            success=False,
            available=False,
            command=command,
            workdir=str(run_dir),
            returncode=None,
            run_id=resolved_run_id,
            created_at=created_at,
            script_path=script_path_str,
            expected_mode=normalized_mode,
            required_outputs=required_outputs,
            missing_outputs=required_outputs.copy(),
            errors=[str(exc)],
        )

    warnings: list[str] = []
    errors: list[str] = []
    typed_postprocess_results: dict[str, Any] | None = None
    try:
        outputs, postprocess_results = collect_meep_outputs(run_dir)
    except (OSError, json.JSONDecodeError) as exc:
        outputs = {}
        postprocess_results = None
        errors.append(f"Could not parse Meep outputs: {exc}")

    if result.returncode != 0:
        errors.append(f"Meep script failed with return code {result.returncode}")

    missing_outputs = _missing_required_outputs(outputs, required_outputs)
    for output_name in missing_outputs:
        errors.append(f"Missing required output for {normalized_mode}: {output_name}")
    if normalized_mode == "research_preview" and "postprocess_results.json" in outputs:
        try:
            raw_postprocess_results = parse_postprocess_results(run_dir)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Could not parse postprocess_results.json: {exc}")
            postprocess_results = None
        else:
            if not isinstance(raw_postprocess_results, dict):
                errors.append("postprocess_results.json must be a JSON object")
                postprocess_results = None
            else:
                postprocess_results = raw_postprocess_results
                typed_postprocess_results = parse_typed_postprocess_results(raw_postprocess_results).to_dict()
    elif isinstance(postprocess_results, dict):
        typed_postprocess_results = parse_typed_postprocess_results(postprocess_results).to_dict()

    execution_result = ExecutionResult(
        success=result.returncode == 0 and not errors,
        available=True,
        command=command,
        workdir=str(run_dir),
        returncode=result.returncode,
        run_id=resolved_run_id,
        created_at=created_at,
        script_path=script_path_str,
        stdout=result.stdout,
        stderr=result.stderr,
        outputs=outputs,
        postprocess_results=postprocess_results,
        typed_postprocess_results=typed_postprocess_results,
        expected_mode=normalized_mode,
        required_outputs=required_outputs,
        missing_outputs=missing_outputs,
        errors=errors,
        warnings=warnings,
    )
    _write_execution_artifacts(execution_result, save_artifacts=save_artifacts)
    return execution_result


def _required_outputs_for_mode(expected_mode: str) -> list[str]:
    if expected_mode == "research_preview":
        return RESEARCH_PREVIEW_REQUIRED_OUTPUTS.copy()
    return []


def _missing_required_outputs(outputs: dict[str, str], required_outputs: list[str]) -> list[str]:
    return [name for name in required_outputs if name not in outputs]


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _typed_postprocess_dict(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if raw is None:
        return None
    return parse_typed_postprocess_results(raw).to_dict()


def _safe_collect_outputs(workdir: Path) -> tuple[dict[str, str], dict[str, Any] | None, list[str]]:
    try:
        outputs, postprocess_results = collect_meep_outputs(workdir)
        return outputs, postprocess_results, []
    except (OSError, json.JSONDecodeError) as exc:
        return {}, None, [f"Could not parse Meep outputs: {exc}"]


def _run_manifest(result: ExecutionResult) -> dict[str, Any]:
    return {
        "schema_version": result.schema_version,
        "run_id": result.run_id,
        "created_at": result.created_at,
        "script_path": result.script_path,
        "workdir": result.workdir,
        "expected_mode": result.expected_mode,
        "command": result.command,
        "success": result.success,
        "available": result.available,
        "returncode": result.returncode,
        "outputs": result.outputs,
        "required_outputs": result.required_outputs,
        "missing_outputs": result.missing_outputs,
    }


def _write_execution_artifacts(result: ExecutionResult, *, save_artifacts: bool) -> None:
    if not save_artifacts:
        return

    run_dir = Path(result.workdir)
    try:
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "stdout.txt").write_text(result.stdout, encoding="utf-8")
        (run_dir / "stderr.txt").write_text(result.stderr, encoding="utf-8")
        (run_dir / "execution_result.json").write_text(
            json.dumps(result.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (run_dir / "run_manifest.json").write_text(
            json.dumps(_run_manifest(result), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as exc:
        result.warnings.append(f"Could not write execution artifacts: {exc}")


def _write_early_failure_artifacts(
    result: ExecutionResult,
    *,
    workdir: Path | None,
    save_artifacts: bool,
) -> None:
    if workdir is None:
        return
    result.workdir = str(Path(workdir).expanduser())
    _write_execution_artifacts(result, save_artifacts=save_artifacts)
