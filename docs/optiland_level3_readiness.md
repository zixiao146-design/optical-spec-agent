# Optiland Level-3 Manual Validation Readiness

## Purpose

This document defines what is required to advance the Optiland adapter from
Level 2 to Level 3 in the adapter maturity model.

## Current Status

- Current public prerelease: v0.9.0rc7
- Current main release draft: 0.9.0rc8
- Optiland current maturity: Level 3
- Target maturity achieved: Level 3 - Optional manual backend validation
- Optiland is not required by default
- Optiland is not run by default
- Default tests do not require Optiland execution
- Default pytest does not run Optiland
- Default quality gates do not require Optiland execution
- No production-grade optical validation is claimed

## Level 3 Requirements

- Optiland Python availability check: complete
- Fixed input fixture: `examples/specs/optiland_preview.json`
- Generated Optiland artifact or minimal project-owned validation script: complete
- Explicit opt-in command: complete
- Manual validation report: `validation/optiland/optiland_validation_pilot_2026-05-14.md`
- Optiland version recorded: complete
- Generated artifact recorded: complete
- Observed result recorded: complete
- Limitations recorded: complete
- Release-note claim reviewed: limited claim only

## What Is Not Required For Level 3

- Production-grade optical validation.
- Formal convergence proof.
- Default CI execution.
- Default release gate execution.
- Proprietary solver availability.

## Status Checklist

- Adapter registered: yes
- CLI visible: yes
- Local artifact preview: yes
- Golden/evidence fixture: yes
- Optional manual validation script: yes
- Actual Optiland execution recorded: yes, opt-in only
- Manual validation report filled: yes
- Level 3 achieved: yes

## Level 3 Evidence Boundary

This evidence does not claim production-grade optical validation.
This evidence does not claim a formal convergence proof.
This evidence does not validate optical design correctness.
This evidence does not make Optiland a default dependency.

The next maturity step is a reproducible backend-backed benchmark with
documented environment assumptions and high-level expected results. That is not
yet achieved.
