# Meep Optional Validation Pilot

## Purpose

This pilot defines a safe optional path for manually validating the Meep adapter
without making Meep a default dependency.

## Current Scope

- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- Adapter: meep
- Default tests do not run Meep.
- Default smoke does not run Meep.
- Release validation does not require Meep.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.

## Current Pilot Status

The 2026-05-14 opt-in pilot succeeded and is recorded in
`validation/meep/meep_validation_pilot_2026-05-14.md`. The pilot generated a
local Meep preview artifact from
`examples/specs/missing_wavelength_meep_preview.json`, then ran a tiny
project-owned PyMeep validation path from `/tmp`. This is Level 3 evidence only
for the optional manual validation path.

## Input Fixture

- `examples/specs/missing_wavelength_meep_preview.json`
- `tests/fixtures/adapter_golden/meep_missing_wavelength_expected_fragments.txt`

## What Is Validated By Default

Default checks cover only:

- Adapter registration.
- Adapter-list visibility.
- Local Meep script / preview artifact generation.
- Expected fragments / metadata.
- Diagnostics.
- No external solver execution.

## Optional Manual Validation Path

DO NOT RUN BY DEFAULT.

1. Check PyMeep availability.
2. Generate a local Meep script / minimal validation script.
3. Manually run PyMeep only if the maintainer explicitly opts in.
4. Record the result using the manual solver validation report template.
5. Do not use the result to claim production-grade validation unless scope is
   reviewed.

## Explicit Opt-in

Optional Meep execution may only be enabled with:

```bash
OSA_RUN_OPTIONAL_MEEP_VALIDATION=1
```

Default: `OSA_RUN_OPTIONAL_MEEP_VALIDATION` is unset, so no Meep simulation is
executed.

## Non-goals

- No automatic Meep execution.
- No CI Meep requirement.
- No release gate Meep requirement.
- No production-grade validation claim.
- No formal convergence proof.
- No proprietary solver dependency.
