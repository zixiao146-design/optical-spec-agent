# Local Meep Physical Stability Pre-Study v0.6

This document records a local/manual v0.6 pre-study for physical Au
research-preview stability. It is not a release validation, not a default CI
gate, and not production-grade Meep simulation evidence.

## Purpose

v0.5 proved the execution harness and a nonphysical low-cost diagnostic loop:
`scattering_spectrum.csv`, `postprocess_results.json`,
`scattering_spectrum.png`, `execution_result.json`, and `run_manifest.json`.

The v0.6 pre-study asks a narrower question:

Can any bounded, library-Au research-preview profile complete the artifact
contract without NaN/Inf or timeout?

## Environment

- Date: 2026-04-30 UTC
- Repository: `/Users/lizixiao/Desktop/光学设计agent/optical-spec-agent`
- Meep command:
  `micromamba run -n meep python -c "import meep"`
- Meep was available through the `micromamba` environment named `meep`.
- Ordinary CI still does not install or require Meep.

## Baseline

- v0.5 low-cost dielectric-sanity diagnostic passes.
- Normal PML + library Au research-preview previously failed with NaN/Inf.
- Normal Absorber + library Au research-preview previously failed with NaN/Inf.
- Absorber + library Au + Courant 0.25 previously timed out in normal profile.

## Probe Matrix

The probe script is:

```bash
python scripts/local_meep_physical_stability_probe.py --quick --timeout 600
```

It writes artifacts to:

```text
runs/physical-stability-probe/<matrix_run_id>/<case_name>/
```

and writes a summary:

```text
runs/physical-stability-probe/<matrix_run_id>/physical_stability_summary.json
```

| Case | Source | Boundary | Material mode | Flux mode | Courant | Resolution | Freq points | Stop strategy | Result |
|------|--------|----------|---------------|-----------|---------|------------|-------------|---------------|--------|
| `low-cost-dielectric-sanity-control` | Ez | Absorber | dielectric_sanity | closed_box | 0.25 | 8 | 5 | fixed 30 | Passed |
| `source-ex-absorber-library-courant-025-fixed-50` | Ex | Absorber | library | closed_box | 0.25 | 12 | 10 | fixed 50 | Failed: NaN/Inf |
| `source-ex-absorber-library-courant-01-fixed-50` | Ex | Absorber | library | closed_box | 0.1 | 12 | 10 | fixed 50 | Passed |
| `source-ex-absorber-library-epsavg-false-fixed-50` | Ex | Absorber | library | closed_box | 0.25 | 12 | 10 | fixed 50 | Failed: NaN/Inf |
| `source-ex-absorber-library-single-plane-fixed-50` | Ex | Absorber | library | single_plane | 0.25 | 12 | 10 | fixed 50 | Failed: NaN/Inf |

Additional available but not run in the quick matrix:

- `particle-library-film-dielectric-fixed-50`
- `particle-dielectric-film-library-fixed-50`
- `lower-resolution-library-fixed-50`

These remain useful for isolating particle-vs-film dispersive material
instability if the candidate profile stops reproducing.

## Case Evidence

### Control: Low-Cost Dielectric Sanity

- Command:
  `python scripts/local_meep_physical_stability_probe.py --only low-cost-dielectric-sanity-control --timeout 300`
- Matrix run ID: `physical-probe-20260430-113332-f0a3cc08`
- Artifact directory:
  `runs/physical-stability-probe/physical-probe-20260430-113332-f0a3cc08/low-cost-dielectric-sanity-control`
- Success: yes
- Return code: 0
- Generated:
  - `scattering_spectrum.csv`
  - `postprocess_results.json`
  - `scattering_spectrum.png`
  - `execution_result.json`
  - `run_manifest.json`
- Physical interpretation level: `none`

This confirms the v0.5 diagnostic pipeline still works.

### Failed: Courant 0.25 Library Au

- Matrix run ID: `physical-probe-20260430-113353-df1f295c`
- Case: `source-ex-absorber-library-courant-025-fixed-50`
- Artifact directory:
  `runs/physical-stability-probe/physical-probe-20260430-113353-df1f295c/source-ex-absorber-library-courant-025-fixed-50`
