# optical-spec-agent

[![Tests](https://github.com/zixiao146-design/optical-spec-agent/actions/workflows/test.yml/badge.svg)](https://github.com/zixiao146-design/optical-spec-agent/actions/workflows/test.yml)

> Convert optical simulation requests into validated, solver-ready spec JSON.

**optical-spec-agent** is a compilation layer between human language and optical solvers. You describe a simulation task in plain text (Chinese or English), and it produces a single structured, validated JSON spec — with typed fields, provenance tracking, and completeness checks — ready for downstream solver agents.

```
"用Meep FDTD仿真金纳米球-金膜gap plasmon，扫gap从5到25nm，提取共振波长和FWHM"
                                    ↓
                        OpticalSpec (JSON)
                     ┌─────────────────────┐
                     │ task, physics,       │
                     │ geometry_material,   │
                     │ simulation, output   │
                     │ + validation status  │
                     └─────────────────────┘
```

It is **not** a solver. It does not run Meep, Lumerical, or COMSOL — it produces the spec that a solver agent would consume.

## Why this project?

Optical simulation tasks are inherently multi-parameter: geometry, materials, solver settings, sweep plans, post-processing targets. Humans describe these imprecisely; solvers require exact, structured input. This gap makes automation and multi-agent pipelines fragile.

`optical-spec-agent` is the **missing compiler**:
- **Input**: messy natural language
- **Output**: typed, validated spec JSON with per-field provenance (confirmed / inferred / missing)
- **Contract**: every field carries its status and derivation note, so downstream agents know what to trust and what to verify

## Current scope (v0.1)

The v0.1 closed loop:

```
Natural language  →  Rule-based parser  →  Structured spec JSON  →  Validation
```

**What works:**
- Keyword + regex parsing of Chinese and English optical task descriptions
- Structured sub-models for geometry, materials, sweep plans, source settings, boundary conditions
- Post-hoc inference (gap plasmon → FDTD, FWHM/T2 → Lorentzian fit, nanoparticle_on_film → 3D)
- Per-field provenance tracking: confirmed / inferred / missing
- Pydantic v2 validation with task-type-aware rules
- CLI, FastAPI, and Python SDK interfaces

**What does NOT work yet:**
- Real LLM integration (only a placeholder parser exists)
- Solver execution — no Meep, Lumerical, or COMSOL adapters
- Parameter file generation (`.ctl`, `.lsf`, `.mph`)
- Visualization or plotting pipeline

## Install

```bash
cd optical-spec-agent
pip install -e ".[dev]"
```

Requires Python 3.11+.

## Quick start

### CLI

```bash
# Parse a task description
optical-spec parse "研究金纳米球-金膜体系中gap从5到25nm变化对散射谱主峰线宽和退相位时间的影响，使用Meep FDTD，提取共振波长、FWHM和T2。"

# Save output to file
optical-spec parse "..." -o outputs/my_spec.json

# Run built-in examples
optical-spec example all
optical-spec example 01

# Validate a saved spec
optical-spec validate outputs/my_spec.json

# Export JSON Schema
optical-spec schema -o schema.json

# Or use python -m
python -m optical_spec_agent parse "..."
```

### Python SDK

```python
from optical_spec_agent.services.spec_service import SpecService

svc = SpecService()
spec = svc.process(
    "用FDTD仿真金纳米球Mie散射，直径100nm，波长400-800nm",
    task_id="demo-001",
)

print(spec.confirmed_fields)    # {"task.task_type": "simulation", ...}
print(spec.inferred_fields)     # {"task.research_goal": {...}, ...}
print(spec.missing_fields)      # ["simulation.polarization", ...]
print(spec.validation_status)   # ValidationStatus(is_executable=False, ...)
```

### API

```bash
uvicorn optical_spec_agent.api.app:app --reload --port 8000
```

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/parse` | Parse natural language → spec |
| `POST` | `/validate` | Validate a spec |
| `GET` | `/schema` | Export JSON Schema |

Interactive docs at `http://localhost:8000/docs`.

## Example input & output

**Input:**
```
研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和
退相位时间的影响，使用 Meep FDTD，提取共振波长、FWHM 和 T2。
```

**Extracted spec (key fields):**

| Field | Value | Status |
|-------|-------|--------|
| `task.task_type` | `simulation` | confirmed |
| `physics.physical_system` | `nanoparticle_on_film` | confirmed |
| `physics.structure_type` | `sphere_on_film` | confirmed |
| `simulation.solver_method` | `fdtd` | confirmed |
| `simulation.software_tool` | `meep` | confirmed |
| `simulation.sweep_plan.variable` | `gap_nm` (5→25) | confirmed |
| `output.output_observables` | `scattering_spectrum, FWHM` | confirmed |
| `output.postprocess_target` | `resonance_wavelength, fwhm_extraction, T2_extraction, lorentzian_fit` | confirmed + inferred |
| `physics.model_dimension` | `3d` | inferred |
| `geometry_material.material_model` | `Johnson-Christy` | inferred |

**Inferences logged:**
- `nanoparticle_on_film 通常需要 3D 仿真`
- `默认金属光学常数来源`
- `FWHM/T2 提取需求推断补充 Lorentzian 拟合`

## Schema design

The spec is organized in five sections, each field wrapped in a `StatusField(value, status, note)`:

```
OpticalSpec
├── task               task_id, task_name, task_type, research_goal
├── physics            physical_system, physical_mechanism, model_dimension, structure_type
├── geometry_material  geometry_definition, material_system, particle_info,
│                      substrate_or_film_info, gap_medium, key_parameters
├── simulation         solver_method, software_tool, sweep_plan, excitation_source,
│                      source_setting, boundary_condition, mesh_setting, ...
├── output             output_observables, postprocess_target
└── system             confirmed_fields, inferred_fields, missing_fields,
                       assumption_log, validation_status
```

### Enums

| Enum | Values |
|------|--------|
| `TaskType` | modeling, simulation, fitting, data_analysis, plotting, writing |
| `SolverMethod` | fdtd, fem, rcwa, analytical, coupled_oscillator |
| `ModelDimension` | 2d, 3d, axisymmetric |
| `SoftwareTool` | meep, lumerical, comsol, matlab, python, ... |
| `PhysicalSystem` | nanoparticle_on_film, waveguide, metasurface, grating, ... |
| `StructureType` | sphere_on_film, rod_on_film, cube_on_film, cross_structure, ... |
| `ExcitationSource` | plane_wave, tfsf, dipole, mode_source, gaussian_beam, ... |

### Structured sub-models

Key fields use structured Pydantic models instead of raw strings:

| Sub-model | Fields |
|-----------|--------|
| `SweepPlan` | variable, range_start, range_end, step, unit |
| `SourceSetting` | source_type, wavelength_range, polarization, incident_angle |
| `BoundaryConditionSetting` | x_min/max, y_min/max, z_min/max |
| `GeometryDefinition` | geometry_type, dimensions (dict), units |
| `MaterialSystem` | materials (list of MaterialEntry with name, role, model) |
| `ParticleInfo` | particle_type, material, dimensions |

### Validation rules

The validator is **task-type-aware**:

- **Always required**: `task_type`, `research_goal`
- **simulation requires**: `solver_method`, `software_tool`, `excitation_source`, `source_setting`, `boundary_condition`, `monitor_setting`
- **Cross-field**: solver vs software consistency (fdtd→meep/lumerical), physical system rules (nanoparticle_on_film→particle_info), postprocess vs observables (fwhm_extraction→spectrum output)

### JSON Schema export

```python
from optical_spec_agent.models.spec import OpticalSpec
print(OpticalSpec.export_json_schema())
```

## Testing

```bash
pytest -v                      # 76 tests
pytest --cov=optical_spec_agent # with coverage
```

Test coverage includes:
- Model construction and serialization
- Parser: 6 Chinese inputs, 2 English inputs, inference rules
- Validator: required fields, consistency, physical system rules
- API endpoints: parse, validate, schema
- Service integration

## Project structure

```
optical-spec-agent/
├── pyproject.toml
├── Makefile
├── LICENSE
├── README.md
├── .gitignore
├── src/optical_spec_agent/
│   ├── __init__.py
│   ├── __main__.py                  # python -m support
│   ├── models/
│   │   ├── enums.py                 # All enum definitions
│   │   ├── base.py                  # StatusField, structured sub-models
│   │   ├── spec.py                  # OpticalSpec + JSON Schema export
│   │   └── __init__.py
│   ├── parsers/
│   │   ├── base.py                  # BaseParser ABC
│   │   ├── rule_based.py            # Keyword/regex parser (default)
│   │   ├── llm_placeholder.py       # LLM stub
│   │   └── __init__.py
│   ├── validators/
│   │   ├── spec_validator.py        # Task-type-aware validation
│   │   └── __init__.py
│   ├── services/
│   │   ├── spec_service.py          # Parse → validate orchestrator
│   │   └── __init__.py
│   ├── api/
│   │   ├── app.py                   # FastAPI app factory
│   │   ├── routes.py                # /health, /parse, /validate, /schema
│   │   └── __init__.py
│   ├── cli/
│   │   ├── main.py                  # parse, validate, schema, example
│   │   └── __init__.py
│   └── utils/
│       ├── format.py                # JSON + human-readable summary
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_parser.py               # 38 parser tests
│   ├── test_validator.py
│   ├── test_service.py
│   └── test_api.py
├── examples/
│   ├── example_01_nanoparticle_gap_plasmon.py
│   ├── example_02_asymmetric_gold_cross.py
│   ├── example_03_lumerical_fdtd_scattering.py
│   ├── example_04_comsol_mode_analysis.py
│   └── example_05_lorentzian_fitting.py
└── outputs/
    └── .gitkeep
```

## Roadmap

| Version | Goal | Status |
|---------|------|--------|
| **v0.1** | NL → spec JSON + validation (rule-based) | **Done** |
| v0.2 | LLM parser integration (Claude / GPT) | Planned |
| v0.3 | Meep adapter (spec → `.ctl` script) | Planned |
| v0.4 | Lumerical adapter (spec → `.lsf` script) | Planned |
| v0.5 | COMSOL adapter (spec → `.mph` Java API) | Planned |
| v1.0 | Full multi-agent loop: spec → simulate → postprocess → report | Planned |

## License

[MIT](LICENSE)
