# Release Readiness: v0.9.0rc2

This document prepares the next release candidate after the `v0.9.0rc1`
post-release smoke test found a missing test dependency declaration.

## v0.9.0rc2 Goals

- Include post-release dependency fix from `730f6b6 Add httpx test dependency`.
- Include smoke test status documentation from
  `bcfe673 Record v0.9.0rc1 smoke test results`.
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
- `origin/main` contains `39fb14f`.
- `origin/main` contains `bcfe673`.
- `origin/main` contains `730f6b6`.
- `scripts/smoke_release.sh` passes.
- `pytest` passes: 331 passed, 4 warnings.
- `python -m build` passes.
- `optical-spec --help` passes.
- Documentation is updated.
- GitHub release draft is prepared.
- PyPI decision is explicitly recorded.

## Current Draft Status

- `origin/main` contains `39fb14f Add release smoke test automation`.
- `origin/main` contains `bcfe673 Record v0.9.0rc1 smoke test results`.
- `origin/main` contains `730f6b6 Add httpx test dependency`.
- `scripts/smoke_release.sh`: passed.
- `pytest`: 331 passed, 4 warnings.
- `python -m build`: passed.
- `optical-spec --help`: passed.
- PyPI decision: not published unless explicitly approved.

## Next Required Step

After this draft preparation commit lands on `main`, the next release step is:

1. Run a final smoke test from a clean environment.
2. Confirm build artifacts use version `0.9.0rc2`.
3. Create a new `v0.9.0rc2` tag from the approved `main` commit.
4. Create the GitHub pre-release for `v0.9.0rc2`.
5. Do not publish PyPI unless separately approved.

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
