# Pytest Marker Policy

## Purpose

Default tests must remain offline and no-solver. Optional external validation
markers exist only to make future manual checks explicit and skippable.

## Current Defaults

- Current public prerelease: v0.9.0rc4
- Current main development version: 0.9.0rc5.dev0
- Default `pytest` remains no-solver.
- Default smoke and quality gates do not execute external solvers.
- External LLM access is not required by default.
- Proprietary solver tests are not default tests.

## Marker Meanings

- `solver_optional`: optional open-source solver validation, skipped by default
  unless explicitly enabled by a maintainer.
- `external_solver`: requires an external solver installation; not part of the
  default test contract.
- `manual_validation`: manual validation only; not part of default CI, smoke, or
  release dry-runs.
- `external_llm`: requires an external LLM provider or network access; not part
  of the default test contract.

## Selection Guidance

Run default tests normally:

```bash
python -m pytest
```

Optional solver tests, if added later, should require an explicit marker
selection and an explicit environment variable. They should be skipped by
default when the solver or opt-in variable is unavailable.

The Gmsh optional validation pilot is guarded by
`OSA_RUN_OPTIONAL_GMSH_VALIDATION=1`. Default tests and quality gates must not
set that variable.

The Meep optional validation pilot is guarded by
`OSA_RUN_OPTIONAL_MEEP_VALIDATION=1`. Default tests and quality gates must not
set that variable.

The MPB optional validation pilot is guarded by
`OSA_RUN_OPTIONAL_MPB_VALIDATION=1`. Default tests and quality gates must not
set that variable, and default tests must not require an MPB CLI command.

The Optiland optional validation pilot is guarded by
`OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1`. Default tests and quality gates must
not set that variable.

The Elmer optional validation pilot is guarded by
`OSA_RUN_OPTIONAL_ELMER_VALIDATION=1`. Default tests and quality gates must not
set that variable, and default tests must not require ElmerSolver.

## Guardrails

- Do not make external solvers a default dependency.
- Do not make external LLM providers a default dependency.
- Do not require proprietary solvers by default.
- Do not use optional solver markers to claim production-grade physical
  validation.
