# Quality Gates

## Purpose

This document defines repeatable local quality gates for v1.0 readiness and
future release-candidate preparation.

## Current Scope

- Current public prerelease: v0.9.0rc5
- Current main release draft: `0.9.0rc6`
- PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0
- v0.9.0rc6 tag: not created

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
Automatic GitHub CI is intentionally kept lightweight in `ci.yml`; benchmark
and extended-test workflows are manual-only so push/PR checks do not depend on
longer report-generation paths.

## Gate Components

- TestPyPI no-upload preflight.
- Open-source solver validation preflight, availability detection only.
- Gmsh optional validation pilot default preflight, no Gmsh execution.
- Meep optional validation pilot default preflight, no Meep execution.
- MPB optional validation pilot default preflight, no MPB execution and no MPB
  CLI requirement.
- Optiland optional validation pilot default preflight, no Optiland execution.
- Elmer optional validation pilot default preflight, no Elmer execution and
  ElmerSolver unavailable is non-blocking.
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
- No solver execution in the open-source solver preflight.
- No Gmsh execution in the Gmsh optional validation pilot default preflight.
- The recorded Gmsh Level 3 report is optional manual evidence only and is not
  part of the default quality gate.
- No Meep execution in the Meep optional validation pilot default preflight.
- The recorded Meep Level 3 report is optional manual evidence only and is not
  part of the default quality gate.
- No MPB execution in the MPB optional validation pilot default preflight.
- The recorded MPB Level 3 report is optional manual evidence only, does not
  require MPB CLI, and is not part of the default quality gate.
- No Optiland execution in the Optiland optional validation pilot default
  preflight.
- The recorded Optiland Level 3 report is optional manual evidence only and is
  not part of the default quality gate.
- No Elmer execution in the Elmer optional validation pilot default preflight.
- Elmer remains Level 2 with Level-3-ready documentation until ElmerSolver is
  installed and an explicit opt-in validation run records a report. The
  2026-05-15 package-manager install attempt is recorded as deferred.
- No external LLM by default.
- No proprietary solver by default.
- No token is required for the default local quality gate.

## When To Run

- Before release draft.
- Before tag creation.
- Before TestPyPI approval decision.
- After major docs, contract, schema, adapter, or workflow changes.
- Before changing release automation or CI workflow behavior.
- Before considering optional manual open-source solver validation.
- Before considering the Gmsh optional validation pilot with explicit opt-in.
- Before considering the MPB optional validation pilot with explicit opt-in.
- Before considering the Optiland optional validation pilot with explicit
  opt-in.
- Before considering the Elmer optional validation pilot with explicit opt-in.
