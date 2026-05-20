# v1.0 Public Contract Freeze Confirmation

## Current status

- Current public prerelease: v0.9.0rc7
- Current main release draft: 0.9.0rc8
- TestPyPI uploaded and verified: yes
- PyPI published: no
- PyPI publication approval: not granted
- v1.0.0 released: no
- Maintainer confirmation: approved
- Freeze approval date: 2026-05-16
- Freeze baseline commit: 6e7ddf9c1811685c12db16bffb55cd76455267fe

## What this document is

This document records the maintainer-approved documentation freeze for the
v1.0 public contract. It summarizes the approved frozen public surface, the
areas that remain preview or explicitly non-goal, and the gates that should
remain satisfied before any later v1.0.0 release.

This approval freezes the documented public contract surface only. It does not
publish PyPI, does not create `v1.0.0`, does not create any tag or GitHub
release, and does not approve production-grade physical validation or a formal
convergence proof.

- This freeze does not publish PyPI.
- This freeze does not create any tag or GitHub release.
- This freeze does not create `v1.0.0`.

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

Recommendation: treat the v1.0 public contract freeze as approved for the
documented surface above, while keeping PyPI publication, `v1.0.0` release,
tag creation, and GitHub release creation separately gated.
