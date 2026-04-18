# Adapter Architecture

> **Status**: Design document. No adapters are implemented yet.
> This defines the interface contract and responsibility boundaries
> for future solver adapters.

---

## 1 Architecture overview

Current v0.1 pipeline:

```
NL text  →  Parser  →  OpticalSpec  →  Validator  →  enriched spec JSON
```

Future pipeline with adapters:

```
NL text  →  Parser  →  OpticalSpec  →  Validator  →  Adapter  →  solver input
                                                                      ↓
                                                                  Solver (run externally)
                                                                      ↓
NL text  ←  Report  ←  Post-process  ←  raw solver output  ←─────────┘
```

**optical-spec-agent stops at "adapter output".** It does not run solvers,
manage compute resources, or produce plots. Those are downstream concerns.

---

## 2 Responsibility boundaries

### spec-agent 负责 (current repo)

| 职责 | 说明 |
|------|------|
| **Parse** | NL text → structured OpticalSpec |
| **Validate** | spec completeness, cross-field consistency |
| **Provenance tracking** | per-field confirmed / inferred / missing |
| **Adapter dispatch** | select adapter by `software_tool` or `solver_method` |
| **Generate solver input** | via adapter, spec → script/config text |

### adapter 负责 (future)

| 职责 | 说明 |
|------|------|
| **can_handle(spec)** | 判断自己能否处理该 spec |
| **generate(spec)** | 将 OpticalSpec 转为工具原生的输入（Python 脚本 / .sif / .pro） |
| **报告 missing_required** | 列出生成过程中必需但 spec 中缺失的字段 |
| **不负责执行** | adapter 不调用 solver，只生成输入 |

### solver 本体负责 (external)

| 职责 | 说明 |
|------|------|
| **执行仿真** | Meep / Elmer / MPB 等，由用户或外部 agent 调度 |
| **资源管理** | MPI 并行、内存、GPU 等 |
| **输出原始结果** | HDF5 / VTK / CSV / numpy arrays |

### postprocess 层负责 (future, outside adapter)

| 职责 | 说明 |
|------|------|
| **读取 solver 输出** | 解析 HDF5 / VTK / CSV |
| **计算衍生量** | Lorentzian 拟合、FWHM 提取、T2 计算 |
| **可视化** | matplotlib / PyVista 图表 |
| **汇总报告** | markdown / PDF 报告生成 |

---

## 3 Adapter interface

All adapters implement `BaseAdapter` from `adapters/base.py`:

```python
class BaseAdapter(ABC):
    tool_name: str                           # e.g. "meep"
    _consumes: list[str]                     # spec paths this adapter reads

    def can_handle(self, spec: OpticalSpec) -> bool: ...
    def generate(self, spec: OpticalSpec) -> AdapterResult: ...
```

`AdapterResult` contains:

| Field | Type | Description |
|-------|------|-------------|
| `tool` | `str` | Tool name |
| `content` | `str` | Generated script/config text |
| `language` | `str` | "python", "scheme", "sif", "pro", etc. |
| `missing_required` | `list[str]` | Fields adapter needed but were missing in spec |

---

## 4 Spec consumption map — which tools read which fields

### 4.1 Meep / MPB (electromagnetic FDTD + eigenmode)

| Spec section | Meep consumes | MPB consumes |
|--------------|---------------|--------------|
| `physics.physical_system` | yes — geometry layout | yes — unit cell type |
| `physics.model_dimension` | yes — 2D/3D | yes — always 3D periodic |
| `physics.physical_mechanism` | yes — hints source type | partial — photonic_crystal |
| `geometry_material.geometry_definition` | yes — objects in cell | yes — lattice + dielectric |
| `geometry_material.material_system` | yes — material functions | yes — dielectric constants |
| `geometry_material.particle_info` | yes — nanoparticle geometry | no |
| `geometry_material.substrate_or_film_info` | yes — film layers | no |
| `simulation.solver_method` | yes — must be fdtd | yes — must be eigenmode |
| `simulation.excitation_source` | yes — source type | no |
| `simulation.source_setting` | yes — wavelength range | no |
| `simulation.boundary_condition` | yes — PML / periodic / Bloch | yes — always periodic |
| `simulation.symmetry_setting` | yes — reduce cell | yes — symmetry exploitation |
| `simulation.mesh_setting` | yes — resolution | yes — grid resolution |
| `simulation.sweep_plan` | yes — parameter sweep | yes — k-point sweep |
| `simulation.monitor_setting` | yes — flux / field | no |
| `output.output_observables` | yes — what to measure | yes — band diagram data |
| `output.postprocess_target` | partial | yes — band_diagram |

**Key difference**: Meep 是时域求解器，消费 source/monitor；MPB 是频域特征模求解器，不关心 source，主要消费 lattice 和 dielectric 定义。

### 4.2 RayOptics / Optiland (imaging optics)

| Spec section | RayOptics | Optiland |
|--------------|-----------|----------|
| `physics.physical_system` | no | partial — imaging system |
| `geometry_material.geometry_definition` | yes — lens surfaces | yes — surface definitions |
| `geometry_material.material_system` | yes — glass catalog | yes — lens materials |
| `simulation.solver_method` | no (always ray trace) | no (always ray trace) |
| `simulation.excitation_source` | yes — field angle | yes — field points |
| `simulation.source_setting` | yes — wavelengths | yes — wavelengths |
| `output.output_observables` | yes — ray data | yes — spot diagram, MTF |
| `output.postprocess_target` | no | yes — optimization targets |

