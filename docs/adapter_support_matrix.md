# Adapter Support Matrix

Version scope: current `main` release draft version `0.9.0rc3` after the
verified public `v0.9.0rc2` pre-release. The `v0.9.0rc3` tag has not been
created yet.

Adapter outputs are local generated artifacts. They do not run external solvers
by default and do not claim production-grade physical validation.

| Adapter | Status | Generated artifact | External solver required to generate? | External solver run by default? | Test coverage | v1.0 readiness |
|---|---|---|---|---|---|---|
| `meep` | `preview` / research-preview | Python script | No | No | Unit, CLI, smoke, defaults, diagnostics | Needs clearer production-validation boundary |
| `mpb` | MVP scaffold | Python scaffold | No | No | Unit, CLI, workflow, benchmark | Needs richer periodic geometry schema |
| `gmsh` | MVP scaffold | `.geo` scaffold | No | No | Unit, CLI, workflow, benchmark | Needs richer CAD/mesh schema |
| `elmer` | MVP scaffold | `.sif` scaffold | No | No | Unit, CLI, workflow, benchmark | Needs explicit mesh and FEM boundary contract |
| `optiland` | MVP scaffold | Python scaffold | No | No | Unit, CLI, workflow, benchmark | Needs lens prescription/schema extension |

## Registry contract

The adapter registry currently exposes:

- `meep`
- `mpb`
- `gmsh`
- `elmer`
- `optiland`

`adapter-list --json` must include the same adapter names and metadata fields:
`tool_name`, `display_name`, `solver_family`, `output_language`,
`output_extension`, `supported_solver_methods`, `supported_physical_systems`,
`current_status`, `limitations`, and `consumed_fields`.

## Support boundary

- External solvers are not run by default.
- External solver installation is not required for default tests.
- MPB/Gmsh/Elmer/Optiland outputs are scaffold/MVP unless separately validated.
- Meep execution remains optional/local and must be explicitly requested.
- Adapter warnings and defaults are part of the auditable output contract.
- Physical correctness is not claimed as production-grade.
