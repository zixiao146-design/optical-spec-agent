# Gmsh Optional Validation Pilot

## Purpose

This pilot defines a safe optional path for manually validating the Gmsh adapter
without making Gmsh a default dependency.

## Current Scope

- Current public prerelease: v0.9.0rc4
- Current main development version: 0.9.0rc5.dev0
- Adapter: `gmsh`
- Default tests do not run Gmsh.
- Default smoke does not run Gmsh.
- Release validation does not require Gmsh.
- No production-grade physical validation is claimed.
- Current pilot status: opt-in validation passed on 2026-05-14 for a narrow
  project/adapter `.geo` artifact path.
- Evidence report: `validation/gmsh/gmsh_validation_pilot_2026-05-14.md`.
- Level 3 readiness: `docs/gmsh_level3_readiness.md`.

## Input Fixture

The default local evidence path uses:

- `examples/specs/gmsh_preview.json`
- `tests/fixtures/adapter_golden/gmsh/`

These fixtures are for local `.geo` preview evidence. They are not solver-backed
validation by themselves.

The 2026-05-14 opt-in pilot generated
`/tmp/osa-gmsh-validation-output/gmsh_preview.geo` from
`examples/specs/gmsh_preview.json`, then ran Gmsh against that generated
artifact. The generated mesh output stayed in `/tmp` and is not committed.

## What Is Validated By Default

Default tests validate:

- adapter registration
- `adapter-list` visibility
- local `.geo` preview artifact generation
- expected fragments and metadata
- no external solver execution

## Optional Manual Validation Path

The future optional path is:

1. Check Gmsh availability.
2. Generate a local `.geo` preview artifact.
3. Manually run Gmsh only if the maintainer explicitly opts in.
4. Record the result using
   `docs/manual_solver_validation_reports/gmsh_validation_pilot_template.md`.
5. Do not use the result to claim production-grade validation unless scope is
   separately reviewed.

DO NOT RUN BY DEFAULT.

## Explicit Opt-in

Optional Gmsh execution may only be enabled with an explicit environment
variable:

```bash
OSA_RUN_OPTIONAL_GMSH_VALIDATION=1
```

Default: `OSA_RUN_OPTIONAL_GMSH_VALIDATION` is unset, so no Gmsh command is
executed.

## Non-goals

- No automatic Gmsh execution.
- No CI Gmsh requirement.
- No release gate Gmsh requirement.
- No production-grade validation claim.
- No formal convergence proof.
- No proprietary solver dependency.
- No default pytest, smoke, quality gate, or release-gate dependency on Gmsh.
