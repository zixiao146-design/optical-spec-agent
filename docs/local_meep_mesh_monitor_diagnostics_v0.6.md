# Local Meep Mesh / Monitor Diagnostics v0.6

This document records local/manual mesh and monitor-geometry diagnostics for the
current v0.6 library-Au physical candidate. It is not production validation and
is not part of ordinary CI.

## Why This Diagnostic Exists

The v0.6 physical candidate is execution-stable, and the candidate hardening
matrix completed without NaN/Inf in the CSV outputs. However, spectrum
consistency metrics showed a near-zero baseline flux, and observable diagnostics
showed that the original closed flux box intersects the film.

The core case has a `5 nm` SiO2 gap. The current candidate uses
`resolution=12 px/um`, so the grid size is approximately `83.33 nm`. That means
the `5 nm` gap is represented by only about `0.06` grid cells. This is severely
under-resolved and blocks physical interpretation.

## Mesh Sanity

The research-preview script now writes `mesh_diagnostics` into
`postprocess_results.json`.

For the latest local observable diagnostics run:

| Quantity | Value |
|----------|-------|
| `resolution_px_per_um` | `12` |
| `grid_size_nm` | `83.3333` |
| `gap_thickness_nm` | `5.0` |
| `gap_cells` | `0.06` |
| `particle_radius_nm` | `40.0` |
| `particle_radius_cells` | `0.48` |
| `film_thickness_nm` | `100.0` |
| `film_thickness_cells` | `1.2` |
| `gap_under_resolved` | `true` |
| `min_recommended_gap_cells` | `5.0` |
| `recommended_resolution_for_5_gap_cells` | `1000.0 px/um` |

Interpretation:

- The current candidate is stable as an execution profile.
- The current candidate is not physically resolved.
- Any spectrum from this profile is diagnostic only.
- A `5 nm` gap needs much higher resolution for physical interpretation.

## Monitor Presets

The research-preview adapter now supports these monitor/flux presets:

| Preset | Meaning | Production interpretation |
|--------|---------|---------------------------|
| `closed_box` | Existing six-surface closed box around the particle | Diagnostic until geometry is fixed |
| `gap_clearance_box` | Attempts to place the lower plane inside the gap | Infeasible when the gap is under-resolved |
| `upper_hemibox` | Open upper box that avoids the film | Diagnostic only |
| `top_plane` | Single upward z-plane | Diagnostic only |
| `single_plane` | Legacy single z-plane diagnostic | Diagnostic only |

If `gap_clearance_box` is requested but the gap has less than about one grid
cell, the generated script records `gap_clearance_box_feasible=false` and falls
back to `top_plane`. This avoids silently generating an invalid monitor.

## Local Run

Command:

```bash
python scripts/local_meep_observable_diagnostics.py --timeout 900
```

Environment:

- Meep command: `micromamba run -n meep python -c "import meep"`
- Matrix run ID: `observable-diagnostics-20260501-045806-82b41774`
- Artifact root: `runs/observable-diagnostics/observable-diagnostics-20260501-045806-82b41774/`

The artifact directory is local evidence only and is not committed to the repo.

## Results

| Case | Effective monitor | Success | Intersects film | Gap clearance feasible | `max_abs_flux` | `integrated_abs_flux` | Near zero |
|------|-------------------|---------|-----------------|------------------------|----------------|-----------------------|-----------|
| `closed-box-baseline` | `closed_box` | yes | yes | false | `1.36e-26` | `3.10e-24` | yes |
| `gap-clearance-box` | `top_plane` fallback | yes | no | false | `1.11e-27` | `2.56e-25` | yes |
| `upper-hemibox` | `upper_hemibox` | yes | no | false | `5.98e-27` | `1.37e-24` | yes |
| `top-plane` | `top_plane` | yes | no | false | `1.11e-27` | `2.56e-25` | yes |
| `single-plane` | `single_plane` | yes | no | false | `1.11e-27` | `2.56e-25` | yes |

All supported cases generated the expected execution artifacts and optional
`flux_surfaces.csv`.

## Interpretation

- `closed_box` remains the strongest of the tested signals, but it intersects
  the film and is hard to interpret.
- `gap_clearance_box` is infeasible at the current mesh because the `5 nm` gap
  is far below one grid cell.
- `upper_hemibox` avoids the film and gives a stronger signal than `top_plane`,
  but it is still near zero and not a closed scattering cross-section.
- `top_plane` and `single_plane` are weaker than `closed_box`.
- Per-surface flux diagnostics still do not point to strong cancellation as the
  dominant cause of the near-zero observable.

## Recommendation

Do not expand the convergence matrix using the current geometry. The next v0.6
step should choose one of two paths:

- Reduce geometry difficulty for physical validation, for example by using a
  larger gap or a simpler domain to establish a nonzero observable first.
- Run a high-resolution local case with a smaller domain and a monitor that
  avoids the film, then repeat mesh/monitor diagnostics before convergence.

The current execution-stable candidate should remain labeled as diagnostic
until the gap and monitor geometry are physically resolved.
