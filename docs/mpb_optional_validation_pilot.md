# MPB Optional Validation Pilot

## Purpose

This pilot defines a safe optional path for manually validating the MPB adapter
without making MPB a default dependency.

## Current Scope

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- Adapter: mpb
- MPB Python path is supported through `from meep import mpb`
- MPB CLI is not required
- Default tests do not run MPB
- Default smoke does not run MPB
- Release validation does not require MPB
- No production-grade physical validation is claimed
- No formal convergence proof is claimed

## Input Fixture

- `examples/specs/mpb_preview.json`
- `tests/fixtures/adapter_golden/mpb/`

## What Is Validated By Default

Default project checks only validate:

- adapter registration
- `adapter-list` visibility
- local MPB scaffold / preview artifact generation
- expected fragments and metadata
- diagnostics
- no external solver execution

## Optional Manual Validation Path

DO NOT RUN BY DEFAULT:

1. Check MPB Python availability through `from meep import mpb`.
2. Generate a local MPB script or minimal validation path.
3. Manually run MPB only if a maintainer explicitly opts in.
4. Record the result using the manual solver validation report template.
5. Do not use the result to claim production-grade validation unless scope is
   reviewed separately.

## Explicit Opt-in

Optional MPB execution may only be enabled with:

```bash
OSA_RUN_OPTIONAL_MPB_VALIDATION=1
```

Default: `OSA_RUN_OPTIONAL_MPB_VALIDATION` is unset, so no MPB solver path is
executed.

## 2026-05-14 Pilot Status

The 2026-05-14 opt-in pilot generated the project MPB adapter scaffold from
`examples/specs/mpb_preview.json`, then ran a tiny project-owned MPB validation
path through `from meep import mpb`. The recorded report is
`validation/mpb/mpb_validation_pilot_2026-05-14.md`.

This supports only Level 3 optional manual validation evidence for a narrow
MPB/PyMeep path. It does not require MPB CLI, does not make MPB a default
dependency, does not claim production-grade physical validation, and does not
claim a formal convergence proof.

## Non-goals

- No automatic MPB execution.
- No CI MPB requirement.
- No release gate MPB requirement.
- No MPB CLI requirement.
- No production-grade validation claim.
- No formal convergence proof.
- No proprietary solver dependency.
