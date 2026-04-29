# Benchmarks

Golden-case regression tests for the rule-based parser + validator pipeline.
The v0.3 reliability milestone also adds a semantic benchmark for the core
Meep nanoparticle-on-film parsing path.

## Benchmark modes

| Mode | What it checks | When to use |
|------|---------------|-------------|
| `exact` (default) | Full output JSON must match golden snapshot byte-for-byte | CI regression — catches any parser change |
| `key_fields` | Only core fields must be present with `confirmed`/`inferred` status | Assessing parser extraction quality — resilient to non-breaking output changes |
| `all` | Runs both modes | Full check |

Semantic benchmark:

| Runner | What it checks |
|--------|----------------|
| `python benchmarks/run_semantic_benchmark.py` | Core-case semantic fields such as particle diameter, film thickness, gap medium, solver path, and postprocess targets |

**Key fields** checked in `key_fields` mode: `task.task_type`, `physics.physical_system`, `simulation.solver_method`, `output.output_observables`. Cases can override this list by adding an `expected_key_fields` array to their golden entry.

## What this does NOT benchmark

- **Semantic understanding quality** — exact mode checks byte equality, not "best" interpretation
- **Solver correctness** — no solver is invoked
- **LLM parsing** — only the rule-based parser is tested
- **Edge case robustness** — the snapshot benchmark covers 16 common regression cases, while the semantic benchmark currently focuses on one reliability-critical Meep case

## File structure

```
benchmarks/
├── README.md              # This file
├── golden_cases.json      # 16 golden test cases with input + expected output
├── run_benchmark.py       # Runner with exact / key_fields / all modes
├── semantic_cases.json    # Semantic assertions for reliability-critical cases
└── run_semantic_benchmark.py
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

# Semantic benchmark for the core Meep case
python benchmarks/run_semantic_benchmark.py

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

## v0.3 reliability focus

The semantic benchmark intentionally avoids full JSON snapshot matching. It checks
only the meaning-bearing fields that matter for the current milestone:

- `SiO2` must not degrade into `Si`
- `80 nm` particle size must land in `particle_info.dimensions`
- `100 nm` film thickness must land in `substrate_or_film_info`
- `Meep + FDTD + plane_wave` path must remain stable
- `resonance_wavelength` and `fwhm_extraction` postprocess targets must be present
