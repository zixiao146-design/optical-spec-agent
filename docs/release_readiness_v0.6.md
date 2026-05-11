# v0.6 Release Readiness Notes

## Current Version State

- Packaged baseline: `v0.5.0` in `pyproject.toml` and package metadata.
- Current `main` branch: v0.6 local/manual diagnostics work.
- GitHub latest formal release may therefore lag behind the current `main`
  branch capabilities until a v0.6 release is explicitly cut.

Do not create a GitHub release or tag from this note alone.

## v0.6 Completion Items

- Stable user-facing diagnostics entry point:
  `optical-spec diagnose`.
- Backward-compatible script wrapper:
  `python scripts/generate_physical_diagnostics.py`.
- Post-hoc diagnostics artifacts:
  `mesh_report.csv`, `flux_report.csv`, `execution_diagnostics.json`, and
  `diagnostic_preview.png`.
- Execution artifact checks for `stdout.txt`, `stderr.txt`,
  `execution_result.json`, and `run_manifest.json`.
- Conservative detection for `NaN`, `Inf`, timeout text, nonzero return code,
  and `success=false`.
- Semantic benchmark report output via
  `python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json`.
- Tests covering missing specs, demo spec creation, missing/partial/corrupted
  run artifacts, JSON CLI output, CSV schema, PNG generation, and script wrapper
  compatibility.

## v0.6 Does Not Claim

- No real LLM parser.
- No full solver automation.
- No production-grade physical validation.
- No formal convergence proof.
- No production-grade visualization or plotting pipeline.
- No requirement that ordinary CI installs or runs Meep.
- No claim that the library-Au Meep profile is publication-ready; it remains a
  candidate-level local diagnostic profile.

## Validation Commands

```bash
pip install -e ".[dev]"
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
make check
optical-spec diagnose outputs/my_spec.json --output-dir outputs --create-demo-spec-if-missing
optical-spec diagnose outputs/my_spec.json --output-dir outputs --run-dir runs/demo --json
```

## Manual Meep Gates

These remain optional/local and are not ordinary CI requirements:

```bash
python scripts/local_meep_integration_gate.py --mode smoke
python scripts/local_meep_stability_matrix.py --skip-research
python scripts/local_meep_candidate_hardening.py --timeout 900
python scripts/local_meep_observable_diagnostics.py --timeout 900
```

## Release Blockers To Review

- Decide whether to bump package version from `0.5.0` to `0.6.0`.
- Decide whether generated local artifacts under `outputs/` should remain
  ignored or whether tiny example reports should be checked in.
- Re-run manual Meep smoke gate on a machine with Meep installed.
- Keep release notes clear that v0.6 is diagnostics hardening, not production
  simulation validation.

## Recommended v0.6 Release Notes

Suggested headline:

> v0.6 adds a stable post-hoc diagnostics CLI for OpticalSpec/Meep artifacts.

Suggested bullets:

- Added `optical-spec diagnose` for mesh, flux, execution-artifact, and preview
  diagnostics.
- Added stable diagnostics report fields and CSV schemas.
- Added semantic benchmark JSON reporting.
- Expanded tests for missing/corrupted execution artifacts and JSON CLI output.
- Preserved the script wrapper for automation compatibility.
- Reaffirmed that diagnostics are local/manual sanity checks, not production
  physical validation.
