# Open-source Solver Validation Harness

## Purpose

This harness prepares optional manual solver-backed validation without making
external solvers default requirements.

## Current Scope

- Current public prerelease: v0.9.0rc4
- Current main development version: 0.9.0rc5.dev0
- PyPI/TestPyPI: not published / not uploaded
- v0.9.0rc5 tag: not created

## What The Preflight Does

`scripts/open_solver_validation_preflight.sh`:

- detects candidate open-source solver commands and Python-backed solver modules
- reports CLI and Python module availability separately
- writes an optional JSON report when `OSA_SOLVER_PREFLIGHT_JSON` is set
- does not run solvers
- does not create tags or releases
- does not upload packages
- does not require proprietary tools

## Candidate Open-source Solver Families

- Meep: current preview adapter and optional explicit local execution harness.
- MPB: current MVP/scaffold band-structure input preview.
- Gmsh: current MVP/scaffold geometry and mesh artifact preview.
- Elmer: current MVP/scaffold FEM input preview.
- Optiland: current MVP/scaffold optical-design preview.

Meep may be available through `import meep as mp` even when a `meep` CLI command
is absent. MPB may be available through `from meep import mpb` even when an
`mpb` CLI command is absent. Optiland may be available through `import optiland`
even when an `optiland` CLI command is absent. Gmsh is currently detected by
`command -v gmsh`; Elmer is detected by `command -v ElmerSolver`, and
ElmerSolver absence is acceptable for default gates.

Candidate availability does not mean validation was run. An installed solver
does not imply production-grade correctness.
An unavailable solver does not fail default tests. Unavailable solvers also do
not fail smoke, quality gates, or release dry-runs.

The first pilot-ready path is the Gmsh optional validation pilot in
`docs/gmsh_optional_validation_pilot.md` and
`scripts/run_optional_gmsh_validation.sh`. Its default mode only checks
availability and fixture presence; it does not run Gmsh unless explicitly enabled
outside the default gates.

The 2026-05-14 Gmsh opt-in pilot processed a project/adapter-generated `.geo`
artifact and is recorded in
`validation/gmsh/gmsh_validation_pilot_2026-05-14.md`. This is Level 3 optional
manual validation evidence for a narrow artifact path. It is not
production-grade physical validation and not a default dependency.

The 2026-05-14 Meep opt-in pilot generated a Meep preview artifact and executed
a tiny project-owned PyMeep validation path. It is recorded in
`validation/meep/meep_validation_pilot_2026-05-14.md` and documented in
`docs/meep_level3_readiness.md`. This is Level 3 optional manual validation
evidence for a narrow PyMeep path only. It is not production-grade physical
validation and not a default dependency.

The 2026-05-14 MPB opt-in pilot generated an MPB preview artifact and executed
a tiny project-owned MPB/PyMeep validation path through `from meep import mpb`.
It is recorded in `validation/mpb/mpb_validation_pilot_2026-05-14.md` and
documented in `docs/mpb_level3_readiness.md`. This is Level 3 optional manual
validation evidence for a narrow MPB path only. MPB CLI is not required. It is
not production-grade physical validation and not a default dependency.

The 2026-05-14 Optiland opt-in pilot generated an Optiland preview artifact and
executed a tiny project-owned Optiland backend path. It is recorded in
`validation/optiland/optiland_validation_pilot_2026-05-14.md` and documented in
`docs/optiland_level3_readiness.md`. This is Level 3 optional manual validation
evidence for a narrow Optiland path only. It is not production-grade optical
validation and not a default dependency.

## Future Manual Validation Path

Future manual solver validation should follow this pattern:

- enable an explicit environment variable or manual command
- run a solver-specific manual check outside the default gates
- compare high-level diagnostics rather than brittle full-output snapshots
- record the result in a manual validation report
- keep default CI and smoke no-solver

## Non-goals

- no default solver execution
- no production-grade physical validation claim
- no formal convergence proof
- no proprietary solver validation
- no TestPyPI/PyPI upload
- no release creation
