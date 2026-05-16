# v1.0 Public Contract Freeze Confirmation

## Current status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- TestPyPI uploaded and verified: yes
- PyPI published: no
- v1.0.0 released: no
- Maintainer confirmation: pending

## What this document is

This document prepares the maintainer-facing confirmation package for freezing
the v1.0 public contract. It summarizes the candidate frozen public surface,
the areas that remain preview or explicitly non-goal, and the confirmation
gates that must be reviewed before the freeze can be approved.

This document does not approve the freeze. Maintainer confirmation remains
pending until a separate explicit approval step.

## Candidate frozen areas

- `optical-spec` console script
- Documented CLI commands
- Documented CLI options that are explicitly covered by contract tests
- Documented JSON schema public fields
- Adapter registry names
- `adapter-list --json` top-level shape
- `workflow-plan --json` top-level shape
- Offline examples and examples manifest
- No-network/no-default-solver/no-default-LLM/no-default-proprietary guarantees
- Package metadata: name, version semantics, console script

## Areas not frozen

- Generated adapter script internals
- Optional solver validation internals
- Workflow implementation internals
- External LLM-assisted parse internals
- Proprietary export-only future targets
- Production-grade physical validation
- Formal convergence proof
- Elmer Level 3 validation

## Confirmation gates

- Quality gates pass
- CI pass
- Pytest/build/make check pass
- TestPyPI verified
- PyPI publication decision remains explicit
- Validation claims reviewed
- Maintainer explicitly approves freeze

## Current recommendation

Recommendation: keep maintainer confirmation pending until final review, then
approve freeze in a separate explicit step.

