# Current Draft Release Notes

Draft only. This document summarizes current `main` branch work since the
the previous `0.5.0` packaged baseline. It prepares `0.9.0rc1` as a release
candidate, pending manual tag/release approval.

## Summary

The current branch extends the v0.5 packaged Meep execution baseline with:

- v0.6 diagnostics
- v0.7 adapters
- v0.8 LLM parser foundation
- v0.9 workflow orchestration preview
- release engineering quality gates

## Since v0.5.0

- v0.6: post-hoc physical diagnostics via `optical-spec diagnose`.
- v0.7: adapter registry and `adapter-list` / `adapter-generate` for Meep,
  MPB, Gmsh, Elmer, and Optiland input scaffolds.
- v0.8: provider-agnostic parser foundation with deterministic mock LLM client,
  conservative hybrid parser, parser reports, and LLM benchmark.
- v0.9: local synchronous workflow orchestration with workflow artifacts,
  replay, reports, human-review checklist, and workflow benchmark.
- Release engineering: CI workflows, release-readiness scripts, artifact
  contracts, docs/CLI/API/benchmark contracts, issue templates, and changelog.

## What Is New

- `diagnose` CLI for post-hoc mesh/flux/execution diagnostics.
- `adapter-list` and `adapter-generate` for multi-solver scaffold generation.
- `llm-eval` for deterministic mock-provider parser evaluation.
- `workflow-plan`, `workflow-run`, `workflow-replay`, and `workflow-report` for
  local synchronous orchestration.
- CI workflows for local quality gates, benchmarks, docs checks, and release
  dry-runs.
- Release engineering scripts:
  - `scripts/check_cli_surface.py`
  - `scripts/check_docs_consistency.py`
  - `scripts/check_release_readiness.py`
  - `scripts/check_artifact_contracts.py`
  - `scripts/regenerate_demo_outputs.py`
- Artifact contracts and CLI/API/benchmark contracts.

## Quality Gates

- `pytest -q`
- `python benchmarks/run_benchmark.py --mode key_fields`
- `python benchmarks/run_semantic_benchmark.py`
- `python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json`
- `python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json`
- `make check`

## Verification Status

Most recent known local verification:

- `pip install -e ".[dev]"`: passed
- `pytest -q`: 329 passed, 4 warnings
- key_fields benchmark: 16/16 passed
- semantic benchmark: 27/27 passed
- LLM benchmark: 40/40 passed
- workflow benchmark: 12/12 passed
- `make check`: passed
- `docs-check`: ready
- `cli-check`: ready
- `release-check`: ready after the `0.9.0rc1` version bump
- `artifact-check`: ready
- `python -m build`: passed
- `twine check dist/*`: passed

## Not Included

- No production-grade physical validation.
- No formal convergence proof.
- No automatic external solver execution for MPB/Gmsh/Elmer/Optiland.
- No mandatory external LLM provider.
- No solver result interpretation by LLM.
- Mock LLM provider is deterministic and not proof of real model quality.
- Adapter outputs are MVP/scaffold.
- Workflow is synchronous/local preview.
- Release/tag creation remains manual.

## Suggested Release Tag

Recommended release label: `0.9.0rc1` if maintainers want to publish a
candidate.

No GitHub release, git tag, or PyPI publication has been created by this
document.
