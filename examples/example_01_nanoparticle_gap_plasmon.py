"""Example 01: Nanoparticle-on-film gap plasmon — sweep gap thickness."""

import json
import sys
from pathlib import Path

# Ensure src is importable when running from the examples/ directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json, spec_to_summary


TEXT = (
    "用FDTD仿真一个gap plasmon体系：80nm金纳米立方体放在金膜上，"
    "间隙填充SiO2（5 nm），用总场散射场(TFSF)光源正入射，"
    "扫间隙厚度从2nm到20nm，步长2nm，计算散射截面和吸收截面。"
    "波长范围400-900nm。"
)


def main():
    svc = SpecService()
    spec = svc.process(TEXT, task_id="ex-01")

    print(spec_to_summary(spec))

    out = Path(__file__).resolve().parents[1] / "outputs" / "example_01_spec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(spec_to_json(spec), encoding="utf-8")
    print(f"\n→ JSON saved to {out}")


if __name__ == "__main__":
    main()
