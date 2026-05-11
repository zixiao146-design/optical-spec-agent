# v0.9 Workflow Benchmark

The workflow benchmark verifies deterministic local orchestration behavior. It
does not run external solvers and does not judge physical correctness.

## Run

```bash
python benchmarks/run_workflow_benchmark.py \
  --cases benchmarks/workflow_cases.json \
  --output-dir outputs/workflow_benchmark \
  --report outputs/workflow_benchmark_report.json
```

Or:

```bash
make workflow-check
```

## Case Schema

Each case includes:

- `id`
- `text`
- `parser`
- `llm_provider`
- `tool`
- `expected_steps`
- `expected_artifacts`
- `expected_warnings` optional
- `not_expected_claims`

## Report Schema

The report includes:

- `schema_version`
- `generated_at`
- `total_cases`
- `passed_cases`
- `failed_cases`
- `cases[]`

Each case records missing steps, missing artifacts, warnings, errors, output
directory, and whether false production/solver-execution claims were avoided.

## What It Tests

- Workflow CLI/runner compatibility with Meep, MPB, Gmsh, Elmer, and Optiland intent.
- Artifact creation and source-of-truth `workflow_run.json`.
- No false claim that solvers ran when `--no-execute` is used.
- Human review artifacts are present for ambiguous or incomplete specs.

## What It Does Not Test

- Physical correctness.
- Solver convergence.
- External LLM provider quality.
- MPB/Gmsh/Elmer/Optiland execution.
