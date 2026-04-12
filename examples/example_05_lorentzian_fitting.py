"""Example 05: Lorentzian fitting — extract FWHM and T2 from scattering spectrum."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json, spec_to_summary


TEXT = (
    "对实验测得的散射谱进行Lorentzian拟合，数据范围500-900nm，"
    "主峰位于680nm附近，提取FWHM和T2退相干时间。"
    "用Python scipy做曲线拟合。"
)


def main():
    svc = SpecService()
    spec = svc.process(TEXT, task_id="ex-05")

    print(spec_to_summary(spec))

    out = Path(__file__).resolve().parents[1] / "outputs" / "example_05_spec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(spec_to_json(spec), encoding="utf-8")
    print(f"\n→ JSON saved to {out}")


if __name__ == "__main__":
    main()
