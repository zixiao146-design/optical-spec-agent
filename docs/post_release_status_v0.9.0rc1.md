# Post-release Status: v0.9.0rc1

## Release State

- Git tag: `v0.9.0rc1`
- Tag commit: `3b4cfa83ca74a0c0bcab981614b86bf876974059`
- Tag commit message: `Add Chinese README support`
- Release verified: yes
- GitHub pre-release: created
- GitHub prerelease flag verified: yes
- Release title: `optical-spec-agent v0.9.0rc1`
- Release URL: <https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc1>
- Release notes source: `docs/github_release_draft_v0.9.0rc1.md`
- Release notes include Chinese summary: yes
- PyPI published: no
- Final stable `1.0`: no

## Bilingual README

- `README.md` language switch: yes
- `README.zh-CN.md`: yes
- Chinese release summary: yes

## Validation Summary

- `pytest -q`: 331 passed, 4 warnings
- key_fields benchmark: 16/16 passed
- semantic benchmark: 27/27 passed
- LLM benchmark: 40/40 passed
- workflow benchmark: 12/12 passed
- `make check`: passed
- docs consistency: ready
- CLI surface: ready
- release readiness: ready
- artifact contracts: ready
- `python -m build`: passed
- `twine check dist/*`: passed
- CLI smoke: passed

## Post-release Smoke Test Follow-up

After the `v0.9.0rc1` GitHub pre-release was verified, a clean-environment
post-release smoke test found a test dependency declaration gap:

- `python -m pip install -e .`: passed
- `python -m build`: passed
- Initial `python -m pytest`: failed during collection because `httpx` was
  missing.
- Failure reason: `starlette.testclient` / `fastapi.testclient` requires
  `httpx`.
- After manually installing `httpx`, `python -m pytest` passed with 331 passed
  and 4 warnings.

The dependency declaration was fixed on `main` after the release tag:

- Fix commit: `730f6b6 Add httpx test dependency`
- Changed file: `pyproject.toml`
- Added optional dependency group:
  `test = ["pytest>=8.0", "httpx>=0.27"]`
- Pushed to `origin/main`: yes

Post-fix clean venv verification:

- `python -m pip install -e ".[test]"`: passed
- `python -m pytest`: 331 passed, 4 warnings
- `python -m build`: passed
- `project.scripts` declares CLI command: `optical-spec`
- `optical-spec --help`: passed
- `git status`: clean

Important release note: the `v0.9.0rc1` tag itself does not contain post-release
fix `730f6b6`. That commit is a post-release smoke-test dependency fix on
`main`. If maintainers want this dependency declaration fix included in an
installable release artifact, prepare `v0.9.0rc2` instead of retagging or moving
`v0.9.0rc1`.

## Verification Notes

- Verification method: GitHub CLI with token authentication.
- GitHub CLI verification result:
  - `tagName`: `v0.9.0rc1`
  - `name`: `optical-spec-agent v0.9.0rc1`
  - `isDraft`: `false`
  - `isPrerelease`: `true`
  - `url`: <https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc1>

## Remaining Limitations

- No PyPI publish.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs remain MVP/scaffold.
- Workflow orchestration is local/synchronous preview.
- RC is not final `1.0` stability.

## Recommended Next Action

- Observe early user feedback.
- Do not publish PyPI yet.
- Consider Chinese docs deep localization.
- Consider v1.0 API stabilization after RC feedback.
