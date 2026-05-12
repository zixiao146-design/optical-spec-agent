# Release Readiness: v0.9.0rc2

This document prepares the next release candidate after the `v0.9.0rc1`
post-release smoke test found a missing test dependency declaration.

## v0.9.0rc2 Goals

- Include post-release dependency fix from `730f6b6 Add httpx test dependency`.
- Include smoke test status documentation from
  `bcfe673 Record v0.9.0rc1 smoke test results`, once pushed.
- Validate clean install with the test extra: `python -m pip install -e ".[test]"`.
- Validate `pytest`.
- Validate `python -m build`.
- Validate `optical-spec --help`.
- Keep PyPI unpublished unless explicitly approved.

## Relationship To v0.9.0rc1

- The `v0.9.0rc1` tag does not contain `730f6b6`.
- Do not retag, move, or overwrite `v0.9.0rc1`.
- If maintainers want a release artifact that includes the `httpx` test
  dependency fix, create `v0.9.0rc2`.

## v0.9.0rc2 Release Checklist

- `git status` is clean.
- `origin/main` contains `bcfe673`.
- `origin/main` contains `730f6b6`.
- `scripts/smoke_release.sh` passes.
- `python -m build` passes.
- `optical-spec --help` passes.
- Documentation is updated.
- GitHub release draft is prepared.
- PyPI decision is explicitly recorded.

## Smoke Test Command

```bash
chmod +x scripts/smoke_release.sh
OSA_SMOKE_VENV=/tmp/osa-smoke-v0.9.0rc2 ./scripts/smoke_release.sh
```

The script creates a clean virtual environment, installs the project with the
`test` extra, runs `pytest`, builds sdist/wheel artifacts, checks the declared
`optical-spec` console script, and lists `dist/` artifacts. It does not publish
PyPI, does not modify git tags, and does not edit GitHub releases.

## Remaining Limitations

- PyPI published: no.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs remain MVP/scaffold.
- Workflow orchestration is local/synchronous preview.
- RC is not final `1.0` stability.
