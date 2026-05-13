# Quality Gates

## Purpose

This document defines repeatable local quality gates for v1.0 readiness and
future release-candidate preparation.

## Current Scope

- Current public prerelease: v0.9.0rc4
- Current main development version: 0.9.0rc5.dev0
- PyPI/TestPyPI: not published / not uploaded
- v0.9.0rc5 tag: not created

## One-command Local Gate

```bash
./scripts/run_quality_gates.sh
```

Makefile convenience target:

```bash
make quality
```

CI parity and workflow boundaries are documented in
[`ci_quality_gate_parity.md`](ci_quality_gate_parity.md). Release dry-runs are
documented in [`release_dry_run_operations.md`](release_dry_run_operations.md).

## Gate Components

- TestPyPI no-upload preflight.
- `smoke_release.sh`.
- Wheel smoke.
- `pytest`.
- `python -m build`.
- `make check`.
- Documented CLI examples.
- E2E workflow example.

## Safety Guarantees

- No upload.
- No tag creation.
- No GitHub release creation.
- No external solver by default.
- No external LLM by default.
- No proprietary solver by default.
- No token is required for the default local quality gate.

## When To Run

- Before release draft.
- Before tag creation.
- Before TestPyPI approval decision.
- After major docs, contract, schema, adapter, or workflow changes.
- Before changing release automation or CI workflow behavior.
