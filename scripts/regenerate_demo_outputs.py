#!/usr/bin/env python3
"""Regenerate deterministic demo artifacts without external solvers or APIs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optical_spec_agent.analysis.physical_diagnostics import (  # noqa: E402
    generate_physical_diagnostics,
    prepare_diagnostic_spec,
)
from optical_spec_agent.services.spec_service import SpecService  # noqa: E402


EXAMPLES = {
    "gap_plasmon_rule": "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon，输出散射谱和 FWHM。",
    "waveguide_mode_rule": "用 Elmer 做 Si3N4 波导 FEM 模式分析，输出有效折射率和模场。",
    "mpb_hybrid_mock": "用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。",
}


def _run(command: list[str]) -> None:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"{' '.join(command)} failed:\n{completed.stdout}\n{completed.stderr}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "examples" / "outputs" / "release_demo",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    svc = SpecService()
    generated: dict[str, str] = {}
    for name, text in EXAMPLES.items():
        spec = svc.process(text, task_id=name)
        path = args.output_dir / f"{name}.json"
        path.write_text(json.dumps(spec.model_dump(mode="json"), indent=2, ensure_ascii=False))
        generated[name] = str(path)

    mpb_output = args.output_dir / "mpb_band.py"
    _run(
        [
            sys.executable,
            "-m",
            "optical_spec_agent",
            "adapter-generate",
            generated["mpb_hybrid_mock"],
            "--tool",
            "mpb",
            "--output",
            str(mpb_output),
        ]
    )
    generated["mpb_band.py"] = str(mpb_output)

    diagnostic_spec, _ = prepare_diagnostic_spec(
        args.output_dir / "diagnostic_spec.json",
        create_demo_spec_if_missing=True,
    )
    diagnostics = generate_physical_diagnostics(
        spec_path=diagnostic_spec,
        output_dir=args.output_dir / "diagnostics",
        artifact_dir=args.output_dir / "missing_run_artifacts",
    )
    generated.update(diagnostics.generated_outputs)

    manifest = args.output_dir / "demo_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "demo_artifacts.v0.1",
                "generated_outputs": generated,
                "notes": [
                    "Deterministic demo artifacts only.",
                    "No external solver or external LLM provider was run.",
                    "Diagnostics are post-hoc checks, not production physical validation.",
                ],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Regenerated demo artifacts in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
