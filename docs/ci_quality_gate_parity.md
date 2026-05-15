# CI and Quality Gate Parity

## Purpose

This document maps local quality gates to CI and release-dry-run expectations.
It keeps the default operational path no-upload, no-release, no-tag, and
independent of external solvers, external LLM providers, or proprietary optical
software.

## Current Status

- Current public prerelease: v0.9.0rc4
- Current main development version: 0.9.0rc5.dev0
- PyPI/TestPyPI: not published / not uploaded
- v0.9.0rc5 tag: not created
- TestPyPI upload approval: pending
- Upload command authorized: no
- PyPI publication approval: not granted

## Local Quality Gate

The local one-command gate is:

```bash
./scripts/run_quality_gates.sh
```

It is expected to cover:

- TestPyPI no-upload preflight
- open-source solver availability preflight without solver execution
- Gmsh optional validation pilot default preflight without Gmsh execution
- Meep optional validation pilot default preflight without Meep execution
- MPB optional validation pilot default preflight without MPB execution or MPB
  CLI requirement
- Optiland optional validation pilot default preflight without Optiland execution
- Elmer optional validation pilot default preflight without Elmer execution;
  ElmerSolver unavailable is non-blocking
- `smoke_release.sh`
- wheel smoke
- `pytest`
- `python -m build`
- `make check`
- documented CLI examples
- E2E workflow example

The script prints `NO UPLOAD PERFORMED`, `NO TAG CREATED`, and
`NO RELEASE CREATED` as part of its summary.

## CI Parity Expectations

CI should cover the same risk classes as the local quality gate, while keeping
individual jobs shorter where appropriate:

- install the package with test extras
- run `pytest`
- run build and metadata checks
- run documented CLI examples
- run docs, contract, and release-readiness checks
- never upload PyPI/TestPyPI
- never create tags or GitHub releases from default CI
- never require external solver, external LLM, or proprietary optical software
- optional solver availability checks may run, but solver commands must not be
  executed by default CI
- default CI must not set `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1`
- recorded Gmsh Level 3 evidence remains optional/manual and must not become a
  default CI requirement
- recorded Meep Level 3 evidence remains optional/manual and must not become a
  default CI requirement
- recorded MPB Level 3 evidence remains optional/manual and must not become a
  default CI requirement
- recorded Optiland Level 3 evidence remains optional/manual and must not
  become a default CI requirement
- Elmer Level-3-ready checks remain no-execution by default and must not require
  ElmerSolver in default CI; the 2026-05-15 package-manager install attempt is
  recorded as deferred rather than validation evidence

## Current Workflow Inventory

- `.github/workflows/ci.yml`: push/PR CI on `main`; installs the project and
  runs `make check` across Python 3.11 and 3.12. It is a default quality
  workflow and must not publish packages or create releases.
- `.github/workflows/test.yml`: push/PR tests and deterministic benchmarks. It
  is a default quality workflow and must not publish packages or create
  releases.
- `.github/workflows/docs.yml`: pull-request and manual documentation,
  readiness, CLI, and artifact checks. It is a quality workflow and must not
  publish packages or create releases.
- `.github/workflows/benchmarks.yml`: manual benchmark reporting. It may upload
  GitHub Actions report artifacts, but it must not upload package artifacts to
  PyPI/TestPyPI and must not create tags or releases.
- `.github/workflows/release-dry-run.yml`: manual release dry-run. It may build
  local distributions and run `twine check`; it must not upload PyPI/TestPyPI,
  create tags, or create GitHub releases.
- `.github/workflows/create-prerelease.yml`: manual `workflow_dispatch`
  prerelease helper. It is not default CI and requires explicit maintainer
  operation. It must not be treated as an automatic release path.

No new workflow was added for this operations pass because the repository
already has CI and release-dry-run workflows. The current work documents and
tests their boundaries instead of adding overlapping automation.

## Non-goals

- no upload
- no tag creation
- no GitHub release creation
- no external solver by default
- no external LLM by default
- no proprietary solver by default
