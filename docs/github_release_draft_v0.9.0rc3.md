# optical-spec-agent v0.9.0rc3

## English Summary

`v0.9.0rc3` is the third release candidate for the `v0.9.0` line. It includes
the v1.0 readiness hardening work that landed after the verified `v0.9.0rc2`
pre-release.

Highlights:

- Moves `main` from `0.9.0rc3.dev0` to the `0.9.0rc3` release-candidate draft
  state.
- Adds and stabilizes v1.0 readiness contracts.
- Adds or updates CLI contract coverage.
- Adds schema contract coverage.
- Adds adapter support matrix coverage.
- Adds workflow preview contract coverage.
- Adds validation boundary documentation.
- Adds PyPI/TestPyPI decision documentation and packaging gates.
- Adds validation gate documentation.
- Adds optional external solver and external LLM policy docs.
- Adds a wheel install smoke path to the release smoke script.
- Confirms clean install with the `test` extra.
- Confirms `pytest` passes.
- Confirms `python -m build` passes.
- Confirms `make check` passes.
- Confirms documented offline `optical-spec` CLI examples pass.

## 中文简介

`v0.9.0rc3` 是 `v0.9.0` 的第三个候选版本，纳入了 `v0.9.0rc2`
之后的 v1.0 readiness 加固工作。

本候选版本包括：

- CLI / schema / adapter / workflow contract 文档与测试加固。
- validation boundary、packaging gate、validation gate 和 PyPI decision gate。
- external solver / external LLM 默认不启用的策略文档。
- release smoke script 的 wheel install smoke 路径。
- `pytest` 通过：357 passed, 4 warnings。
- `python -m build` 通过。
- `make check` 通过。
- `optical-spec` 离线 CLI 示例通过。
- PyPI / TestPyPI 仍未发布。

## Verification

- `scripts/smoke_release.sh`: passed.
- Wheel install smoke: passed.
- `pytest`: 357 passed, 4 warnings.
- `python -m build`: passed.
- `make check`: passed.
- CLI examples passed:
  - `optical-spec --help`
  - `optical-spec adapter-list --json`
  - `optical-spec schema`
  - `optical-spec parse`
  - `optical-spec validate`
  - `optical-spec workflow-plan --json`
- PyPI: not published.
- TestPyPI: not uploaded.

## Scope Limitations

- No PyPI publish.
- No TestPyPI upload.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs may still be MVP/scaffold unless explicitly validated.
- Workflow orchestration is a local/synchronous preview.
- This release candidate is not final `1.0` stability.

## Important Note

- The `v0.9.0rc1` and `v0.9.0rc2` tags are unchanged.
- `v0.9.0rc3` should be created as a new annotated tag only after final
  readiness checks pass.
- This draft does not publish PyPI or TestPyPI.
- This draft does not create or move any tag.
