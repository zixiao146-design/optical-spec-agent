# GitHub Release Draft: `v0.9.0rc1`

This file is a maintainer draft only. Do not treat it as evidence that a
GitHub release, git tag, or PyPI package has been published.

## Release Title

`optical-spec-agent v0.9.0rc1`

## Release Type

Release candidate / preview / not final stable.

## Suggested Tag

`v0.9.0rc1`

## Summary

This release candidate packages the current main-branch engineering surface:

- v0.6 local/manual post-hoc diagnostics.
- v0.7 multi-solver adapter MVP scaffolds for Meep, MPB, Gmsh, Elmer, and
  Optiland.
- v0.8 provider-agnostic LLM parser foundation with deterministic mock
  provider and conservative hybrid parser.
- v0.9 synchronous local workflow orchestration with auditable artifacts,
  replay, reports, and human-review checklists.
- Release engineering quality gates for tests, benchmarks, docs consistency,
  CLI surface, artifact contracts, package build, and release dry-runs.

## What Changed

- Added `optical-spec diagnose` for post-hoc diagnostics.
- Added `optical-spec adapter-list` and `optical-spec adapter-generate` for
  solver-native input scaffold generation.
- Added `optical-spec llm-eval` for deterministic mock-provider parser
  evaluation.
- Added `optical-spec workflow-plan`, `workflow-run`, `workflow-replay`, and
  `workflow-report`.
- Added CI workflows for deterministic local quality gates, manual benchmark
  reports, docs/contract checks, and release dry-run builds.
- Added Makefile quality gates for tests, benchmarks, docs, CLI, release, and
  artifact contract checks.
- Added release engineering scripts for CLI surface, docs consistency, release
  readiness, artifact contracts, and demo output regeneration.
- Added artifact, API, CLI, benchmark, security, robustness, versioning, and
  release-readiness documentation.

## Verification

Most recent known local validation before this draft:

- `pip install -e ".[dev]"`: passed
- `pytest -q`: 329 passed, 4 warnings
- key_fields benchmark: 16/16 passed
- semantic benchmark: 27/27 passed
- LLM benchmark: 40/40 passed
- workflow benchmark: 12/12 passed
- `make check`: passed
- `docs-check`: ready
- `cli-check`: ready
- `release-check`: ready
- `artifact-check`: ready
- `python -m build`: passed
- `twine check dist/*`: passed

Maintainers should verify GitHub Actions after pushing the release-candidate
commit.

## Installation

If this candidate is published to PyPI after separate approval:

```bash
pip install optical-spec-agent==0.9.0rc1
```

This task does not publish to PyPI.

## Known Limitations

- No production-grade physical validation.
- No formal convergence proof.
- No full solver automation.
- External solvers are not run by default.
- External LLM providers are not required by default.
- The mock LLM provider is deterministic test infrastructure, not proof of
  real model quality.
- Adapter outputs are MVP/scaffold unless separately validated.
- Workflow orchestration is synchronous/local preview.
- Meep execution remains optional/local.
- This is not a final stable `1.0` API.

## Manual Maintainer Steps

1. Review the final diff on `main`.
2. Push `main` and verify GitHub Actions.
3. Create the tag manually only after approval:

   ```bash
   git tag v0.9.0rc1
   git push origin v0.9.0rc1
   ```

4. Draft a GitHub pre-release using this file.
5. Attach `release_readiness_report.json` if desired.
6. Publish to PyPI only after separate approval.
