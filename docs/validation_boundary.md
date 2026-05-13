# Validation Boundary

This document states what current tests and diagnostics validate, and what they
do not validate.

Version scope: current `main` development version `0.9.0rc3.dev0` after the
verified public `v0.9.0rc2` pre-release. `0.9.0rc3.dev0` is not a release.

## What current tests validate

- `OpticalSpec` model serialization, schema export, and status-field behavior.
- Rule-based, mock LLM, and hybrid parser behavior for deterministic examples.
- SpecValidator structural completeness and task-aware consistency checks.
- Meep script generation structure, defaults, warnings, and syntax.
- Adapter registry and scaffold generation for Meep, MPB, Gmsh, Elmer, and
  Optiland.
- Workflow plan/run/replay/report artifact structure.
- Benchmark routing and deterministic mock evaluation.
- Release engineering checks for docs, CLI surface, artifacts, build, and
  smoke install/test behavior.

## What current tests do not validate

- No production-grade physical validation.
- No formal convergence proof.
- Numerical accuracy of external solver results.
- Full material model correctness.
- Full CAD, FEM, lens, or mesh prescription correctness.
- Real external LLM model quality.
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