- Success: no
- Return code: 1
- Missing outputs:
  - `scattering_spectrum.csv`
  - `postprocess_results.json`
- Error evidence:
  - `RuntimeError: meep: simulation fields are NaN or Inf`

### Candidate: Courant 0.1 Library Au

- Matrix run ID: `physical-probe-20260430-113353-df1f295c`
- Case: `source-ex-absorber-library-courant-01-fixed-50`
- Artifact directory:
  `runs/physical-stability-probe/physical-probe-20260430-113353-df1f295c/source-ex-absorber-library-courant-01-fixed-50`
- Success: yes
- Return code: 0
- Generated:
  - `scattering_spectrum.csv`
  - `postprocess_results.json`
  - `scattering_spectrum.png`
  - `execution_result.json`
  - `run_manifest.json`
- `typed_postprocess_results`: present
- Physical interpretation level: `physical_candidate`

Candidate configuration:

```text
diagnostic_profile=physical_probe
source_component=Ex
boundary_type=absorber
material_mode=library
flux_mode=closed_box
Courant=0.1
resolution=12
freq_points=10
stop_strategy=fixed
fixed_run_time=50
```

The generated `postprocess_results.json` included:

```json
{
  "diagnostic_profile": "physical_probe",
  "source_component": "Ex",
  "boundary_type": "absorber",
  "material_mode": "library",
  "flux_mode": "closed_box",
  "resolution": 12,
  "freq_points": 10
}
```

Peak metrics were produced by the current heuristic postprocess. They are not
validated physical results yet.

### Repeat: Courant 0.1 Library Au

- Command:
  `python scripts/local_meep_physical_stability_probe.py --only source-ex-absorber-library-courant-01-fixed-50 --timeout 900`
- Matrix run ID: `physical-probe-20260430-113427-be130474`
- Artifact directory:
  `runs/physical-stability-probe/physical-probe-20260430-113427-be130474/source-ex-absorber-library-courant-01-fixed-50`
- Success: yes
- Return code: 0
- Generated:
  - `scattering_spectrum.csv`
  - `postprocess_results.json`
  - `scattering_spectrum.png`
  - `execution_result.json`
  - `run_manifest.json`
- `typed_postprocess_results`: present

The repeat produced the same profile-level postprocess fields and successfully
completed the output contract.

## Other Failed Quick Probes

### `source-ex-absorber-library-epsavg-false-fixed-50`

- Success: no
- Return code: 1
- Missing CSV/JSON outputs
- Error evidence:
  - `RuntimeError: meep: simulation fields are NaN or Inf`

### `source-ex-absorber-library-single-plane-fixed-50`

- Success: no
- Return code: 1
- Missing CSV/JSON outputs
- Error evidence:
  - `RuntimeError: meep: simulation fields are NaN or Inf`
- Note: `single_plane` is diagnostic only and not a scattering cross-section.

## Interpretation

- A bounded physical-candidate profile exists locally:
  `Ex + Absorber + library Au + Courant 0.1 + closed_box + fixed 50`.
- The candidate completed twice and produced CSV/JSON/PNG plus execution
  artifacts.
- Courant remains a major stability lever: 0.25 failed with NaN/Inf, while 0.1
  passed under the same bounded fixed-run profile.
- This is still not production validation. The candidate uses low/moderate
  resolution, few frequency points, fixed runtime, and heuristic postprocessing.

## Release Recommendation

- v0.5 remains releaseable as:
  Meep execution harness + auditable artifacts + nonphysical low-cost diagnostic
  research-preview pipeline.
- v0.6 should focus on turning the physical candidate into a more credible
  research-preview profile by studying convergence, runtime, source placement,
  monitor placement, and material stability.

## Next Steps

- Repeat the candidate across slightly longer fixed run times, e.g. 100 and 200.
- Run candidate at higher resolution and more frequency points.
- Compare Ex and Ey.
- Investigate whether `Courant=0.1` is required generally or only for this
  geometry.
- Run mixed material isolation probes if NaN/Inf returns.
- Keep all real Meep research-preview runs outside ordinary CI.
