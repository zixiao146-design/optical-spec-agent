# MPB Level-3 Manual Validation Readiness

## Purpose

This document defines what is required to advance the MPB adapter from Level 2
to Level 3 in the adapter maturity model.

## Current Status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- MPB current maturity: Level 3
- Target maturity achieved: Level 3 - Optional manual solver validation
- MPB is not required by default
- MPB is not run by default
- MPB CLI is not required if the `meep.mpb` Python path is available
- Default tests do not require MPB
- Default pytest does not run MPB
- Default quality gates do not require MPB execution
- No production-grade physical validation is claimed

## Level 3 Requirements

- MPB Python availability check: complete
- Fixed input fixture: `examples/specs/mpb_preview.json`
- Generated MPB artifact or minimal project-owned validation script: complete
- Explicit opt-in command: complete
- Manual validation report: `validation/mpb/mpb_validation_pilot_2026-05-14.md`
- MPB/PyMeep version recorded: complete
- Generated artifact recorded: complete
- Observed result recorded: complete
- Limitations recorded: complete
- Release-note claim reviewed: limited claim only

## What Is Not Required For Level 3

- Production-grade physical validation.
- Formal convergence proof.
- Default CI execution.
- Default release gate execution.
- MPB CLI.
- Proprietary solver availability.

## Status Checklist

- Adapter registered: yes
- CLI visible: yes
- Local artifact preview: yes
- Golden/evidence fixture: yes
- Optional manual validation script: yes
- Actual MPB execution recorded: yes, opt-in only
- Manual validation report filled: yes
- Level 3 achieved: yes

## Level 3 Evidence Boundary

This evidence does not claim production-grade physical validation.
This evidence does not claim a formal convergence proof.
This evidence does not validate optical design correctness.
This evidence does not make MPB a default dependency.
This evidence does not require MPB CLI.

The next maturity step is a reproducible solver-backed benchmark with documented
environment assumptions and high-level expected results. That is not yet
achieved.
