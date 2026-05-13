# Current Release Readiness

This document describes the current `main` branch. It is not a release tag.

## Current State

- `pyproject.toml` package version on `main`: `0.9.0rc3.dev0`
- Current public pre-release: `v0.9.0rc2`
- Main branch state: post-rc2 development toward a possible `v0.9.0rc3`
- `v0.9.0rc3` tag created: no
- GitHub pre-release created: yes
- Release verified: yes
- Post-release status doc: `docs/post_release_status_v0.9.0rc2.md`
- Latest release-status commit: `0a49fda`
- PyPI published: no
- Main branch capabilities:
  - v0.6 local/manual post-hoc diagnostics
  - v0.7 multi-solver adapter MVP scaffolds
  - v0.8 LLM parser foundation with deterministic mock provider
  - v0.9 synchronous local workflow orchestration foundation

## Capability Matrix

| Area | Main branch status | Release note |
|---|---|---|
| Rule parser | Stable baseline | Default parser |
| Diagnostics | RC preview | Does not run Meep |
| Meep execution harness | Optional local/manual | Meep not required in CI |
| MPB/Gmsh/Elmer/Optiland adapters | RC MVP scaffold generation | Do not run external solvers |
| LLM parser foundation | RC preview | Mock provider is deterministic |
| Workflow orchestration | RC preview | Local and synchronous |
| Bilingual README | RC ready | `README.md` links to `README.zh-CN.md`; Chinese README is complete |
| Public contracts | v1.0-readiness foundation | CLI, schema/API, adapter, workflow, validation, and PyPI boundaries documented |

## Quality Gates

Run these before proposing a release:

```bash
pip install -e ".[dev]"
OSA_SMOKE_VENV=/tmp/osa-smoke-current ./scripts/smoke_release.sh
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json
python scripts/check_cli_surface.py
python scripts/check_docs_consistency.py
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python scripts/check_artifact_contracts.py
make check
python -m build
twine check dist/*
```

## Recommended Version Action

Current recommendation: treat `v0.9.0rc2` as the active verified public
pre-release, treat `0.9.0rc3.dev0` on `main` as unreleased development, keep
PyPI unpublished, and continue `v1.0` readiness hardening. Prepare a
`v0.9.0rc3` release draft only when the accumulated hardening changes should be
published as a new public RC.

Current main contract artifacts:

- `docs/cli_contract.md`
- `docs/schema_contract.md`
- `docs/adapter_support_matrix.md`
- `docs/workflow_preview_contract.md`
- `docs/validation_boundary.md`
- `docs/pypi_publication_decision.md`
- `docs/packaging_gate.md`
- `docs/validation_gate.md`
- `docs/external_solver_policy.md`
- `docs/external_llm_policy.md`
- `docs/release_engineering_playbook.md`
- `docs/v1_0_readiness_plan.md`

## Release Blockers

- No hard release blocker is currently recorded for `v0.9.0rc2`.
- Do not move `v0.9.0rc1` or `v0.9.0rc2`.
- Do not publish PyPI yet.
- Keep generated adapter scaffolds presented as MVP inputs.
- Keep default CI free of external solver and external LLM requirements.
- Next blocker class: any `v0.9.0rc3` candidate must pass the release smoke
  script, full tests, build, docs checks, and release readiness checks before a
  new tag is considered.

## Known Limitations

- No production-grade physical validation.
- No formal convergence proof.
- No full solver automation.
- No external solver execution in default CI.
- No external LLM provider required by default.
- Mock LLM evaluation is deterministic and not a real model-quality proof.
- Adapter outputs remain scaffold/MVP unless separately validated.
- Meep execution remains optional/local.

## Manual Release Checklist

1. Use `docs/post_release_status_v0.9.0rc2.md` as the rc2 source of truth.
2. Use `docs/v1_0_readiness_plan.md` for the next hardening priorities.
3. Use `docs/release_engineering_playbook.md` for repeatable RC procedure.
4. Review the public contract docs before changing CLI, schema, adapter, or
   workflow behavior.
5. Run the packaging and validation gates before any future RC.
6. Before cutting `v0.9.0rc3`, change `0.9.0rc3.dev0` to `0.9.0rc3` and rerun
   final smoke/build checks.
7. Prepare `v0.9.0rc3` only if the next hardening patch needs a release
   candidate.
8. Keep PyPI unpublished unless explicitly approved.
