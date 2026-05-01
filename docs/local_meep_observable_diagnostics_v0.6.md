# Local Meep Observable Diagnostics v0.6

This document records local/manual observable diagnostics for the current v0.6
library-Au physical candidate. It is not production validation and is not part
of ordinary CI.

## Purpose

The previous candidate convergence analysis showed that the v0.6 candidate can
run repeatedly and produce finite CSV/JSON/PNG artifacts, but the baseline
integrated flux was approximately `3.10e-24`. That is close enough to zero that
normalized L2 and integrated relative-difference metrics become `null`.

This round therefore diagnoses the observable itself: flux monitor geometry,
per-surface flux, and whether a diagnostic top-plane observable gives a stronger
signal than the closed flux box.

## Command

```bash
python scripts/local_meep_observable_diagnostics.py --timeout 900
```

Environment:

- Meep command: `micromamba run -n meep python -c "import meep"`
- Latest mesh/monitor matrix run ID: `observable-diagnostics-20260501-045806-82b41774`
- Artifact root: `runs/observable-diagnostics/observable-diagnostics-20260501-045806-82b41774/`

The run generated `observable_diagnostics_summary.json` under the artifact root.
The artifact directory is local evidence only and is not committed to the repo.

## Matrix

All supported cases used the current physical-candidate settings:

| Parameter | Value |
|-----------|-------|
| `source_component` | `Ex` |
| `boundary_type` | `absorber` |
| `material_mode` | `library` |
| `courant` | `0.1` |
| `resolution` | `12` |
| `freq_points` | `10` |
| `stop_strategy` | `fixed` |
| `fixed_run_time` | `50` |

| Case | Flux mode | Status |
|------|-----------|--------|
| `closed-box-baseline` | `closed_box` | ran |
| `gap-clearance-box` | `gap_clearance_box` | infeasible, fell back to top-plane |
| `upper-hemibox` | `upper_hemibox` | ran |
| `top-plane` | `top_plane` | ran |
| `closed-box-larger-clearance` | `closed_box` | unsupported until flux box padding/scale is exposed |
| `single-plane` | `single_plane` | ran |

## Results

| Case | Success | `max_abs_flux` | `integrated_abs_flux` | Near zero | `flux_surfaces.csv` | Intersects film |
|------|---------|----------------|-----------------------|-----------|---------------------|-----------------|
| `closed-box-baseline` | yes | `1.36e-26` | `3.10e-24` | yes | yes | yes |
| `gap-clearance-box` | yes | `1.11e-27` | `2.56e-25` | yes | yes | no |
| `upper-hemibox` | yes | `5.98e-27` | `1.37e-24` | yes | yes | no |
| `top-plane` | yes | `1.11e-27` | `2.56e-25` | yes | yes | no |
| `single-plane` | yes | `1.11e-27` | `2.56e-25` | yes | yes | no |

All supported cases generated:

- `scattering_spectrum.csv`
- `flux_surfaces.csv`
- `postprocess_results.json`
- `scattering_spectrum.png`
- `execution_result.json`
- `run_manifest.json`

## Geometry Diagnostics

The generated research-preview script now writes `geometry_diagnostics` into
`postprocess_results.json`.

For the closed-box baseline:

| Quantity | Value |
|----------|-------|
| `film_top_z` | `0.1` |
| `particle_center_z` | `0.145` |
| `particle_bottom_z` | `0.105` |
| `particle_top_z` | `0.185` |
| `flux_box_center_z` | `0.145` |
| `flux_box_bottom_z` | `0.045` |
| `flux_box_top_z` | `0.245` |
| `flux_box_intersects_film` | `true` |
| `flux_box_encloses_particle` | `true` |

The current flux box encloses the particle, but its bottom is below the film
top (`0.045 < 0.1`), so the closed flux box intersects the film. The generated
script records the warning:

```text
flux box intersects film; closed-box flux may be hard to interpret
```

The generated script also writes `mesh_diagnostics`. At the current candidate
settings, `resolution=12 px/um` means `grid_size_nm≈83.33`; the `5 nm` gap is
only `0.06` cells. The JSON records `gap_under_resolved=true` and recommends
approximately `1000 px/um` for five gap cells. This is a diagnostic heuristic,
not a formal convergence rule, but it confirms the current candidate is not
physically resolved.

## Per-Surface Flux

The generated research-preview script now writes `flux_surfaces.csv`.

For `closed-box-baseline`, the per-surface diagnostic summary was:

| Surface | `max_abs_flux` | signed sum | abs sum |
|---------|----------------|------------|---------|
| `flux_x_minus` | `3.12e-27` | `7.67e-27` | `7.67e-27` |
| `flux_x_plus` | `3.12e-27` | `7.67e-27` | `7.67e-27` |
| `flux_y_minus` | `3.12e-27` | `7.67e-27` | `7.67e-27` |
| `flux_y_plus` | `3.12e-27` | `7.67e-27` | `7.67e-27` |
| `flux_z_minus` | `4.81e-29` | `-1.06e-28` | `1.12e-28` |
| `flux_z_plus` | `1.11e-27` | `2.74e-27` | `2.74e-27` |

The closed-box `cancellation_ratio` was approximately `0.994`, so the near-zero
total is not primarily caused by strong positive/negative surface cancellation.
Instead, each particle-induced surface signal is already extremely small.

## Top-Plane Result

`top_plane` and `single_plane` both completed successfully and produced the
optional `flux_surfaces.csv`, but their signal was weaker than the closed-box
baseline:

- `closed_box max_abs_flux`: `1.36e-26`
- `upper_hemibox max_abs_flux`: `5.98e-27`
- `top_plane max_abs_flux`: `1.11e-27`
- `single_plane max_abs_flux`: `1.11e-27`

Therefore, `top_plane` is useful as a diagnostic observable, but it is not a
stronger candidate for the next convergence matrix. It is also not a scattering
cross-section.

`upper_hemibox` avoids the film and is stronger than `top_plane`, but it is
still near zero and is also not a closed scattering cross-section.

## Interpretation

This diagnostic pass shifts the likely blocker:

- The execution harness is stable for these profiles.
- The output artifacts are generated reliably.
- `flux_surfaces.csv` does not show strong surface cancellation.
- The closed-box monitor intersects the film, which makes the observable hard
  to interpret.
- The gap is severely under-resolved at the current mesh.
- A simple top-plane diagnostic does not produce a stronger signal.
- `upper_hemibox` avoids the film but is still near-zero.

The next v0.6 step should resolve mesh and monitor geometry before running
larger convergence matrices. See
[`local_meep_mesh_monitor_diagnostics_v0.6.md`](local_meep_mesh_monitor_diagnostics_v0.6.md).

## Recommendation

Do not use the current closed-box, upper-hemibox, or top-plane spectra for
physical interpretation. The next round should either simplify the geometry or
run a higher-resolution local case with a smaller domain and monitor geometry
that avoids the film.
