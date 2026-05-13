# Validation Boundary

This document states what current tests and diagnostics validate, and what they
do not validate.

Version scope: current public prerelease `v0.9.0rc3`; current `main`
development version `0.9.0rc4.dev0`. `v0.9.0rc4.dev0` is not a release, the
`v0.9.0rc4` tag has not been created, and PyPI/TestPyPI remain unpublished.
Continue v1.0 readiness engineering and prepare a `v0.9.0rc4` release draft
only when accumulated changes should be published as another RC.

The project is open-source-solver-first. Proprietary solvers are not default
dependencies, and no proprietary license is required for default tests, smoke,
examples, or release validation.

## What current tests validate

- `OpticalSpec` model serialization, schema export, and status-field behavior.
- Rule-based, mock LLM, and hybrid parser behavior for deterministic examples.
- SpecValidator structural completeness and task-aware consistency checks.
- Meep script generation structure, defaults, warnings, and syntax.
- Adapter registry and scaffold generation for Meep, MPB, Gmsh, Elmer, and
  Optiland.
- Workflow plan/run/replay/report artifact structure.
- Offline examples, adapter evidence fixtures, workflow evidence fixtures,
  schema compatibility policy, and failure-mode regression checks.
- v1.0 compatibility policy, validation evidence manifest, optional
  open-source solver validation plan, and examples manifest checks.
- Expanded adapter family evidence for Gmsh, Elmer, MPB, and Optiland local
  scaffold generation.
- Benchmark routing and deterministic mock evaluation.
- Release engineering checks for docs, CLI surface, artifacts, build, and
  smoke install/test behavior.

## What current tests do not validate

- No production-grade physical validation.
- No formal convergence proof.
- Numerical accuracy of external solver results.
- Solver-backed validation of Gmsh, ElmerSolver, MPB, or Optiland outputs.
- Full material model correctness.
- Full CAD, FEM, lens, or mesh prescription correctness.
- Real external LLM model quality.
- Commercial/proprietary solver-backed validation unless explicitly documented
  as manual and non-default.
- Cloud or background orchestration behavior.

## Physical diagnostics status

Diagnostics are sanity/preview checks unless explicitly stated otherwise. They
help expose mesh, flux, execution, and artifact issues, but they do not prove
physical correctness. Meep/default wavelength warnings mean the adapter applied
a conservative local default, not that the resulting simulation is physically
validated.

## External solver validation

External solver validation is optional/manual. Default CI and release smoke do
not require Meep, MPB, Gmsh, Elmer, Optiland, or external LLM providers.
Default tests do not require Meep, MPB, Gmsh, Elmer, Optiland, or external LLM providers.
Optional open-source solver validation is documented in
`docs/open_source_solver_validation_plan.md`; those checks remain manual,
skipped by default, and non-blocking for default smoke/release validation.

## Requirements for production-grade validation

A production-grade validation track would need at least:

- Explicit solver versions and reproducible environments.
- Reference cases with known expected numerical behavior.
- Mesh/resolution convergence studies.
- Material-model validation.
- Boundary/source/monitor validation.
- Human review by a domain expert.
- Clear acceptance tolerances and rollback policy.

Until then, the project remains an auditable spec/scaffold/workflow layer.

## Offline user journey boundary

The offline user journey in `docs/offline_user_journey.md` and `examples/e2e/`
is compatibility evidence for validate, parse, adapter listing, and
`workflow-plan` preview behavior. It does not require network access, external
solvers, external LLM providers, or proprietary optical software. The error
model in `docs/error_model.md` describes deterministic local failures, while
`docs/migration_notes_pre_v1.md` records pre-v1 compatibility boundaries.
