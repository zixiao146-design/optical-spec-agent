# Local Meep Stability Matrix Report v0.5

This report records local/manual stability diagnostics for the v0.5
research-preview Meep script. It is evidence for debugging and release hygiene,
not a default CI gate and not a claim of production-grade physical fidelity.

## Environment

- Repository: `/Users/lizixiao/Desktop/光学设计agent/optical-spec-agent`
- Date: 2026-04-30 UTC
- Meep command detected by `check_meep_available()`:
  `micromamba run -n meep python -c "import meep"`
- Current project Python was not the Meep runtime; Meep was available through
  the `micromamba` environment named `meep`.
- Ordinary CI does not install or require Meep.

## Why This Matrix Exists

The normal research-preview script previously passed the PML/cell geometry
validity issue but failed at runtime with:

```text
RuntimeError: meep: simulation fields are NaN or Inf
```

The working hypothesis is numerical instability in the research-preview setup,
especially around dispersive library metal materials, boundary treatment, source
placement, and time stepping. The Meep FAQ commonly discusses field blow-up
causes such as PML interactions, material dispersion, and Courant/resolution
choices; this matrix does not prove the root cause, but it makes local
diagnostics reproducible.

Reference: <https://meep.readthedocs.io/en/latest/FAQ/>

## Matrix Profiles

| Case | Diagnostic profile | Boundary | Material mode | Courant | Resolution | Freq points | Result |
|------|--------------------|----------|---------------|---------|------------|-------------|--------|
| `smoke` | `normal` | PML | smoke dielectric | Meep default | smoke template | smoke template | Passed |
| `research_preview_pml_library` | `normal` | PML | `meep.materials` Au/SiO2 | Meep default | 50 | 200 | Failed: NaN/Inf |
| `research_preview_absorber_library` | `normal` | Absorber | `meep.materials` Au/SiO2 | Meep default | 50 | 200 | Failed: NaN/Inf |
| `research_preview_absorber_library_courant_025` | `normal` | Absorber | `meep.materials` Au/SiO2 | 0.25 | 50 | 200 | Timed out after 120 s |
| `research_preview_absorber_dielectric_sanity` | `normal` | Absorber | nonphysical dielectric placeholders | Meep default | 50 | 200 | Timed out after 120 s |
| `research_preview_low_cost_dielectric_sanity` | `low_cost` | Absorber | nonphysical dielectric placeholders | 0.25 | 8 | 5 | Passed |

## Low-Cost Diagnostic Profile

The `low_cost` profile is intentionally nonphysical. It exists only to verify
the execution pipeline:

- Uses `boundary_type=absorber`
- Uses `material_mode=dielectric_sanity`
- Uses `Courant=0.25`
- Uses `resolution=8`
- Uses `freq_points=5`
- Uses fixed short reference and structure runs instead of an unbounded decay
  wait
- Writes clear generated-script warnings that output is diagnostic only and not
  valid for physical interpretation

## Run Evidence

### Smoke

- Command:
  `python scripts/local_meep_stability_matrix.py --skip-research --timeout-smoke 300`
- Run ID: `stability-matrix-20260430-105140-c3f6ea40`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-105140-c3f6ea40/smoke`
- Success: yes
- Return code: 0
- Required outputs: none for smoke mode
- `execution_result.json`: success true, available true, expected mode `smoke`
- `run_manifest.json`: present

### Low-Cost Dielectric Sanity

- Command:
  `python scripts/local_meep_stability_matrix.py --only low-cost-dielectric-sanity --timeout-research 600`
- Run ID: `stability-matrix-20260430-105201-135cf0ff`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-105201-135cf0ff/research_preview_low_cost_dielectric_sanity`
- Success: yes
- Return code: 0
- Generated `scattering_spectrum.csv`: yes
- Generated `postprocess_results.json`: yes
- Generated `scattering_spectrum.png`: yes
- Generated `execution_result.json`: yes, `success=true`
- Generated `run_manifest.json`: yes
- `typed_postprocess_results`: present as a dict in `execution_result.json`
- `physical_interpretation`: false
- `recommended_for_execution_pipeline_debug`: true

The parsed `postprocess_results.json` includes:

