# Final RC Gate: v0.9.0rc1

This document is the final release-candidate gate summary for `v0.9.0rc1`.
It does not create a git tag, GitHub release, or PyPI publication.

## Public Main Status

- Base public HEAD before bilingual README work:
  `46d6721 Add final 0.9.0rc1 release gate summary`
- Remote live verification before bilingual README work: `git fetch origin`
  succeeded and local `main` matched `origin/main`.
- GitHub Actions live verification: pending because `gh` is not installed.
- Public/main package metadata expected from the cached remote ref:
  - `pyproject.toml`: `version = "0.9.0rc1"`
  - `src/optical_spec_agent/__init__.py`: `__version__ = "0.9.0rc1"`
- README status: describes `0.9.0rc1` as a release candidate, not final stable
  `1.0`.
- Release draft exists: `docs/github_release_draft_v0.9.0rc1.md`
- Manual release checklist exists: `docs/manual_release_checklist_v0.9.0rc1.md`
- Chinese README support: `README.zh-CN.md` exists and `README.md` links to it.
- This final gate document status: updated with bilingual README support before
  the final documentation commit.

## Version Status

- pyproject version: `0.9.0rc1`
- package `__version__`: `0.9.0rc1`
- release candidate: yes
- final stable release: no
- GitHub tag created: no
- GitHub release created: no
- PyPI published: no

## Local Validation Status

Latest refreshed local release-candidate validation on 2026-05-12:

- `pip install -e ".[dev]"`: passed
- `pytest -q`: 331 passed, 4 warnings
- key_fields benchmark: 16/16 passed
- semantic benchmark: 27/27 passed
- semantic benchmark report: generated locally, not committed
- LLM benchmark: 40/40 passed
- workflow benchmark: 12/12 passed
- `make check`: passed
- `docs-check`: ready
- `cli-check`: ready
- `release-check`: ready
- `artifact-check`: ready
- `python -m build`: passed
- `twine check dist/*`: passed
- wheel metadata: `Version: 0.9.0rc1`
- source distribution includes both `README.md` and `README.zh-CN.md`
- CLI smoke: passed for parse, validate, schema, Meep preview generation,
  diagnose, adapter list/generate, LLM eval, workflow run, and workflow report.

Generated reports and build artifacts are local verification artifacts and
should not be committed.

## GitHub Actions Status

- Automatic workflows observed in this run: not live-verified because `gh` is
  not installed.
- Benchmark workflow status: manual dispatch required if maintainers want a
  fresh public report.
- Release dry-run workflow status: manual dispatch required if maintainers want
  a fresh public build artifact.
- Pending checks: unknown until GitHub Actions can be checked through the
  GitHub web UI or a configured `gh` CLI.
- Failures: none observed locally; live remote CI verification remains pending.

## RC Tag Readiness

- ready_for_manual_tag: no until this final documentation commit is pushed and
  GitHub Actions are verified green, or maintainers explicitly accept the
  current Actions state.
- ready_for_github_prerelease: no until this final documentation commit is
  pushed and GitHub Actions are verified green, or maintainers explicitly accept
  the current Actions state.
- ready_for_pypi: no unless separately approved.

## Manual Tag Commands, Not Executed

```bash
git tag v0.9.0rc1
git push origin v0.9.0rc1
```

## GitHub Release Instructions

- Use `docs/github_release_draft_v0.9.0rc1.md`.
- Mark the release as a pre-release.
- Do not mark it as final stable `1.0`.
- Do not publish PyPI unless separately approved.

## Remaining Limitations

- No production-grade physical validation.
- No formal convergence proof.
- No full solver automation.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs are MVP/scaffold.
- Workflow is local/synchronous preview.
- RC is not final `1.0` stability.

## Final Recommendation

If local quality gates and GitHub Actions are green after the bilingual README
support commit is pushed, the maintainer may manually tag `v0.9.0rc1` and
create a GitHub pre-release. If GitHub Actions cannot be verified, wait until
`git fetch origin`, `git push origin main`, and Actions status can be checked.
