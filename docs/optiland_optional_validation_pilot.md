# Optiland Optional Validation Pilot

## Purpose

This pilot defines a safe optional path for manually validating the Optiland
adapter without making Optiland a default dependency.

## Current Scope

- Current public prerelease: v0.9.0rc7
- Current main release draft: 0.9.0rc8
- Adapter: optiland
- Optiland Python import is available in the local solver environment
- Default tests do not run Optiland
- Default smoke does not run Optiland
- Release validation does not require Optiland
- No production-grade optical validation is claimed
- No formal convergence proof is claimed

## Input Fixture

- `examples/specs/optiland_preview.json`
- `tests/fixtures/adapter_golden/optiland/`

## What Is Validated By Default

Default project checks only validate:

- adapter registration
- `adapter-list` visibility
- local Optiland scaffold / preview artifact generation
- expected fragments and metadata
- diagnostics
- no external backend execution

## Optional Manual Validation Path

DO NOT RUN BY DEFAULT:

1. Check Optiland Python availability.
2. Generate a local Optiland scaffold or minimal validation path.
3. Manually run Optiland only if a maintainer explicitly opts in.
4. Record the result using the manual validation report template.
5. Do not use the result to claim production-grade validation unless scope is
   reviewed separately.

## Explicit Opt-in

Optional Optiland execution may only be enabled with:

```bash
OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1
```

Default: `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION` is unset, so no Optiland backend
path is executed.

## 2026-05-14 Pilot Status

The 2026-05-14 opt-in pilot generated the project Optiland adapter scaffold
from `examples/specs/optiland_preview.json`, then ran a tiny project-owned
Optiland validation path. The recorded report is
`validation/optiland/optiland_validation_pilot_2026-05-14.md`.

This supports only Level 3 optional manual validation evidence for a narrow
Optiland backend path. It does not make Optiland a default dependency, does not
claim production-grade optical validation, and does not claim a formal
convergence proof.

## Non-goals

- No automatic Optiland execution.
- No CI Optiland requirement.
- No release gate Optiland requirement.
- No production-grade validation claim.
- No formal convergence proof.
- No proprietary solver dependency.
