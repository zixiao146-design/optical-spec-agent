"""Example 06: Generate a Meep script from a parsed spec.

Usage:
    cd optical-spec-agent
    python examples/example_06_meep_nanoparticle.py
"""

from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.adapters.meep import MeepAdapter
from pathlib import Path

TEXT = (
    "用Meep FDTD仿真金纳米球-金膜gap plasmon体系，直径80nm金球放在金膜上，"
    "间隙填充SiO2（5nm），平面波正入射，扫gap从5到25nm，"
    "计算散射谱，提取共振波长、FWHM和T2。"
)

svc = SpecService()
spec = svc.process(TEXT, task_id="example-06")

adapter = MeepAdapter()
if adapter.can_handle(spec):
    result = adapter.generate(spec)
    out = Path("examples/outputs/meep_nanoparticle_on_film.py")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result.content, encoding="utf-8")
    print(f"Generated: {out}")
    print(f"Script length: {len(result.content)} chars")
else:
    print("Adapter cannot handle this spec")
    print(f"  physical_system: {spec.physics.physical_system.value}")
    print(f"  solver_method: {spec.simulation.solver_method.value}")
    print(f"  software_tool: {spec.simulation.software_tool.value}")
