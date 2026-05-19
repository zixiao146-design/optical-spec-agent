# Offline User Journey

## Purpose

This document describes the default local-first journey for
`optical-spec-agent`. It requires no network, no external solver, no external LLM,
no proprietary software, and no proprietary optical software.

## Current version scope

- Current public prerelease: v0.9.0rc7
- Current main development version: `0.9.0rc8.dev0`
- PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0
- v0.9.0rc8 tag: not created

## Journey steps

1. Inspect the CLI surface.
2. Validate a local spec fixture.
3. Parse a local spec fixture through the deterministic offline path.
4. List registered adapters without loading external solvers.
5. Generate or inspect adapter preview evidence from checked-in fixtures.
6. Run `workflow-plan` in local preview/no-execute mode.
7. Inspect diagnostics and stable output shape.

## Commands

```bash
optical-spec --help
optical-spec validate examples/specs/minimal_nanoparticle.json
optical-spec parse examples/specs/minimal_nanoparticle.json --json
optical-spec adapter-list --json
optical-spec workflow-plan examples/workflows/local_preview_request.json --json
optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json
```

## Expected guarantees

- Commands run offline.
- No external solver is executed.
- No external LLM is required.
- No proprietary software is required.
- Output shape is covered by tests.
- Examples are regression checked.
- Public contract coverage is tracked in `docs/public_contract_manifest.json`.

## Non-goals

- No production-grade physical validation.
- No formal convergence proof.
- No solver-backed correctness claim by default.
- No PyPI/TestPyPI publication.
- No commercial solver validation.
