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

## When To Run

- Before release draft.
- Before tag creation.
- Before TestPyPI approval decision.
- After major docs, contract, schema, adapter, or workflow changes.
