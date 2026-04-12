"""Example 02: Asymmetric gold nano-cross structure with polarization-dependent scattering."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json, spec_to_summary


TEXT = (
    "建模非对称金纳米十字结构，两臂长度分别为120nm和80nm，宽40nm，厚30nm，"
    "放在SiO2基底上。用Lumerical FDTD计算偏振相关的散射谱，"
    "x偏振和y偏振都要做，波长范围500-1200nm。"
)


def main():
    svc = SpecService()
    spec = svc.process(TEXT, task_id="ex-02")

    print(spec_to_summary(spec))

    out = Path(__file__).resolve().parents[1] / "outputs" / "example_02_spec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(spec_to_json(spec), encoding="utf-8")
    print(f"\n→ JSON saved to {out}")


if __name__ == "__main__":
    main()
