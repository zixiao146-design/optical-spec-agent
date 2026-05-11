# v0.6 Physical Diagnostics Reports

This project now includes a small local diagnostics layer for the hero workflow:

```text
natural language optical task
-> OpticalSpec JSON
-> Meep script
-> optional execution artifacts
-> post-hoc mesh/flux/execution diagnostics
```

The diagnostics layer is intentionally post-hoc. It does not run Meep, does not
change the parser, and does not claim production-grade physical validation.

## Recommended CLI

```bash
optical-spec diagnose outputs/my_spec.json \
  --output-dir outputs \
  --run-dir runs/demo \
  --create-demo-spec-if-missing
```

`diagnose` is the stable user-facing entry point. It reads an `OpticalSpec`
JSON and optionally links it to an existing `meep-run` directory. It does not
generate a Meep script and does not run Meep.

Supported options:

- `SPEC_PATH` positional argument, for example `outputs/my_spec.json`
- `--spec <path>` as an explicit alternative to the positional path
- `--output-dir <path>` for reports, default `outputs`
- `--run-dir <path>` for existing Meep execution artifacts
- `--create-demo-spec-if-missing` to create a traceable core demo spec
- `--json` for machine-readable CLI output

## Backward-Compatible Script

The script wrapper remains available for automation and backwards
compatibility. It calls the same core implementation as the CLI:

```bash
python scripts/generate_physical_diagnostics.py \
  --spec outputs/my_spec.json \
  --output-dir outputs \
  --run-dir runs/observable-diagnostics/<matrix_run_id>/closed-box-baseline \
  --create-demo-spec-if-missing
```

If `outputs/my_spec.json` is missing, `--create-demo-spec-if-missing` creates a
traceable demo spec from the core Meep nanoparticle-on-film task:

```text
80 nm Au sphere on 100 nm Au film, SiO2 gap = 5 nm,
normal-incidence plane wave, wavelength range 400-900 nm,
scattering spectrum, resonance wavelength, and FWHM.
```

## Outputs

All reports are written under `outputs/`:

- `mesh_report.csv`: `check_name`, `value`, `threshold`, `unit`, `status`, and
  `message` rows for grid size, gap cells, particle/film cells, and recommended
  resolution.
- `flux_report.csv`: `monitor_name`, `surface`, `value`, `unit`, `status`, and
  `message` rows plus per-monitor aggregate metrics.
- `execution_diagnostics.json`: traceable JSON summary of spec fields,
  provenance, mesh diagnostics, flux diagnostics, execution-result excerpts,
  warnings, and errors.
- `diagnostic_preview.png`: a quick local visual artifact. The script uses
  matplotlib if available; otherwise it writes a small built-in fallback PNG.

## Mesh Interpretation

The current v0.6 physical candidate is execution-stable but not physically
resolved for the 5 nm gap. With the diagnostic default `resolution=12 px/um`,
the grid spacing is about `83 nm`, so:

```text
gap_cells = 5 nm / 83 nm ~= 0.06
```

The diagnostics therefore flag:

- `gap is under-resolved`
- `particle radius has very few grid cells`
- `film thickness has very few grid cells`

These warnings should not be treated as failures of the execution harness. They
mean the run is useful for artifact plumbing and stability diagnostics, not for
quantitative physical interpretation.

## Flux Interpretation

When `flux_surfaces.csv` is available, the diagnostics compute each monitor
surface separately:

- `flux_x_minus`
- `flux_x_plus`
- `flux_y_minus`
- `flux_y_plus`
- `flux_z_minus`
- `flux_z_plus`
- `flux_total`

Near-zero signals are flagged conservatively. This is a diagnostic heuristic,
not a physical standard. It is meant to catch cases where the observable is too
weak or too cancellation-prone for meaningful convergence metrics.

## Execution Artifact Checks

When `--run-dir` is provided, diagnostics look for the standard artifacts from
`optical-spec meep-run`:

- `stdout.txt`
- `stderr.txt`
- `execution_result.json`
- `run_manifest.json`

Missing files do not crash the command. They are recorded in
`execution_diagnostics.json` as `missing_artifacts` and turn the report status
into `warning`.

The diagnostics read `execution_result.json`, plus `stdout.txt` and `stderr.txt`
when available. They flag:

- `NaN` / `Inf`
- timeout text
- nonzero return code
- missing execution artifacts

The result is written into `execution_diagnostics.json` so the diagnostic chain
is auditable after the run.

The top-level JSON includes at least:

- `schema_version`
- `spec_path`
- `output_dir`
- `run_dir`
- `generated_at`
- `status`
- `warnings`
- `errors`
- `missing_artifacts`
- `nan_detected`
- `inf_detected`
- `timeout_detected`
- `notes`

## Benchmark Report

The semantic benchmark runner can also write a machine-readable report:

```bash
python benchmarks/run_semantic_benchmark.py \
  --report outputs/semantic_benchmark_report.json
```

The report records every semantic check, pass/fail status, and diagnostic
message. This is useful for comparing parser behavior after adding new semantic
coverage without refreshing exact JSON snapshots.

## Current Limitations

- This is still local/manual tooling, not ordinary CI.
- It does not run Meep by itself.
- It does not prove convergence.
- `diagnostic_preview.png` is a readability artifact, not a scientific figure.
- The v0.6 library-Au physical candidate remains a candidate, not a validated
  production simulation profile.
