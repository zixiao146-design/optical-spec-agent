# Version Bump Plan: `0.9.0rc1`

This plan records the `0.9.0rc1` bump. Applying the version bump does not create
a git tag, GitHub release, or PyPI publication.

## Proposed Version

`0.9.0rc1`

## Why RC1 Instead Of Final `0.9.0`

- Main branch has a large feature surface across v0.6-v0.9.
- v0.6-v0.9 capabilities are engineering previews, scaffolds, diagnostics, or
  evaluation tools.
- The user-facing CLI surface is broad and should receive release-candidate
  testing.
- CI and local gates pass, but formal releases have lagged behind main.
- An RC lets users test without implying final stability or production physical
  validation.

## Files To Update If Bumping

- `pyproject.toml`
- `src/optical_spec_agent/__init__.py`
- `README.md`
- `CHANGELOG.md`
- `docs/release_readiness_current.md`
- `docs/release_notes_current.md`
- `docs/release_notes_v0.9.0.md`
- `docs/versioning_policy.md`, if additional wording is needed

## Exact Pyproject Change

```diff
-version = "0.5.0"
+version = "0.9.0rc1"
```

Also update `src/optical_spec_agent/__init__.py` from `0.5.0` to `0.9.0rc1`
if the package version is mirrored there.

## Required Commands After Bump

```bash
pip install -e ".[dev]"
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json
make check
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python -m build
twine check dist/*
```

## Manual Release Steps

1. Review generated docs and release notes.
2. Confirm no generated `outputs/` artifacts are accidentally committed.
3. Confirm README still states no production-grade physical validation.
4. Create a git tag manually only after approval.
5. Create a GitHub release manually only after approval.
6. Attach `release_readiness_report.json` if desired.
7. Do not publish to PyPI unless separately approved.
