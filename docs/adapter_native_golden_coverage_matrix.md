# Adapter-Native Golden Coverage Matrix

This page summarizes the local adapter-native golden preview cases that lock
source, monitor, observable, and adapter mapping semantics. These checks are
preview/design-assist evidence only. They do not execute Meep, MPB, Gmsh,
ElmerSolver, Optiland, external LLMs, uploads, tags, or releases.
The checker does not execute external solvers or produce real monitor results.
No production-grade physical validation is claimed. No formal convergence proof
is claimed.

## Coverage Matrix

| Adapter | Golden case | Source model | Monitor model | Observable diagnostics | Native mapping terms | Real solver required? | Solver executed? | Preview-only? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Meep | `meep_nanoparticle_scattering` | plane wave, 400-900 nm broadband, linear x | scattering spectrum | scattering/extinction spectrum | `mp.Source`, broadband/GaussianSource metadata, flux/DFT monitor metadata | yes | no | yes |
| MPB | `mpb_photonic_crystal_band` | eigenmode/band context | band structure | band structure, mode frequency | k-points, band frequencies, eigenmode context | yes | no | yes |
| Gmsh | `gmsh_mesh_region` | source metadata only | mesh region / physical group | mesh region | physical groups, mesh-region annotations | yes for real optical result outside Gmsh | no | yes |
| Elmer | `elmer_fem_boundary_source` | mode source placeholder | mode overlap/output placeholder | mode overlap, mode frequency | boundary condition placeholder, body force/source section, ResultOutputSolver placeholder | yes | no | yes |
| Optiland | `optiland_lens_image_plane` | ray bundle/object metadata | image plane | image plane, ray fan | ray bundle, image plane, focal spot, ray fan | yes | no | yes |

## Strict Metadata Diff

Every golden case includes `expected_metadata.json`. The checker compares:

- adapter name
- source type
- monitor type
- observable kinds
- required native terms
- `requires_solver_for_real_result`
- `external_solver_executed=false`
- `preview_only=true`
- no production-grade validation claim
- no formal convergence proof claim

The checker also preserves the older expected-fragment checks so maintainers
can catch both structured metadata drift and accidental wording loss.

Run:

```bash
python scripts/check_adapter_native_golden.py
```

The script prints `ADAPTER NATIVE METADATA DIFF PASSED` when the strict
metadata checks pass.

## Backend Capability Report

The same coverage data is exposed through:

- `GET /api/adapter-native-golden-coverage`
- `GET /api/backend-capability-report`
- `scripts/generate_backend_capability_report.py`

The report records which adapters are covered, whether any registered adapter
is missing coverage, and whether every golden case remains preview-only and
solver-free.

## Limitations

Golden coverage proves stable preview semantics, not physical correctness. Real
flux, field, band, FEM, mesh-coupled, or ray-trace results require explicit
solver execution and independent validation. This project does not claim
production-grade physical validation or formal convergence proof from these
golden cases.
