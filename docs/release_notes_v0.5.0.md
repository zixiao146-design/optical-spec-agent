# Release Notes v0.5.0

## Summary

v0.5.0 lands the first auditable Meep execution harness for
`optical-spec-agent`. The release can check local Meep availability, run an
already-generated Meep script, collect known outputs, and write structured run
artifacts.

This release does not make the project a production solver. Normal Au library
research-preview Meep runs remain unstable in local diagnostics and may fail
with NaN/Inf or timeout.

## What Is New

- Optional Meep execution harness in `optical_spec_agent.execution.meep_runner`
- `ExecutionResult` dataclass with JSON-serializable `to_dict()`
- Meep availability probing through current Python and `micromamba run -n meep`
- Explicit `meep-check` and `meep-run` CLI commands
- Mode-aware execution contract for `smoke`, `preview`, and `research-preview`
- Required-output validation for research-preview runs
- Local/manual integration gate script
- Local/manual stability matrix script
- Nonphysical low-cost diagnostic research-preview profile

## ExecutionResult Schema

`execution_result.json` uses schema version:

```text
execution_result.v0.1
```

Key fields include:

- `schema_version`
- `run_id`
- `created_at`
- `script_path`
- `expected_mode`
- `required_outputs`
- `missing_outputs`
- `outputs`
- `postprocess_results`
- `typed_postprocess_results`
- `success`
- `available`
- `returncode`
- `stdout`
- `stderr`
- `errors`
- `warnings`

## CLI

```bash
optical-spec meep-check --json
optical-spec meep-run generated_script.py --workdir runs/demo --expected-mode research-preview --timeout 300
```

`meep-run` supports:

- `--expected-mode auto|smoke|preview|research-preview`
- `--json`
- `--run-id`
- `--no-save-artifacts`
- `--timeout`
- `--workdir`

## Run Artifacts

By default, `meep-run` writes:

- `stdout.txt`
- `stderr.txt`
- `execution_result.json`
- `run_manifest.json`

For successful research-preview diagnostic runs, the generated script may also
write:

- `scattering_spectrum.csv`
- `postprocess_results.json`
- `scattering_spectrum.png`

## Typed Postprocess Results

When `postprocess_results.json` is present and is a JSON object,
`typed_postprocess_results` extracts a lightweight typed view:

- `mode`
- `resonance_wavelength_nm`
- `fwhm_nm`
- `gap_thickness_nm`
- `wavelength_min_nm`
- `wavelength_max_nm`
- `defaults_applied`
- `limitations`
- `raw`

The raw `postprocess_results` object is still preserved.

## Local Integration Gate

Manual/local gate:

```bash
python scripts/local_meep_integration_gate.py --mode smoke
python scripts/local_meep_integration_gate.py --mode research-preview --timeout 3600
```

This gate is not part of ordinary CI. It is intended for local evidence capture
when Meep is installed.

## Stability Matrix Gate

Manual/local stability matrix:

```bash
python scripts/local_meep_stability_matrix.py --skip-research
python scripts/local_meep_stability_matrix.py --only low-cost-dielectric-sanity --timeout-research 600
```

The matrix records boundary type, material mode, Courant factor, diagnostic
profile, output files, errors, warnings, and artifact directories.

## Low-Cost Diagnostic Profile

v0.5.0 includes:

```text
diagnostic_profile=low_cost
material_mode=dielectric_sanity
boundary_type=absorber
Courant=0.25
```

This profile is nonphysical and diagnostic only. It uses low resolution, few
frequency points, and fixed short runs to validate that the execution pipeline
can produce:

- `scattering_spectrum.csv`
- `postprocess_results.json`
- `scattering_spectrum.png`
- `execution_result.json`
- `run_manifest.json`

Do not interpret low-cost dielectric-sanity spectra as physical Au plasmon
simulation results.

## Verified Local Gates

Local evidence recorded in `docs/local_meep_stability_matrix_v0.5.md`:

- Smoke gate passed.
- Low-cost dielectric-sanity research-preview gate passed and produced the full
  CSV/JSON/PNG artifact loop.
- PML + library Au failed with NaN/Inf.
- Absorber + library Au failed with NaN/Inf.
- Absorber + library Au + Courant 0.25 timed out in the short diagnostic window.

## Known Limitations

- The project is still not a solver.
- v0.5.0 does not implement full solver automation.
- v0.5.0 does not provide production-grade result interpretation.
- Normal Au library research-preview execution is not stable yet.
- Real Meep execution is not part of ordinary CI.
- Low-cost dielectric-sanity output is nonphysical and diagnostic only.

## Tests

Release checks:

```bash
pytest
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
```

Do not refresh benchmark snapshots as part of this release.
