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
- Relevant diagnostic scripts:
  - `python scripts/local_meep_stability_matrix.py --timeout-smoke 300 --timeout-research 3600`
  - `python scripts/local_meep_stability_matrix.py --skip-research --timeout-smoke 300`
  - `python scripts/local_meep_stability_matrix.py --only absorber-library-courant-025 --timeout-research 300`
  - `python scripts/local_meep_stability_matrix.py --only dielectric-sanity --timeout-research 300`

## Why This Matrix Exists

The core research-preview script previously passed the PML/cell geometry
validity issue but failed at runtime with:

```text
RuntimeError: meep: simulation fields are NaN or Inf
```

The working hypothesis is numerical instability in the research-preview setup,
especially around dispersive library metal materials, boundary treatment, and
time stepping. The Meep FAQ commonly discusses field blow-up causes such as PML
interactions, material dispersion, and Courant/resolution choices; this matrix
does not prove the root cause, but it makes local diagnostics reproducible.

Reference: <https://meep.readthedocs.io/en/latest/FAQ/>

## Matrix Profiles

| Case | Boundary | Material mode | Courant | Result |
|------|----------|---------------|---------|--------|
| `smoke` | PML | simple smoke dielectric | Meep default | Passed |
| `research_preview_pml_library` | PML | `meep.materials` Au/SiO2 | Meep default | Failed: NaN/Inf |
| `research_preview_absorber_library` | Absorber | `meep.materials` Au/SiO2 | Meep default | Failed: NaN/Inf |
| `research_preview_absorber_library_courant_025` | Absorber | `meep.materials` Au/SiO2 | 0.25 | Timed out after 300 s |
| `research_preview_absorber_dielectric_sanity` | Absorber | nonphysical dielectric placeholders | Meep default | Timed out after 300 s |

## Run Evidence

### Smoke

- Run ID: `stability-matrix-20260430-093957-52ef7a37`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-093957-52ef7a37/smoke`
- Success: yes
- Return code: 0
- Required outputs: none for smoke mode
- `execution_result.json`: success true, available true, expected mode `smoke`
- `run_manifest.json`: records command, run ID, workdir, return code, and empty
  missing output list

### PML + Library Metals

- Run ID: `stability-matrix-20260430-093007-9d16c5c7`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-093007-9d16c5c7/research_preview_pml_library`
- Success: no
- Return code: 1
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Error summary:
  - `RuntimeError: meep: simulation fields are NaN or Inf`
  - missing required `scattering_spectrum.csv`
  - missing required `postprocess_results.json`

### Absorber + Library Metals

- Run ID: `stability-matrix-20260430-093007-9d16c5c7`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-093007-9d16c5c7/research_preview_absorber_library`
- Success: no
- Return code: 1
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Error summary:
  - `RuntimeError: meep: simulation fields are NaN or Inf`
  - missing required `scattering_spectrum.csv`
  - missing required `postprocess_results.json`

### Absorber + Library Metals + Courant 0.25

- Run ID: `stability-matrix-20260430-094549-0eb6197d`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-094549-0eb6197d/research_preview_absorber_library_courant_025`
- Success: no
- Return code: null
- Timeout: 300 s
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Error summary:
  - `Meep script timed out after 300 seconds`

This profile did not reproduce the immediate NaN/Inf failure inside the shorter
diagnostic window, but it also did not complete the research-preview output
contract.

### Absorber + Dielectric Sanity

- Run ID: `stability-matrix-20260430-094007-59a51286`
- Artifact directory:
  `runs/stability-matrix/stability-matrix-20260430-094007-59a51286/research_preview_absorber_dielectric_sanity`
- Success: no
- Return code: null
- Timeout: 300 s
- Generated `scattering_spectrum.csv`: no
- Generated `postprocess_results.json`: no
- Generated `scattering_spectrum.png`: no
- Error summary:
  - `Meep script timed out after 300 seconds`

`dielectric_sanity` is explicitly nonphysical. Its purpose is only to validate
the execution pipeline without dispersive metal materials. In this run it did
not fail with NaN/Inf, but it also did not finish inside the 300 s diagnostic
window.

## Interpretation

- Smoke remains healthy, so the basic script generation and Meep availability
  path are intact.
- Switching PML to Absorber alone did not fix the Au library material NaN/Inf
  failure.
- Lowering Courant to 0.25 changed the failure mode from quick NaN/Inf to a
  long-running case in the 300 s diagnostic window, but this is not yet a
  successful stable profile.
- `dielectric_sanity` avoids the immediate dispersive-metal NaN/Inf symptom in
  the 300 s window, but it still timed out and is not physically meaningful.
- No research-preview profile generated the required CSV/JSON output in these
  local diagnostics.

## Current Recommendation

There is no recommended production or research-stable Au library profile yet.
For v0.5, the stable contract is:

- `smoke` can be used as a local executable gate.
- `research-preview` can generate auditable scripts and execution artifacts.
- `research-preview` real Meep runs remain manual/local diagnostics and may
  fail with NaN/Inf or timeout.
- `dielectric_sanity` is a diagnostic mode only; never interpret it as a metal
  scattering result.

## Next Diagnostic Steps

- Add an explicitly low-cost research-preview diagnostic profile, likely by
  reducing resolution and frequency points for local execution only.
- Investigate source placement, flux-box size, and decay monitor location for
  slow decay or NaN/Inf sensitivity.
- Try `eps_averaging=False` and lower Courant combinations as additional matrix
  profiles.
- Keep real research-preview execution outside default CI until a stable local
  profile is demonstrated.
