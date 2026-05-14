# Open-source Solver Validation Plan

## Purpose

This plan defines how optional solver-backed validation may be added later for
open-source tools without making external solvers default release blockers.

The default path remains local artifact preview, offline evidence, and no
external solver execution by default.

The optional availability preflight is
`scripts/open_solver_validation_preflight.sh`. It detects candidate solver
commands and can write an availability JSON report, but it does not execute
Meep, MPB, Gmsh, Elmer, Optiland, or any other solver.

## Candidate open-source solver families

- Meep: current research-preview adapter and optional explicit local execution
  harness.
- Gmsh: current MVP/scaffold geometry and mesh artifact preview.
- Elmer: current MVP/scaffold FEM input preview.
- MPB: current MVP/scaffold band-structure input preview.
- Optiland: current MVP/scaffold optical design preview; solver-backed
  validation is not claimed and depends on future schema maturity.

## Manual validation path

Future optional solver-backed validation should follow this pattern:

- User installs the solver manually.
- `scripts/open_solver_validation_preflight.sh` records availability only.
- An environment variable enables solver-backed validation.
- Tests are skipped by default unless enabled.
- Generated artifacts are compared against expected high-level diagnostics.
- Failures do not block default smoke unless explicitly configured.
- Release notes state whether solver-backed validation was actually run.
- Manual results are recorded with
  `docs/manual_solver_validation_report_template.md`.

The first pilot-ready candidate is Gmsh. Its opt-in guide is
`docs/gmsh_optional_validation_pilot.md`, and its default script path is
`scripts/run_optional_gmsh_validation.sh`. Default mode does not run Gmsh; it
only checks availability, fixture presence, and report metadata.

## Required guardrails

- No external solver is run by default.
- No proprietary license required.
- No network required by default.
- No production-grade claim unless evidence exists.
- Release notes must state whether solver-backed validation was actually run.
- Solver-backed checks must remain separate from default package, CLI, docs, and
  smoke gates unless maintainers explicitly approve a narrower release gate.

## Future optional test naming

- Tests should use `solver_optional`, `external_solver`, and
  `manual_validation` markers, with optional solver-specific markers if needed.
- Tests should be skipped unless an environment variable is set.
- Tests should not be part of default `pytest`.
- Tests should not be part of default `scripts/smoke_release.sh`.
- Tests should not require proprietary tools or proprietary licenses.
- Marker policy is documented in `docs/pytest_marker_policy.md`.