**Key difference**: RayOptics 侧重读取已有设计文件 (.seq/.zmx)，Optiland 侧重从零定义并优化。

**Note**: 当前 OpticalSpec 的 geometry/material 模型偏 nanoparticle 方向。imaging optics adapter 接入时，可能需要扩展 `geometry_definition` 以支持 lens surface 序列定义。这是 v0.6 需要解决的设计问题，不在当前范围。

### 4.3 Gmsh / GetDP / Elmer (FEM chain)

| Spec section | Gmsh | GetDP | Elmer |
|--------------|------|-------|-------|
| `physics.model_dimension` | yes — 2D/3D mesh | yes — equation dim | yes — solver dim |
| `geometry_material.geometry_definition` | yes — geometry to mesh | partial — .geo reference | no — reads mesh |
| `geometry_material.material_system` | partial — physical groups | yes — material props | yes — material props |
| `simulation.solver_method` | no | yes — must be fem | yes — must be fem |
| `simulation.boundary_condition` | partial — boundary tags | yes — BC in .pro | yes — BC in .sif |
| `simulation.mesh_setting` | yes — mesh params | no — receives mesh | no — receives mesh |
| `simulation.excitation_source` | no | yes — source BC | yes — source BC |
| `output.output_observables` | no | yes — what to compute | yes — what to compute |

**Typical chain**: `Gmsh` generates mesh → `Elmer` solves on that mesh.
`GetDP` is an alternative to Elmer for custom PDE formulations.
Adapter 可以拆分为 `GmshAdapter` (geometry → mesh) + `ElmerAdapter` (spec + mesh → .sif)。

### 4.4 Raypier (non-sequential ray tracing / illumination)

| Spec section | Raypier consumes |
|--------------|-----------------|
| `physics.physical_system` | partial — illumination system |
| `geometry_material.geometry_definition` | yes — optical elements |
| `geometry_material.material_system` | yes — spectral materials |
| `simulation.excitation_source` | yes — light source type |
| `simulation.source_setting` | yes — spectral distribution |
| `output.output_observables` | yes — irradiance map, spectrum |

**Status**: Raypier 是候选工具，adapter 优先级较低。

### 4.5 FreeCAD (parametric CAD)

| Spec section | FreeCAD consumes |
|--------------|-----------------|
| `geometry_material.geometry_definition` | yes — parametric model |
| `geometry_material.material_system` | partial — for reference |

**Role**: FreeCAD 不是求解器，而是几何定义的替代前端。当 Gmsh 的 `.geo` 脚本
无法描述复杂机械结构时，通过 FreeCAD Python API 建模，导出 STEP/BREP 给 Gmsh。

---

## 5 Planned adapter directory layout

```
src/optical_spec_agent/adapters/
├── __init__.py          # Package marker + docstring
├── base.py              # BaseAdapter ABC + AdapterResult model
│
│   # v0.3 (planned)
│   # meep.py            # MeepAdapter: spec → Meep Python script
│
│   # v0.4 (planned)
│   # mpb.py             # MPBAdapter: spec → MPB Python/script
│
│   # v0.5 (planned)
│   # elmer.py           # ElmerAdapter: spec + mesh → .sif
│   # gmsh.py            # GmshAdapter: spec → .geo → mesh
│
│   # v0.6 (planned)
│   # optiland.py        # OptilandAdapter: spec → Optic object
│   # rayoptics.py       # RayOpticsAdapter: spec → OpticalModel
│
│   # Future candidates
│   # raypier.py
│   # freecad.py
│   # getdp.py
```

No files beyond `__init__.py` and `base.py` exist today. The commented lines
above show where each adapter will live when implemented.

---

## 6 Dispatch logic (future)

When adapters exist, dispatch can follow this pattern:

```python
# Future pseudocode — not implemented

ADAPTERS: dict[str, type[BaseAdapter]] = {
    "meep": MeepAdapter,
    "mpb": MPBAdapter,
    "elmer": ElmerAdapter,
    "optiland": OptilandAdapter,
    # ...
}

def dispatch(spec: OpticalSpec) -> BaseAdapter:
    tool = spec.simulation.software_tool.value
    adapter_cls = ADAPTERS.get(tool)
    if adapter_cls and adapter_cls().can_handle(spec):
        return adapter_cls()
    raise ValueError(f"No adapter for tool={tool}")
```

This is a flat registry — no plugin discovery, no entry-point magic.
KISS until there are more than 5 adapters.

---

## 7 Spec extension points for v0.6+

Current OpticalSpec is optimized for electromagnetic simulation (FDTD/FEM).
Imaging optics adapters (Optiland, RayOptics) will need additional structured
fields. Candidate extensions (not implemented, for planning only):

| Need | Current status | Possible approach |
|------|---------------|-------------------|
| Lens surface sequence | Not modeled | Add `ImagingSystemSection` or extend `geometry_definition` |
| Glass catalog reference | Not modeled | Extend `material_system` with catalog field |
| Optimization targets | Not modeled | Extend `output.postprocess_target` with merit function |
| Field points / angles | Partial in `source_setting` | Dedicated sub-model |

Design decisions here should wait until v0.6 when Optiland adapter work begins.
