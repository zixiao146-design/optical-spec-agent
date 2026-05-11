# Benchmarks

Golden-case regression tests for the rule-based parser + validator pipeline.
The semantic benchmark now covers 27 reliability-critical parsing paths,
including the core Meep nanoparticle-on-film case plus material, gap, source,
boundary, single-particle, waveguide, and v0.7 adapter-target routing scenarios.
v0.8 also adds a deterministic LLM parser benchmark that uses the local `mock`
provider only; it does not call external APIs.

## Benchmark modes

| Mode | What it checks | When to use |
|------|---------------|-------------|
| `exact` (default) | Full output JSON must match golden snapshot byte-for-byte | CI regression — catches any parser change |
| `key_fields` | Only core fields must be present with `confirmed`/`inferred` status | Assessing parser extraction quality — resilient to non-breaking output changes |
| `all` | Runs both modes | Full check |

The default CI gate should use `pytest`, `key_fields`, and the semantic
benchmark. `exact` remains a manual regression tool for intentional
parser-change review, not the default CI gate.

Semantic benchmark:

| Runner | What it checks |
|--------|----------------|
| `python benchmarks/run_semantic_benchmark.py` | Semantic fields for 27 reliability-critical cases: Chinese + English Meep core cases, gap sweep extraction, SiO2 substrate disambiguation, Si3N4/SiO2 waveguide materials, oxide gaps, air/water gaps, TFSF/dipole/plane-wave sources, oblique incidence, periodic boundaries, Si single-particle, and MPB/Gmsh/Elmer/Optiland adapter-intent cases |
| `python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json` | Same benchmark plus a machine-readable pass/fail report for each semantic check |

LLM parser benchmark:

| Runner | What it checks |
|--------|----------------|
| `python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json` | Deterministic v0.8 parser-mode evaluation for `llm` / `hybrid` with mock provider, field accuracy, repair/fallback reporting, and ambiguous-case missing-field handling |

**Key fields** checked in `key_fields` mode: `task.task_type`, `physics.physical_system`, `simulation.solver_method`, `output.output_observables`. Cases can override this list by adding an `expected_key_fields` array to their golden entry.

## What this does NOT benchmark

- **Semantic understanding quality** — exact mode checks byte equality, not "best" interpretation
- **Solver correctness** — no solver is invoked
- **Real external LLM parsing** — v0.8 LLM cases use deterministic mock parsing
- **External LLM quality** — the v0.8 LLM benchmark uses deterministic mock output only
- **Edge case robustness** — the snapshot benchmark covers 16 common regression cases, while the semantic benchmark focuses on 27 reliability-critical material, geometry, source, boundary, and adapter-intent cases

## File structure

```
benchmarks/
├── README.md              # This file
├── golden_cases.json      # 16 golden test cases with input + expected output
├── run_benchmark.py       # Runner with exact / key_fields / all modes
├── semantic_cases.json    # Semantic assertions for reliability-critical cases
├── run_semantic_benchmark.py
├── llm_cases.json         # Deterministic v0.8 LLM parser evaluation cases
└── run_llm_benchmark.py
```

## Case format

Each entry in `golden_cases.json`:

```json
{
  "task_id": "golden-01",
  "input": "<natural language description>",
  "output": { ... },
  "expected_key_fields": ["task.task_type", "physics.physical_system", "..."]
}
```

The `expected_key_fields` field is optional — if absent, a default set of 4 core fields is used.

## Current cases

| ID | Physical System | Solver | Language | Task Type |
|----|----------------|--------|----------|-----------|
| golden-01 | nanoparticle_on_film (cube) | FDTD | Chinese | simulation |
| golden-02 | nanoparticle_on_film (sphere) | FDTD (Meep) | Chinese | simulation |
| golden-03 | nanoparticle_on_film (cross) | FDTD (Lumerical) | Chinese | simulation |
| golden-04 | waveguide (Si3N4 ridge) | FEM (COMSOL) | Chinese | simulation |
| golden-05 | scattering spectrum | Python scipy | Chinese | fitting |
| golden-06 | metasurface (TiO2) | RCWA | Chinese | simulation |
| golden-07 | nanoparticle_on_film (sphere) | FDTD (Meep) | English | simulation |
| golden-08 | waveguide (Si ridge) | FEM (COMSOL) | English | simulation |
| golden-09 ~ golden-16 | additional regression coverage | mixed | mixed | mixed |

## How to run

```bash
# Exact regression (default)
python benchmarks/run_benchmark.py

# Key-field extraction check
python benchmarks/run_benchmark.py --mode key_fields

# Both modes
python benchmarks/run_benchmark.py --mode all

# Semantic benchmark for reliability-critical cases
python benchmarks/run_semantic_benchmark.py

# Semantic benchmark report
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json

# LLM parser benchmark with deterministic mock provider
python benchmarks/run_llm_benchmark.py \
  --cases benchmarks/llm_cases.json \
  --parser hybrid \
  --llm-provider mock \
  --report outputs/llm_eval_report.json \
  --summary-csv outputs/llm_eval_summary.csv

# Workflow orchestration benchmark
python benchmarks/run_workflow_benchmark.py \
  --cases benchmarks/workflow_cases.json \
  --output-dir outputs/workflow_benchmark \
  --report outputs/workflow_benchmark_report.json

# Update golden snapshots after intentional parser changes
python benchmarks/run_benchmark.py --update
```

## How to add a new case

1. Choose a `task_id` (e.g., `golden-09`)
2. Run the parser and capture output:
   ```python
   from optical_spec_agent.services.spec_service import SpecService
   svc = SpecService()
   spec = svc.process("your input text", task_id="golden-09")
   ```
3. Add the entry to `golden_cases.json`
4. Optionally add `expected_key_fields` to customize which fields to check in key_fields mode
5. Run `python benchmarks/run_benchmark.py --mode all` to verify

## Semantic reliability focus

The semantic benchmark intentionally avoids full JSON snapshot matching. It checks
only meaning-bearing fields:

- `SiO2` and `Si3N4` must not degrade into `Si`
- `80 nm` particle size must land in `particle_info.dimensions`
- `100 nm` film thickness must land in `substrate_or_film_info`
- `gap from 5 to 25 nm` must not overwrite the actual wavelength range
- `Meep + FDTD + plane_wave` path must remain stable
- `TFSF`, `dipole`, oblique-incidence, and periodic-boundary descriptions should stay stable
- `Air`, `Water`, `Al2O3`, and `TiO2` gap/material mentions should not be silently dropped or split into shorter tokens
- `resonance_wavelength` and `fwhm_extraction` postprocess targets must be present
- `MPB`, `Gmsh`, `Elmer`, and `Optiland` requests should route to the intended software/solver fields without adding external solver dependencies

## v0.8 LLM benchmark focus

The LLM benchmark checks whether `llm` / `hybrid` parser modes can preserve the
same structured extraction contract under deterministic mock conditions. It
records:

- case pass/fail
- field accuracy
- parser mode/provider/model
- repair and fallback usage
- conflict count
- warnings and errors
- ambiguous-case missing-field handling

It does not test real external LLM providers, solver execution, or physical
correctness.

## v0.9 workflow benchmark focus

The workflow benchmark checks synchronous local orchestration completeness:

- expected workflow steps are present;
- expected artifacts such as `workflow_run.json`, `spec.json`, generated input,
  diagnostics, and review checklists are written;
- default workflows do not claim external solvers were executed;
- workflow runs remain deterministic with the mock parser provider.

It does not test async orchestration, cloud execution, external solvers, or
production-grade physical validation.
