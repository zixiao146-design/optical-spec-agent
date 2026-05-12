# optical-spec-agent v0.9.0rc2

## English Summary

`v0.9.0rc2` is the next release candidate for the `v0.9.0` line. It follows
`v0.9.0rc1` and focuses on the post-release smoke-test dependency fix and
release automation added on `main`.

What changed since `v0.9.0rc1`:

- Adds an explicit `test` extra with `pytest` and `httpx`.
- Fixes the clean test environment failure caused by missing `httpx` for the
  FastAPI / Starlette `TestClient`.
- Adds `scripts/smoke_release.sh` for repeatable release smoke testing.
- Adds `docs/release_readiness_v0.9.0rc2.md`.
- Confirms clean install with the test extra.
- Confirms `pytest` passes.
- Confirms package build passes.
- Confirms `optical-spec --help` passes.

## 中文简介

`v0.9.0rc2` 是 `v0.9.0` 的第二个候选版本。它包含 `v0.9.0rc1`
发布后发现的测试依赖修复，并把 release smoke test 固化为自动化脚本。

本候选版本确认：

- clean venv 中可通过 `python -m pip install -e ".[test]"` 安装测试依赖。
- `pytest` 通过：331 passed, 4 warnings。
- `python -m build` 通过。
- `optical-spec --help` 通过。
- 新增 release smoke test 自动化脚本：`scripts/smoke_release.sh`。

## Verification

- `scripts/smoke_release.sh`: passed
- `pytest`: 331 passed, 4 warnings
- build: passed
- CLI help: `optical-spec --help` passed
- PyPI: not published

## Scope Limitations

- No PyPI publish.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs remain MVP/scaffold.
- Workflow orchestration is local/synchronous preview.
- RC is not final `1.0` stability.

## Important Note

The `v0.9.0rc1` tag is unchanged. `v0.9.0rc2` should be created as a new tag
from the appropriate `main` commit after readiness checks pass.
