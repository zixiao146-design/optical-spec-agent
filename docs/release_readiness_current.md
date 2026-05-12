# Current Release Readiness

This document describes the current `main` branch. It is not a release tag.

## Current State

- `pyproject.toml` package version: `0.9.0rc2`
- Status: preparing `0.9.0rc2` release-candidate draft
- Formal GitHub release/tag: `v0.9.0rc1` exists; `v0.9.0rc2` is not tagged
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

## Quality Gates

Run these before proposing a release:

```bash
pip install -e ".[dev]"
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

Current recommendation: review the prepared `0.9.0rc2` draft, run the release
smoke test, and create a new tag/GitHub pre-release only after maintainer
approval.

## Release Blockers

- Human decision needed on whether to tag/publish the prepared `0.9.0rc2` RC.
- Confirm whether workflow orchestration should be included in the manually
  published release candidate notes.
- Confirm that generated adapter scaffolds are still presented as MVP inputs.
- Confirm that default CI remains free of external solver and external LLM
  requirements.
- Confirm that `0.9.0rc2` should supersede `0.9.0rc1` for users who need the
  post-release test dependency fix.
- Confirm bilingual README support:
  - `README.md` has a language switch.
  - `README.zh-CN.md` exists.
  - Chinese README release status matches the English README.

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

1. Run all quality gates above.
2. Review `docs/release_notes_current.md`.
3. Confirm `0.9.0rc2` is the desired candidate version.
4. Build with `python -m build`.
5. Check distributions with `twine check dist/*`.
6. Create a release branch or tag manually.
7. Publish GitHub/PyPI artifacts manually after review.
