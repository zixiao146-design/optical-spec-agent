"""Example 03: Lumerical FDTD Mie scattering of a silicon nanosphere."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json, spec_to_summary


TEXT = (
    "Lumerical FDTD仿真硅纳米球的Mie散射，直径150nm，"
    "环境折射率1.5，用TFSF光源，扫波长300-800nm，"
    "计算散射截面、吸收截面和消光截面，提取散射谱主峰位置。"
)


def main():
    svc = SpecService()
    spec = svc.process(TEXT, task_id="ex-03")

    print(spec_to_summary(spec))

    out = Path(__file__).resolve().parents[1] / "outputs" / "example_03_spec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(spec_to_json(spec), encoding="utf-8")
    print(f"\n→ JSON saved to {out}")


if __name__ == "__main__":
    main()
