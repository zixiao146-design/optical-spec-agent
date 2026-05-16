# Validation Boundary

This document states what current tests and diagnostics validate, and what they
do not validate.

Version scope: current public prerelease `v0.9.0rc6`; current `main` development
version `0.9.0rc7.dev0`. The `v0.9.0rc7` tag has not been created, PyPI remains
unpublished, TestPyPI contains the `0.9.0rc6.dev0` development package, and
TestPyPI upload for `0.9.0rc7.dev0` has not been performed.

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
- Production-grade solver-backed validation of Gmsh, ElmerSolver, MPB, or
  Optiland outputs. Gmsh has one narrow optional manual validation report for a
  project/adapter `.geo` artifact path, but that report is not production-grade
  physical validation.
- Production-grade Meep physical validation. Meep has one narrow optional
  manual validation report for a tiny project-owned PyMeep path generated from
  an adapter preview artifact, but that report is not production-grade physical
  validation.
- Production-grade MPB physical validation. MPB has one narrow optional manual
  validation report for a tiny project-owned MPB/PyMeep path generated from an
  adapter preview artifact, but that report is not production-grade physical
  validation. MPB CLI is not required for that report.
- Production-grade Optiland optical validation. Optiland has one narrow
  optional manual validation report for a tiny project-owned Optiland backend
  path generated from an adapter preview artifact, but that report is not
  production-grade optical validation.
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
`scripts/open_solver_validation_preflight.sh` may detect whether open-source
solver commands are available, but availability detection is not solver-backed
validation and does not imply production-grade physical correctness.
Manual validation evidence should be recorded with
`docs/manual_solver_validation_report_template.md`.
The Gmsh optional validation pilot is a manual opt-in path and is not a
production-grade physical validation claim.
The 2026-05-14 Gmsh report in
`validation/gmsh/gmsh_validation_pilot_2026-05-14.md` records that Gmsh
processed the project/adapter `.geo` artifact after explicit opt-in. It does
not make Gmsh part of default pytest, smoke, quality gates, or release
validation.
The Meep optional validation pilot is also a manual opt-in path and is not a
production-grade physical validation claim.
The 2026-05-14 Meep report in
`validation/meep/meep_validation_pilot_2026-05-14.md` records that PyMeep
executed a tiny project-owned validation path after explicit opt-in. It does
not make Meep part of default pytest, smoke, quality gates, CI, or release
validation.
The MPB optional validation pilot is a manual opt-in path and is not a
production-grade physical validation claim.
The 2026-05-14 MPB report in
`validation/mpb/mpb_validation_pilot_2026-05-14.md` records that MPB/PyMeep
executed a tiny project-owned validation path after explicit opt-in. MPB CLI was
not required. It does not make MPB part of default pytest, smoke, quality gates,
CI, or release validation.
The Optiland optional validation pilot is a manual opt-in path and is not a
production-grade optical validation claim.
The 2026-05-14 Optiland report in
`validation/optiland/optiland_validation_pilot_2026-05-14.md` records that
Optiland executed a tiny project-owned backend path after explicit opt-in. It
does not make Optiland part of default pytest, smoke, quality gates, CI, or
release validation.
The Elmer optional validation pilot is a Level-3-ready manual path only.
`scripts/run_optional_elmer_validation.sh` checks ElmerSolver availability in
default mode without executing Elmer. ElmerSolver is not installed locally, no
completed Elmer report exists, the 2026-05-15 package install attempt is
deferred, and Elmer remains Level 2 pending explicit manual validation.

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
