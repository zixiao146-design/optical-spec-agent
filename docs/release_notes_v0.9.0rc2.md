# Release Notes: v0.9.0rc2

Drafted after the verified GitHub pre-release:
https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc2

## Summary

`v0.9.0rc2` supersedes `v0.9.0rc1` as the current release candidate. It keeps
the v0.6-v0.9 preview/scaffold/evaluation scope and adds the post-release test
dependency fix found during the `v0.9.0rc1` smoke test.

## Changes Since v0.9.0rc1

- Added explicit `test` extra with `pytest` and `httpx`.
- Fixed clean test environment collection failure caused by missing `httpx` for
  FastAPI/Starlette `TestClient`.
- Added `scripts/smoke_release.sh` for repeatable clean install/test/build/CLI
  smoke checks.
- Added `docs/release_readiness_v0.9.0rc2.md`.
- Updated release readiness docs to track the rc2 candidate.
- Verified `v0.9.0rc2` GitHub pre-release as `draft=false` and
  `prerelease=true`.

## Verification

- `scripts/smoke_release.sh`: passed
- `pytest`: 331 passed, 4 warnings at release time
- `python -m build`: passed
- Dist files:
  - `optical_spec_agent-0.9.0rc2-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc2.tar.gz`
- `optical-spec --help`: passed
- PyPI published: no

## Known Limitations

- No PyPI publish.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs are MVP/scaffold unless separately validated.
- Workflow orchestration is local/synchronous preview.
- RC is not final `1.0` stability.