```json
{
  "mode": "research_preview",
  "diagnostic_profile": "low_cost",
  "boundary_type": "absorber",
  "material_mode": "dielectric_sanity",
  "resolution": 8,
  "freq_points": 5
}
```

Any resonance or FWHM values in this run are diagnostic artifacts of a
nonphysical setup and must not be interpreted as real Au nanoparticle-on-film
physics.

### PML + Library Metals

- Command:
  `python scripts/local_meep_stability_matrix.py --only pml-library --timeout-research 120`
- Run ID: `stability-matrix-20260430-105257-8fcdaa07`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-105257-8fcdaa07/research_preview_pml_library`
- Success: no
- Return code: 1
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Generated `execution_result.json`: yes
- Generated `run_manifest.json`: yes
- Error summary:
  - `RuntimeError: meep: simulation fields are NaN or Inf`
  - missing required `scattering_spectrum.csv`
  - missing required `postprocess_results.json`

### Absorber + Library Metals

- Command:
  `python scripts/local_meep_stability_matrix.py --only absorber-library --timeout-research 120`
- Run ID: `stability-matrix-20260430-105432-e5041e1d`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-105432-e5041e1d/research_preview_absorber_library`
- Success: no
- Return code: 1
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Generated `execution_result.json`: yes
- Generated `run_manifest.json`: yes
- Error summary:
  - `RuntimeError: meep: simulation fields are NaN or Inf`
  - missing required `scattering_spectrum.csv`
  - missing required `postprocess_results.json`

### Absorber + Library Metals + Courant 0.25

- Command:
  `python scripts/local_meep_stability_matrix.py --only absorber-library-courant-025 --timeout-research 120`
- Run ID: `stability-matrix-20260430-105607-05ba4f17`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-105607-05ba4f17/research_preview_absorber_library_courant_025`
- Success: no
- Return code: null
- Timeout: 120 s
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Error summary:
  - `Meep script timed out after 120 seconds`

### Absorber + Dielectric Sanity

- Command:
  `python scripts/local_meep_stability_matrix.py --only dielectric-sanity --timeout-research 120`
- Run ID: `stability-matrix-20260430-105816-07073e07`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-105816-07073e07/research_preview_absorber_dielectric_sanity`
- Success: no
- Return code: null
- Timeout: 120 s
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Error summary:
  - `Meep script timed out after 120 seconds`

## Interpretation

- Smoke remains healthy, so basic script generation and Meep availability are
  intact.
- PML/library Au and Absorber/library Au still fail with NaN/Inf.
- Lowering Courant to 0.25 avoids immediate NaN/Inf in the short diagnostic
  window but still does not complete the normal research-preview output
  contract.
- Normal `dielectric_sanity` still times out at full research-preview cost.
- `low_cost` is the first profile that completes the research-preview execution
  contract and produces CSV/JSON/PNG plus execution artifacts.

## Current Recommendation

For v0.5, the landed, honest contract can be:

- `smoke` is a local executable gate for basic Meep runtime availability.
- `research-preview` generation remains available as an auditable script
  generator.
- Normal Au library research-preview execution is not stable yet.
- `diagnostic_profile=low_cost` can validate the execution/result-artifact
  pipeline locally, but it is nonphysical and not valid for physical
  interpretation.

This is enough to land v0.5 as an execution harness plus diagnostic
research-preview pipeline, not as production-grade Meep simulation automation.

## Release Candidate Plan

If the final test suite remains green, v0.5 can move to release hygiene with:

- `pyproject.toml`: `0.4.0` to `0.5.0`
- `src/optical_spec_agent/__init__.py`: `0.4.0` to `0.5.0`
- README roadmap: v0.5 `Started` to `Done`
- New release notes: `docs/release_notes_v0.5.0.md`

Do not describe v0.5 as production-grade physical simulation. The accurate
claim is: optional Meep execution harness, auditable artifacts, and a nonphysical
low-cost diagnostic research-preview profile that proves the output contract.

## Next Diagnostic Steps

- Investigate why library Au profiles still produce NaN/Inf.
- Try `eps_averaging=False` and lower-resolution library profiles.
- Review flux-box size, source placement, and decay monitor location for normal
  research-preview stability.
- Keep real research-preview execution outside default CI until a physically
  meaningful stable profile is demonstrated.
