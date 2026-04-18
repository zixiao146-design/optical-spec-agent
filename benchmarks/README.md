# Benchmarks

Golden-case regression tests for the rule-based parser + validator pipeline.

## What this benchmarks

**Key field matching** — each golden case pairs an input text with its expected structured output. The benchmark runner parses every input through the live parser and compares the output against the stored golden JSON, field by field.

Specifically, it verifies:
- All confirmed fields are correctly extracted (physical system, solver, materials, geometry, etc.)
- Inference rules fire as expected (e.g., `nanoparticle_on_film → 3D`, `FWHM/T2 → lorentzian_fit`)
- Missing fields are accurately reported
- Validation errors and warnings match expectations

## What this does NOT benchmark

This benchmark suite intentionally does **not** evaluate:
- **Semantic understanding quality** — it checks exact parser output against a snapshot, not whether the parser chose the "best" interpretation
- **Solver correctness** — no solver is invoked; the spec JSON is never used to run a simulation
- **LLM parsing** — only the rule-based parser is tested (LLM parser is a future placeholder)
- **Edge case robustness** — the 8 cases cover common scenarios, not adversarial or ambiguous inputs

## File structure

```
benchmarks/
├── README.md              # This file
├── golden_cases.json      # 8 golden test cases with input + expected output
└── run_benchmark.py       # Runner: parse all cases, compare vs golden
```

## Case format

Each entry in `golden_cases.json`:

```json
{
  "task_id": "golden-01",
  "input": "<natural language description>",
  "output": { ... }       // Expected OpticalSpec flat dict
}
```

The `output` contains the full spec structure: `task`, `physics`, `geometry_material`, `simulation`, `output`, plus `confirmed_fields`, `inferred_fields`, `missing_fields`, `assumption_log`, and `validation_status`.

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

## How to run

```bash
# Run all golden cases and check for regressions
python benchmarks/run_benchmark.py

# Update golden cases after intentional parser changes
python benchmarks/run_benchmark.py --update
```

**Output example:**
```
PASS  golden-01
PASS  golden-02
...
PASS  golden-08

8 cases: ALL PASSED
```

If a case fails, the runner prints a line-level diff showing where the output diverges from the golden snapshot.

## How to add a new case

1. Choose a descriptive `task_id` (e.g., `golden-09`)
2. Write the input text and run it through the parser:
   ```python
   from optical_spec_agent.services.spec_service import SpecService
   svc = SpecService()
   spec = svc.process("your input text", task_id="golden-09")
   print(spec.to_flat_dict())
   ```
3. Add the entry to `golden_cases.json` with the produced output
4. Run `python benchmarks/run_benchmark.py` to verify it passes
