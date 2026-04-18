# Demo Output

This document shows three representative inputs and their structured spec output, demonstrating `optical-spec-agent`'s parsing, inference, and validation capabilities.

Legend: **[C]** = confirmed, **[~]** = inferred, **---** = missing

---

## Demo 1: Gap Plasmon Sweep (Chinese)

### Input

```
研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和
退相位时间的影响，使用 Meep FDTD，提取共振波长、FWHM 和 T2。
```

### Summary Output

```
Task ID:    demo
Task Name:  [C] 研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和退相位时间的影响，使用 Meep ...
Task Type:  [C] simulation
Goal:       [~] 研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和退相位时间的影响...

Physical System:  [C] nanoparticle_on_film
Mechanism:        [C] scattering
Dimension:        [~] 3d  (inferred: nanoparticle_on_film 通常需要 3D 仿真)
Structure:        [C] sphere_on_film

Solver:           [C] fdtd
Software:         [C] meep
Sweep:            [C] parameter / gap_nm  5.0 → 25.0 nm
Boundary:         [C] PML (all directions)

Observables:      [C] scattering_spectrum, FWHM
Post-process:     [~] resonance_wavelength, fwhm_extraction, T2_extraction,
                       lorentzian_fit (inferred: FWHM/T2 → Lorentzian 拟合)
```

### Key Inferences

| Field | Inferred Value | Reason |
|-------|---------------|--------|
| `physics.model_dimension` | `3d` | nanoparticle_on_film 通常需要 3D 仿真 |
| `geometry_material.material_model` | `Johnson-Christy` | 默认金属光学常数来源 |
| `output.postprocess_target` | +`lorentzian_fit` | FWHM/T2 提取需求推断补充 Lorentzian 拟合 |

### Validation

```
NOT EXECUTABLE — missing: simulation.excitation_source,
                          simulation.source_setting,
                          simulation.monitor_setting
Warnings: suggest adding gap_medium, polarization
```

### Spec JSON (task + physics sections)

```json
{
  "task": {
    "task_id": "demo",
    "task_name": {
      "value": "研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和退相位时间的影响，使用 Meep FDTD，提取共振波长、FWHM 和 T2",
      "status": "confirmed"
    },
    "task_type": { "value": "simulation", "status": "confirmed" },
    "research_goal": {
      "value": "研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和退相位时间的影响...",
      "status": "inferred",
      "note": "从用户描述推断"
    }
  },
  "physics": {
    "physical_system": { "value": "nanoparticle_on_film", "status": "confirmed" },
    "physical_mechanism": { "value": "scattering", "status": "confirmed" },
    "model_dimension": { "value": "3d", "status": "inferred", "note": "nanoparticle_on_film 通常需要 3D 仿真" },
    "structure_type": { "value": "sphere_on_film", "status": "confirmed" }
  }
}
```

---

## Demo 2: Asymmetric Gold Cross (Chinese)

### Input

```
建模非对称金纳米十字结构，两臂长度分别为120nm和80nm，宽40nm，厚30nm，
放在SiO2基底上。用Lumerical FDTD计算偏振相关的散射谱，
x偏振和y偏振都要做，波长范围500-1200nm。
```

### Summary Output

```
Task ID:    demo
Task Type:  [C] simulation

Physical System:  [C] nanoparticle_on_film
Mechanism:        [C] scattering
Dimension:        [~] 3d
Structure:        [C] cross_structure

Geometry:         [C] cross / dimensions: {长度: "120 nm", ...}
Materials:        [C] Au (particle), SiO2 (substrate)
Material Model:   [~] Johnson-Christy

Solver:           [C] fdtd
Software:         [C] lumerical
Sweep:            [C] wavelength / 500 → 1200 nm
Polarization:     [C] linear_x
Boundary:         [C] PML (all directions)

Observables:      [C] scattering_spectrum
```

### Validation

```
NOT EXECUTABLE — missing: simulation.excitation_source,
                          simulation.source_setting,
                          simulation.monitor_setting
```

---

## Demo 3: Ridge Waveguide Mode Analysis (English)

### Input

```
COMSOL FEM mode analysis of a silicon ridge waveguide,
width 500nm, height 220nm, SiO2 BOX, air top cladding.
Calculate effective index and mode profile at 1550nm.
```

### Summary Output

```
Task ID:    demo
Task Type:  [C] simulation

Physical System:  [C] waveguide
Mechanism:        [C] waveguide
Structure:        [C] waveguide

Geometry:         [C] waveguide
Materials:        [C] Si, SiO2, Air

Solver:           [C] fem
Software:         [C] comsol
Polarization:     [C] TE

Observables:      [C] mode_profile
```

### Validation

```
NOT EXECUTABLE — missing: simulation.excitation_source,
                          simulation.source_setting,
                          simulation.boundary_condition,
                          simulation.monitor_setting
```

---

## How to reproduce

```bash
# CLI
optical-spec parse "研究金纳米球-金膜体系中 gap 从 5 到 25 nm..."

# Python
from optical_spec_agent.services.spec_service import SpecService
svc = SpecService()
spec = svc.process("COMSOL FEM mode analysis of a silicon ridge waveguide...")
print(spec.to_flat_dict())
```
