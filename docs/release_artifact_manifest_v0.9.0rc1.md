# Release Artifact Manifest: `0.9.0rc1`

This manifest describes the expected local build outputs for the release
candidate. It is not a publication record.

## Expected Package Artifacts

After a clean build:

- Wheel: `dist/optical_spec_agent-0.9.0rc1-py3-none-any.whl`
- Source distribution: `dist/optical_spec_agent-0.9.0rc1.tar.gz`
- Metadata version: `0.9.0rc1`

Validate with:

```bash
python -m build
twine check dist/*
```

Optional checksums may be generated from the final clean build, but they should
be regenerated immediately before attaching artifacts anywhere.

## Optional Reports to Attach

Maintainers may attach these generated reports to a GitHub pre-release if
desired:

- `outputs/release_readiness_report.json`
- `outputs/semantic_benchmark_report.json`
- `outputs/llm_eval_report.json`
- `outputs/workflow_benchmark_report.json`

These reports are generated artifacts and should not be committed by default.

## Do Not Commit

- `dist/`
- `build/`
- `*.egg-info`
- `outputs/`
- cache directories such as `.pytest_cache/`, `.ruff_cache/`, and
  `__pycache__/`

## Commit These Docs

- Draft release notes.
- Release readiness docs.
- GitHub release draft.
- Release artifact manifest.
- Post-push CI checklist.
- Manual release checklist.

## Verification Notes

`twine check dist/*` must pass before any package artifact is uploaded. The
release candidate remains a preview/scaffold/evaluation package and must not be
described as production-grade physical validation.
