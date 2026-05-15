# Meep Level-3 Manual Validation Readiness

## Purpose

This document defines what is required to advance the Meep adapter from Level 2
to Level 3 in the adapter maturity model.

## Current Status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- Meep current maturity: Level 3 - Optional manual solver validation
- Target next maturity: Level 4 - Reproducible solver-backed benchmark
- Meep is not required by default.
- Meep is not run by default.
- Default tests do not require Meep.
- Default quality gates do not require Meep execution.
- No production-grade physical validation is claimed.

## Level 3 Requirements

- PyMeep availability check.
- Fixed input fixture.
- Generated Meep artifact or minimal project-owned validation script.
- Explicit opt-in command.
- Manual validation report.
- Meep version recorded.
- Generated artifact recorded.
- Observed result recorded.
- Limitations recorded.
- Release-note claim reviewed.

## What Is Not Required For Level 3

- Production-grade physical validation.
- Formal convergence proof.
- Default CI execution.
- Default release gate execution.
- Proprietary solver availability.

## Status Checklist

- Adapter registered: yes
- CLI visible: yes
- Local artifact preview: yes
- Golden/evidence fixture: yes
- Optional manual validation script: added in this task
- Actual Meep execution recorded: yes, only for the 2026-05-14 explicit opt-in pilot
- Manual validation report filled: yes, `validation/meep/meep_validation_pilot_2026-05-14.md`
- Level 3 achieved: yes, only for this narrow optional manual validation path

## Recorded Pilot

- Date: 2026-05-14
- Evidence report: `validation/meep/meep_validation_pilot_2026-05-14.md`
- Python executable: `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`
- Solver version: Meep / PyMeep 1.33.0
- Input fixture: `examples/specs/missing_wavelength_meep_preview.json`
- Generated artifact: `/tmp/osa-meep-validation-output/meep_preview.py`
- Output artifact: `/tmp/osa-meep-validation-output/meep_validation_result.json`
- Passed: yes
- Level 3 achieved: yes

## Boundaries

- Default pytest does not run Meep.
- Default smoke does not run Meep.
- Default quality gates do not execute Meep.
- Release validation does not require Meep.
- This evidence does not claim production-grade physical validation.
- This evidence does not claim a formal convergence proof.
- This evidence does not validate optical design correctness.
- Meep remains an optional open-source solver, not a default dependency.
