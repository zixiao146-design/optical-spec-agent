# Elmer Optional Validation Pilot

## Purpose

This pilot defines a safe optional path for manually validating the Elmer
adapter without making Elmer a default dependency.

## Current Scope

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- Adapter: elmer
- ElmerSolver is not installed locally
- 2026-05-15 install attempt was deferred because a safe binary/package route
  was not available through the checked conda-forge or Homebrew paths.
- Default tests do not run Elmer
- Default smoke does not run Elmer
- Release validation does not require Elmer
- No production-grade physical validation is claimed
- No formal convergence proof is claimed

## Input Fixture

- `examples/specs/elmer_preview.json`
- `tests/fixtures/adapter_golden/elmer/`

## What Is Validated By Default

Default checks cover only:

- adapter registration
- adapter-list visibility
- local Elmer `.sif` preview artifact generation
- expected fragments and metadata
- diagnostics
- no external solver execution

## Optional Manual Validation Path

DO NOT RUN BY DEFAULT.

Future manual validation may:

1. Install Elmer manually through a maintainable binary/package route.
2. Check `ElmerSolver` availability.
3. Generate a local `.sif` preview artifact.
4. Run `ElmerSolver` only after explicit maintainer opt-in.
5. Record the result using the manual validation report template.
6. Avoid production-grade validation claims unless scope is separately reviewed.

## Explicit Opt-in

Optional Elmer execution may only be enabled with:

```bash
OSA_RUN_OPTIONAL_ELMER_VALIDATION=1
```

Default:

`OSA_RUN_OPTIONAL_ELMER_VALIDATION` is unset, so no `ElmerSolver` command is
executed.

The 2026-05-15 install attempt is recorded in
`validation/elmer/elmer_install_deferred_2026-05-15.md`; it is not a completed
manual validation report.

## Non-goals

- No automatic Elmer execution.
- No CI Elmer requirement.
- No release gate Elmer requirement.
- No production-grade validation claim.
- No formal convergence proof.
- No proprietary solver dependency.
