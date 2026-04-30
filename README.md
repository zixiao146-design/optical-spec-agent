# optical-spec-agent

[![Tests](https://github.com/zixiao146-design/optical-spec-agent/actions/workflows/test.yml/badge.svg)](https://github.com/zixiao146-design/optical-spec-agent/actions/workflows/test.yml)

> Convert optical simulation requests into validated, solver-ready spec JSON — and generate Meep scripts.

**optical-spec-agent** is a compilation layer between human language and optical solvers. You describe a simulation task in plain text (Chinese or English), and it produces a single structured, validated JSON spec — with typed fields, provenance tracking, and completeness checks. Its Meep adapter can generate preview-oriented Python scripts for nanoparticle-on-film simulations.

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

It is **not** a solver. By default it generates specs and scripts. v0.5 starts
an optional harness that can run an existing generated Meep script when Meep is
installed, but this is not a full execution or result-parsing pipeline.

## At a glance

| | |
|---|---|
| **Demo outputs** | 3 real parser outputs — [gap plasmon](examples/outputs/demo_gap_plasmon_sweep.json), [gold cross](examples/outputs/demo_asymmetric_cross.json), [waveguide mode](examples/outputs/demo_comsol_waveguide.json) |
| **Adapter** | Meep script generator with `preview`, `research-preview`, and `smoke` modes (nanoparticle_on_film only) — see [adapter doc](docs/meep_adapter_v0.md) |
| **Benchmark** | 16 golden cases + 5 semantic benchmark cases for Meep reliability — `python benchmarks/run_benchmark.py --mode all` and `python benchmarks/run_semantic_benchmark.py` |
| **Tests** | `pytest -q` |

## Why this project?

Optical simulation tasks are inherently multi-parameter: geometry, materials, solver settings, sweep plans, post-processing targets. Humans describe these imprecisely; solvers require exact, structured input. This gap makes automation and multi-agent pipelines fragile.

`optical-spec-agent` is the **missing compiler**:
- **Input**: messy natural language
- **Output**: typed, validated spec JSON with per-field provenance (confirmed / inferred / missing)
- **Contract**: every field carries its status and derivation note, so downstream agents know what to trust and what to verify

## Current scope (v0.5 minimal execution harness)

The current loop:

```
Natural language  →  Rule-based parser  →  Structured spec JSON  →  Validation
                                                               ↓ (if Meep + nanoparticle_on_film)
                                                    Meep Python script (.py)
                                                               ↓ (optional explicit command)
                                                    Meep execution harness
```

**What works:**
- Keyword + regex parsing of Chinese and English optical task descriptions
- Structured sub-models for geometry, materials, sweep plans, source settings, boundary conditions
- Post-hoc inference (gap plasmon → FDTD, FWHM/T2 → Lorentzian fit, nanoparticle_on_film → 3D)
- Per-field provenance tracking: confirmed / inferred / missing
- Pydantic v2 validation with task-type-aware rules
- CLI, FastAPI, and Python SDK interfaces
- Semantic benchmark coverage for five reliability-critical parsing cases
- Meep adapter readiness checks + CLI readiness reporting before script generation
- Meep adapter script modes:
  `preview` for quick structure/script preview,
  `research-preview` for reference/structure runs plus CSV/JSON outputs,
  `smoke` for structural validation only
- Minimal Meep execution harness: availability check, explicit script run, and known output collection
- Schema stability policy: 20+ core fields frozen for 0.x

**What does NOT work yet:**
- Real LLM integration (only a placeholder parser exists)
- Full solver automation or managed result parsing pipeline
- Adapters for other solvers (MPB, Gmsh, Elmer, Optiland) — not yet implemented
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

# Generate Meep script from a spec
optical-spec parse "用Meep FDTD仿真金纳米球-金膜gap plasmon..." -o spec.json
optical-spec meep-generate spec.json -o sim.py
optical-spec meep-generate spec.json -o sim_research.py --mode research-preview
optical-spec meep-generate spec.json -o smoke.py --mode smoke

# Optional v0.5 execution harness for an existing generated script
optical-spec meep-check --json
optical-spec meep-run sim_research.py --workdir runs/demo --timeout 300 --expected-mode research-preview --run-id demo-001

# Manual/local Meep integration gates, not default CI gates
python scripts/local_meep_integration_gate.py --mode smoke
python scripts/local_meep_integration_gate.py --mode research-preview --timeout 3600
python scripts/local_meep_stability_matrix.py --skip-research
python scripts/local_meep_stability_matrix.py --only absorber-library-courant-025 --timeout-research 300
```

### Meep generation modes

- `preview`: 快速脚本预览，保留当前 smoke/preview 路径，不保证物理严谨。
- `research-preview`: 生成更可信的研究预览脚本，包含 reference run、structure run、flux subtraction、CSV 和 JSON 输出。
- `smoke`: 只验证生成脚本的结构和最小运行路径，不代表物理结果。

Script generation modes still generate scripts only. v0.5 starts a minimal
execution harness with `meep-check` and `meep-run`, but this is not a full solver
automation or result parsing pipeline yet. Real Meep execution tests are skipped
unless Meep is installed locally.

`meep-run` supports `--expected-mode smoke|preview|research-preview`. In
`research-preview` mode, successful execution requires both
`scattering_spectrum.csv` and `postprocess_results.json`. By default it writes
`stdout.txt`, `stderr.txt`, `execution_result.json`, and `run_manifest.json`
into the run directory. `execution_result.json` uses schema version
`execution_result.v0.1`. Use `--json` for machine-readable CLI output,
`--run-id` for a stable audit ID, or `--no-save-artifacts` to skip artifact
files.

The local integration gate is manual by design: smoke can be used for a quick
local sanity check, while research-preview can be slow and must be requested
explicitly. Ordinary CI does not require Meep to be installed.

v0.5 also includes a manual/local stability matrix for diagnosing
research-preview NaN/Inf issues. The matrix can switch between PML and Absorber
boundaries, lower the Meep Courant factor, and use a nonphysical
`dielectric_sanity` material mode to test execution plumbing. This diagnostic
gate is not part of ordinary CI, and `dielectric_sanity` results must not be
interpreted as physical metal scattering results. See
[`docs/local_meep_stability_matrix_v0.5.md`](docs/local_meep_stability_matrix_v0.5.md).

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

## Demo gallery

Three real parser outputs covering different physical systems and solvers. Each was generated by running the rule-based parser — no manual editing.

> **Note:** Demos include COMSOL and Lumerical inputs to demonstrate schema coverage. These are compatibility-oriented examples — the current adapter roadmap ([v0.3–v0.7](#roadmap)) targets open-source tools only (Meep, Elmer, Gmsh, Optiland).

### Demo 1: Nanoparticle-on-film gap plasmon

```
研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和
退相位时间的影响，使用 Meep FDTD，提取共振波长、FWHM 和 T2。
```

| Field | Value | Status |
|-------|-------|--------|
| `physics.physical_system` | `nanoparticle_on_film` | confirmed |
| `physics.structure_type` | `sphere_on_film` | confirmed |
| `simulation.solver_method` / `software_tool` | `fdtd` / `meep` | confirmed |
| `simulation.sweep_plan` | gap_nm 5→25 nm | confirmed |
| `output.postprocess_target` | lorentzian_fit, fwhm_extraction, T2_extraction | inferred |
| `physics.model_dimension` | `3d` | inferred |

Full JSON: [`examples/outputs/demo_gap_plasmon_sweep.json`](examples/outputs/demo_gap_plasmon_sweep.json)

### Demo 2: Asymmetric gold cross (Lumerical FDTD)

```
建模非对称金纳米十字结构，两臂长度分别为120nm和80nm，宽40nm，厚30nm，
放在SiO2基底上。用Lumerical FDTD计算偏振相关的散射谱，x偏振和y偏振都要做，
波长范围500-1200nm。
```

| Field | Value | Status |
|-------|-------|--------|
| `physics.structure_type` | `cross_structure` | confirmed |
| `simulation.software_tool` | `lumerical` | confirmed |
| `simulation.polarization` | `linear_x` | confirmed |
| `simulation.sweep_plan` | wavelength_nm 500→1200 nm | confirmed |

Full JSON: [`examples/outputs/demo_asymmetric_cross.json`](examples/outputs/demo_asymmetric_cross.json)

### Demo 3: COMSOL waveguide mode analysis

```
COMSOL模式分析：Si3N4脊波导（宽800nm，高400nm，蚀刻深度250nm），SiO2下包层，
上包层为空气，计算1.55μm波长下的基模有效折射率和模场分布，TE和TM模式都要计算。
```

| Field | Value | Status |
|-------|-------|--------|
| `physics.physical_system` | `waveguide` | confirmed |
| `simulation.solver_method` / `software_tool` | `fem` / `comsol` | confirmed |
| `output.output_observables` | field_distribution, mode_profile | confirmed |

Full JSON: [`examples/outputs/demo_comsol_waveguide.json`](examples/outputs/demo_comsol_waveguide.json)

**Reproduce any demo:**
```bash
optical-spec parse "<input text>" -o my_output.json
```

All demo outputs with detailed field annotations: [`examples/outputs/README.md`](examples/outputs/README.md)

## Schema design

> **Stability policy:** The core fields listed below are frozen for 0.1.x. See [`docs/schema_stability.md`](docs/schema_stability.md) for the full stable surface, volatile fields, and compatibility rules.

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
| `SoftwareTool` | meep, elmer, gmsh, optiland, rayoptics, python, ... |
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
- **Cross-field**: solver vs software consistency (fdtd→meep, fem→elmer), physical system rules (nanoparticle_on_film→particle_info), postprocess vs observables (fwhm_extraction→spectrum output), physical_system+structure_type combination check
- **Solver-specific**: FDTD requires source+boundary+monitor (≥3 missing → error); FEM requires boundary+monitor (both missing → error)
- **Severity escalation**: FWHM/T2 extraction without spectrum output → error (not just warning); nanoparticle_on_film with all geometry missing → error

### JSON Schema export

```python
from optical_spec_agent.models.spec import OpticalSpec
print(OpticalSpec.export_json_schema())
```

## Testing

```bash
pytest -q
pytest --cov=optical_spec_agent # with coverage
```

Test coverage includes:
- Model construction and serialization
- Parser: 6 Chinese inputs, 2 English inputs, inference rules
- Validator: required fields, consistency, physical system rules
- Meep adapter: script generation, rejection, missing field handling
- API endpoints: parse, validate, schema
- Service integration

## Benchmark

16 golden cases, 2 comparison modes:

```bash
python benchmarks/run_benchmark.py               # exact regression (default)
python benchmarks/run_benchmark.py --mode key_fields  # key-field extraction only
python benchmarks/run_benchmark.py --mode all         # both
```

| Mode | What it checks |
|------|---------------|
| `exact` | Full output JSON must match snapshot byte-for-byte — catches any parser change |
| `key_fields` | Only core fields (`task_type`, `physical_system`, `solver_method`, `observables`) must be present — resilient to non-breaking output changes |

**What it does NOT test:** semantic understanding scoring, solver correctness, or LLM parsing.

For the v0.3 reliability milestone, an additional semantic benchmark checks
five reliability-critical cases at the field level:

```bash
python benchmarks/run_semantic_benchmark.py
```

Full details: [`benchmarks/README.md`](benchmarks/README.md)

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
│   │   ├── main.py                  # parse, validate, schema, example, Meep commands
│   │   └── __init__.py
│   ├── execution/
│   │   ├── meep_runner.py           # Optional Meep availability/run harness
│   │   └── __init__.py
│   ├── adapters/
│   │   ├── base.py                  # BaseAdapter ABC + AdapterResult
│   │   └── meep/                    # Meep adapter (nanoparticle_on_film → script)
│   │       ├── models.py            # MeepInputModel
│   │       ├── translator.py        # OpticalSpec → MeepInputModel
│   │       └── template.py          # MeepInputModel → Python script
│   └── utils/
│       ├── format.py                # JSON + human-readable summary
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_parser.py               # Parser tests
│   ├── test_validator.py
│   ├── test_meep_adapter.py         # Meep adapter tests
│   ├── test_meep_runner.py          # Optional Meep execution harness tests
│   ├── test_local_meep_integration_gate.py
│   ├── test_service.py
│   └── test_api.py
├── scripts/
│   ├── local_meep_integration_gate.py
│   └── local_meep_stability_matrix.py
├── examples/
│   ├── example_01_nanoparticle_gap_plasmon.py
│   ├── example_02_asymmetric_gold_cross.py
│   ├── example_03_lumerical_fdtd_scattering.py
│   ├── example_04_comsol_mode_analysis.py
│   ├── example_05_lorentzian_fitting.py
│   ├── example_06_meep_nanoparticle.py
│   └── outputs/
│       ├── README.md
│       ├── demo_gap_plasmon_sweep.json
│       ├── demo_asymmetric_cross.json
│       ├── demo_comsol_waveguide.json
│       └── meep_nanoparticle_on_film.py
├── benchmarks/
│   ├── README.md
│   ├── golden_cases.json
│   ├── semantic_cases.json
│   ├── run_benchmark.py
│   └── run_semantic_benchmark.py
├── docs/
│   ├── open_source_stack.md              # Tool-stack rationale and per-tool specs
│   ├── open_source_integration_focus.md  # Adapter priority tiers and Meep-first rationale
│   ├── meep_adapter_v0.md               # Meep adapter scope and limitations
│   ├── local_meep_gate_report_v0.5.md    # Manual local Meep gate evidence
│   ├── local_meep_stability_matrix_v0.5.md # Manual Meep stability diagnostics
│   ├── schema_stability.md              # Stable field surface for 0.x
│   ├── adapter_architecture.md
│   ├── demo_output.md
│   ├── tool_mapping.md
│   └── repo_metadata.md                  # GitHub About + issue drafts
└── outputs/
    └── .gitkeep
```

## Roadmap

> **Strategy**: open-source-native, scriptable-first. All adapters target open-source tools
> (Meep, MPB, Gmsh, Elmer, Optiland, FreeCAD). Commercial software is not a core dependency.

| Version | Goal | Adapter Target | Status |
|---------|------|---------------|--------|
| **v0.1** | NL → spec JSON + validation (rule-based) | — | **Done** |
| v0.2 | Spec hardening + Meep adapter preview | **Meep** (script gen only) | Done |
| v0.3 | Core Meep reliability + semantic benchmark + adapter readiness | **Meep** (script gen only) | Done |
| v0.4 | Meep research-preview script: normalization run, CSV output, postprocess JSON | **Meep** (script gen only) | Done |
| **v0.5** | Meep execution + result parsing | **Meep** (FDTD) | Started |
| v0.6 | MPB / Gmsh / Elmer / Optiland adapters | **MPB** / **Gmsh** / **Elmer** / **Optiland** | Planned |
| v0.7 | LLM parser integration | — | Planned |
| v0.8 | Multi-agent orchestration | — | Planned |

**Why Meep first:** Pure Python API, spec fields map 1:1 to Meep objects, and a working adapter proves the full NL → spec → simulation chain. See [`docs/open_source_integration_focus.md`](docs/open_source_integration_focus.md) for the prioritization rationale.

**Adapter vs LLM:** Adapter work (v0.3–v0.6) ships before LLM integration (v0.7) because real solver feedback must stabilize the spec schema first. The rule-based parser + golden cases become the evaluation baseline for any future LLM parser.

See [`docs/open_source_stack.md`](docs/open_source_stack.md) for per-tool details and [`docs/open_source_integration_focus.md`](docs/open_source_integration_focus.md) for priority tiers.

## License

[MIT](LICENSE)
