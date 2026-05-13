# Current Release Readiness

This document describes the current `main` branch. It is not a release tag.

## Current State

- `pyproject.toml` package version on `main`: `0.9.0rc4.dev0`
- Current public prerelease: `v0.9.0rc3`
- Current main development version: `0.9.0rc4.dev0`
- Main branch state: post-`v0.9.0rc3` development toward `v0.9.0rc4`
- Product positioning: open-source-solver-first
- `v0.9.0rc4.dev0` is not a release
- `v0.9.0rc4` tag has not been created
- GitHub pre-release created: yes
- Release verified: yes
- Post-release status doc: `docs/post_release_status_v0.9.0rc3.md`
- Latest release-status commit: `4d2991f`
- PyPI published: no
- TestPyPI uploaded: no
- TestPyPI upload approval record:
  `docs/testpypi_upload_approval_v0.9.0rc4.dev0.md`
- TestPyPI upload approval status: pending
- TestPyPI upload authorized: no
- PyPI publication approval: not granted
- Proprietary solvers are not default dependencies.
- No proprietary license is required for default tests, smoke, examples, or
  release validation.
- v1.0 compatibility policy exists: `docs/v1_0_compatibility_policy.md`
- Validation evidence manifest exists: `docs/validation_evidence_manifest.md`
- Optional open-source solver validation plan exists:
  `docs/open_source_solver_validation_plan.md`
- Examples manifest exists: `examples/examples_manifest.json`
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

Current recommendation: treat `v0.9.0rc3` as the active verified public
prerelease. The `main` branch now builds as `0.9.0rc4.dev0` and may contain
post-`v0.9.0rc3` hardening changes. Continue v1.0 readiness engineering and
prepare a `v0.9.0rc4` release draft only when accumulated changes should be
published as another RC. Keep PyPI/TestPyPI unpublished unless explicitly
approved.

Current main contract artifacts:

- `docs/cli_contract.md`
- `docs/schema_contract.md`
- `docs/adapter_support_matrix.md`
- `docs/workflow_preview_contract.md`
- `docs/validation_boundary.md`
- `docs/open_source_solver_strategy.md`
- `docs/proprietary_solver_policy.md`
- `docs/v1_0_compatibility_policy.md`
- `docs/validation_evidence_manifest.md`
- `docs/open_source_solver_validation_plan.md`
- `docs/pypi_publication_decision.md`
- `docs/packaging_gate.md`
- `docs/validation_gate.md`
- `docs/external_solver_policy.md`
- `docs/external_llm_policy.md`
- `docs/release_engineering_playbook.md`
- `docs/v1_0_readiness_plan.md`
- `docs/release_readiness_v0.9.0rc4.md`
- `docs/testpypi_dry_run_gate.md`
- `docs/v1_0_stability_gate.md`
- `docs/schema_compatibility_policy.md`
- `examples/README.md`

Current v1.0 evidence artifacts:

- Offline examples: `examples/specs/minimal_nanoparticle.json`,
  `examples/specs/missing_wavelength_meep_preview.json`, and
  `examples/workflows/local_preview_request.json`.
- Adapter evidence fixtures:
  `tests/fixtures/adapter_golden/meep_missing_wavelength_expected_fragments.txt`.
- Expanded adapter family evidence fixtures:
  `tests/fixtures/adapter_golden/gmsh/`, `tests/fixtures/adapter_golden/elmer/`,
  `tests/fixtures/adapter_golden/mpb/`, and
  `tests/fixtures/adapter_golden/optiland/`.
- Workflow evidence fixtures:
  `tests/fixtures/workflow_preview/local_preview_expected_keys.json`.
- Failure-mode regression: `tests/test_failure_mode_regression.py`.
- Schema compatibility evidence: `docs/schema_compatibility_policy.md` and
  `tests/test_schema_compatibility_policy.py`.
- Workflow-to-adapter planning evidence:
  `tests/test_workflow_adapter_evidence.py`.

## Release Blockers

- No hard release blocker is currently recorded for `v0.9.0rc3`.
- Do not move `v0.9.0rc1`, `v0.9.0rc2`, or `v0.9.0rc3`.
- Do not publish PyPI yet.
- Do not upload TestPyPI yet.
- Keep generated adapter scaffolds presented as MVP inputs.
- Keep default CI free of external solver and external LLM requirements.
- Next blocker class: any `v0.9.0rc4` candidate must pass the release smoke
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

1. Use `docs/post_release_status_v0.9.0rc3.md` as the rc3 source of truth.
2. Use `docs/v1_0_readiness_plan.md` for the next hardening priorities.
3. Use `docs/release_engineering_playbook.md` for repeatable RC procedure.
4. Review the public contract docs before changing CLI, schema, adapter, or
   workflow behavior.
5. Run the packaging and validation gates before any future RC.
6. Confirm `v0.9.0rc4` tag is absent locally and remotely before tag creation.
7. Create an annotated `v0.9.0rc4` tag only after final maintainer approval.
8. Keep PyPI/TestPyPI unpublished unless explicitly approved.
