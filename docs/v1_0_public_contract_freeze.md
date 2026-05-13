# v1.0 Public Contract Freeze Candidate

## Purpose

This document identifies the user-visible behavior that is being prepared for
v1.0 stabilization.

## Current scope

- Current public prerelease: v0.9.0rc3
- Current main release draft: 0.9.0rc4
- v1.0.0 not released
- v0.9.0rc4 tag not created
- GitHub release not created
- PyPI/TestPyPI not published/uploaded

## Candidate stable public contract

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

## Explicit preview / unstable areas

- Adapter generated-script internals
- Scaffold/MVP adapter output details
- Solver-backed physical validation
- Workflow internal implementation details
- External LLM-assisted parse behavior
- Optional external solver validation path
- Proprietary export-only future targets

## Change policy before v1.0

- Breaking changes are allowed before v1.0 but should be documented.
- Public examples must be updated with tests.
- Public schema field changes should get migration notes.
- CLI command removals/renames should be called out in release notes.
- Adapter support-level changes should update `docs/adapter_support_matrix.md`.
- Workflow output-shape changes should update contract tests.

## v1.0 freeze entry criteria

- Public contract manifest exists and passes tests.
- CLI contract tests pass.
- Schema compatibility tests pass.
- Adapter matrix tests pass.
- Workflow preview contract tests pass.
- Offline user journey tests pass.
- Error model tests pass.
- Packaging/preflight checks pass.
- No external solver, external LLM, or proprietary solver dependency is required
  by default.
