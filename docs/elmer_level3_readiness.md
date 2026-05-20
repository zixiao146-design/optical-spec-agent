# Elmer Level-3 Manual Validation Readiness

## Purpose

This document defines what is required to advance the Elmer adapter from Level 2
to Level 3 in the adapter maturity model.

## Current Status

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- Elmer current maturity: Level 2
- Target next maturity: Level 3 - Optional manual solver validation
- ElmerSolver is not installed locally
- 2026-05-15 install attempt: deferred because `elmerfem` and `elmer` were not
  available from the current conda-forge `osx-arm64` channels, and Homebrew had
  no `elmer` or `elmerfem` formula/cask.
- Elmer is not required by default
- Elmer is not run by default
- Default tests do not require Elmer
- Default quality gates do not require Elmer execution
- No production-grade physical validation is claimed

## Level 3 Requirements

- ElmerSolver availability check.
- Fixed input fixture.
- Generated `.sif` artifact.
- Explicit opt-in command.
- Manual validation report.
- Elmer version recorded.
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

- Adapter registered: yes.
- CLI visible: yes.
- Local artifact preview: yes.
- Golden/evidence fixture: yes.
- Optional manual validation script: yes, `scripts/run_optional_elmer_validation.sh`.
- Actual Elmer execution recorded: no.
- Manual validation report filled: no.
- Level 3 achieved: no, pending ElmerSolver installation and explicit opt-in validation.
- Deferred install record: `validation/elmer/elmer_install_deferred_2026-05-15.md`.

## Readiness Boundary

Elmer is Level-3-ready but remains Level 2 until an explicit manual validation
run records a completed report. `ElmerSolver` unavailable is non-blocking for
default tests, smoke, quality gates, release dry-runs, and documentation checks.
The 2026-05-15 package-manager install attempt is recorded as deferred, not as
solver-backed validation evidence.
This readiness state does not make Elmer a default dependency, does not claim
production-grade physical validation, and does not claim a formal convergence
proof. In short: it does not claim production-grade physical validation and
does not claim a formal convergence proof.
