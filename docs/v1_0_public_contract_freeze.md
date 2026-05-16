# v1.0 Public Contract Freeze

## Purpose

This document identifies the user-visible behavior covered by the
maintainer-approved v1.0 public contract freeze.

## Current scope

- Current public prerelease: v0.9.0rc6
- Current main development version: `0.9.0rc7.dev0`
- v1.0.0 not released
- v0.9.0rc7 tag not created
- v0.9.0rc7 GitHub release not created
- TestPyPI uploaded and verified for `0.9.0rc6.dev0`
- PyPI published: no
- PyPI publication approval: not granted
- Public contract freeze: approved
- Freeze approval date: 2026-05-16
- Freeze baseline commit: 6e7ddf9c1811685c12db16bffb55cd76455267fe

The executable freeze checklist is tracked in
`docs/v1_0_public_contract_freeze_checklist.md`, with approved status in
`docs/v1_0_public_contract_freeze_status.md`. Publication decisions remain
pending/not granted and are tracked in `docs/publication_decision_record.md`.

## Approved stable public contract

- Console script name: `optical-spec`
- Documented CLI command names in `docs/cli_contract.md`
- Documented offline examples in `examples/README.md`, `examples/e2e/README.md`,
  and `examples/examples_manifest.json`
- `project.version` and package import `optical_spec_agent.__version__` behavior
- Adapter registry names: `meep`, `mpb`, `gmsh`, `elmer`, and `optiland`
- `adapter-list --json` top-level object with an `adapters` array
- Schema public fields documented in `docs/schema_contract.md`
- Validation deterministic failure categories/fragments documented in
  `docs/error_model.md`
- `workflow-plan --json` public top-level keys documented in
  `docs/workflow_preview_contract.md`
- Examples manifest paths and no-network/no-solver/no-LLM/no-proprietary flags
- Package build metadata sufficient for local wheel install and
  `optical-spec --help`
- Public contract freeze checklist entries in
  `docs/v1_0_public_contract_freeze_checklist.md`

## Explicit preview / unstable areas

- Adapter generated-script internals
- Scaffold/MVP adapter output details
- Solver-backed physical validation
- Workflow internal implementation details
- External LLM-assisted parse behavior
- Optional external solver validation path
- Proprietary export-only future targets

## Change policy after the approved freeze

- Changes to the frozen public surface require maintainer approval.
- Breaking changes require explicit migration notes.
- Public examples must be updated with tests.
- Public schema field changes should get migration notes.
- CLI command removals/renames should be called out in release notes.
- Adapter support-level changes should update `docs/adapter_support_matrix.md`.
- Workflow output-shape changes should update contract tests.

## v1.0 freeze entry criteria

- Public contract manifest exists and passes tests.
- Public contract freeze checklist exists and is reviewed by the maintainer.
- CLI contract tests pass.
- Schema compatibility tests pass.
- Adapter matrix tests pass.
- Workflow preview contract tests pass.
- Offline user journey tests pass.
- Error model tests pass.
- Packaging/preflight checks pass.
- No external solver, external LLM, or proprietary solver dependency is required
  by default.
- TestPyPI/PyPI strategy is explicit before any v1.0 publication action.
- `v1.0.0` final release still requires separate approval.
