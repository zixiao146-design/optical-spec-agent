"""Example 04: COMSOL mode analysis of a Si3N4 ridge waveguide."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json, spec_to_summary


TEXT = (
    "COMSOL模式分析：Si3N4脊波导（宽800nm，高400nm，蚀刻深度250nm），"
    "SiO2下包层，上包层为空气，计算1.55μm波长下的基模有效折射率和模场分布，"
    "TE和TM模式都要计算。"
)


def main():
    svc = SpecService()
    spec = svc.process(TEXT, task_id="ex-04")

    print(spec_to_summary(spec))

    out = Path(__file__).resolve().parents[1] / "outputs" / "example_04_spec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(spec_to_json(spec), encoding="utf-8")
    print(f"\n→ JSON saved to {out}")


if __name__ == "__main__":
    main()
