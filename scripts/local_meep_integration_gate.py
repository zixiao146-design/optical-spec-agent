"""Manual/local Meep integration gate.

This script is intentionally not part of the default CI gate. It generates a
core nanoparticle-on-film Meep script, runs it through the optional execution
harness, and writes auditable artifacts under runs/local-gate/<run_id>/.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optical_spec_agent.adapters.meep import MeepAdapter
from optical_spec_agent.execution import check_meep_available, run_meep_script
from optical_spec_agent.services.spec_service import SpecService


CORE_MEEP_CASE = (
    "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
    "平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。"
)


def _make_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"local-gate-{timestamp}-{uuid4().hex[:8]}"


def _normalize_mode(mode: str) -> str:
    normalized = mode.strip().lower().replace("_", "-")
    if normalized in {"smoke", "research-preview"}:
        return normalized
    raise ValueError(f"Unsupported mode: {mode}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a local/manual Meep integration gate.")
    parser.add_argument(
        "--mode",
        choices=["smoke", "research-preview"],
        default="smoke",
        help="Gate mode. research-preview is explicit because it may be slow.",
    )
    parser.add_argument("--timeout", type=int, default=300, help="Execution timeout in seconds.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "runs" / "local-gate",
        help="Root directory for local gate artifacts.",
    )
    args = parser.parse_args(argv)

    mode = _normalize_mode(args.mode)
    run_id = _make_run_id()
    workdir = args.output_root / run_id
    workdir.mkdir(parents=True, exist_ok=True)

    availability = check_meep_available()
    if not availability.available:
        print(json.dumps(availability.to_dict(), indent=2, ensure_ascii=False))
        print("Meep is not available; local integration gate skipped.", file=sys.stderr)
        return 2

    spec = SpecService().process(CORE_MEEP_CASE, task_id=run_id)
    script_mode = "research-preview" if mode == "research-preview" else "smoke"
    expected_mode = "research-preview" if mode == "research-preview" else "smoke"
    script = MeepAdapter().generate(spec, script_mode=script_mode).content
    script_path = workdir / "generated_script.py"
    script_path.write_text(script, encoding="utf-8")

    result = run_meep_script(
        script_path=script_path,
        workdir=workdir,
        timeout=args.timeout,
        expected_mode=expected_mode,
        save_artifacts=True,
        run_id=run_id,
    )
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
