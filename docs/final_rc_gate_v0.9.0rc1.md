# Final RC Gate: v0.9.0rc1

This document is the final release-candidate gate summary for `v0.9.0rc1`.
It does not create a git tag, GitHub release, or PyPI publication.

## Public Main Status

- Local HEAD: `6c860ff Add 0.9.0rc1 release publication checklists`
- Cached `origin/main` HEAD: `6c860ff`
- Remote live verification: pending due GitHub HTTPS network failure during
  `git fetch origin` on 2026-05-12:
  `fatal: unable to access 'https://github.com/zixiao146-design/optical-spec-agent.git/': Empty reply from server`
- Public/main package metadata expected from the cached remote ref:
  - `pyproject.toml`: `version = "0.9.0rc1"`
  - `src/optical_spec_agent/__init__.py`: `__version__ = "0.9.0rc1"`
- README status: describes `0.9.0rc1` as a release candidate, not final stable
  `1.0`.
- Release draft exists: `docs/github_release_draft_v0.9.0rc1.md`
- Manual release checklist exists: `docs/manual_release_checklist_v0.9.0rc1.md`
- This final gate document status: local until committed and pushed.

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
- `pytest -q`: 329 passed, 4 warnings
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
- `python -m build`: passed
- `twine check dist/*`: passed
- wheel metadata: `Version: 0.9.0rc1`
- CLI smoke: passed for parse, validate, schema, Meep preview generation,
  diagnose, adapter list/generate, LLM eval, workflow run, and workflow report.

Generated reports and build artifacts are local verification artifacts and
should not be committed.

## GitHub Actions Status

- Automatic workflows observed in this run: not live-verified because `gh` is
  not installed and `git fetch origin` failed over HTTPS.
- Benchmark workflow status: manual dispatch required if maintainers want a
  fresh public report.
- Release dry-run workflow status: manual dispatch required if maintainers want
  a fresh public build artifact.
- Pending checks: unknown until GitHub Actions can be checked after network
  recovery or through the GitHub web UI.
- Failures: none observed locally; live remote CI verification remains pending.

## RC Tag Readiness

- ready_for_manual_tag: no until live GitHub Actions / public remote state are
  verified after network recovery.
- ready_for_github_prerelease: no until live GitHub Actions / public remote
  state are verified after network recovery.
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

If local quality gates and GitHub Actions are green after network recovery,
the maintainer may manually tag `v0.9.0rc1` and create a GitHub pre-release.
If remote verification remains blocked by network, wait until `git fetch origin`,
`git push origin main`, and GitHub Actions can be checked.
