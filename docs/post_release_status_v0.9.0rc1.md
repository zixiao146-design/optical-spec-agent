# Post-release Status: v0.9.0rc1

This document records the current public status for the `v0.9.0rc1` release
candidate. At the time of this update, the git tag exists, but the GitHub
pre-release is still pending manual creation through the GitHub Actions
workflow or GitHub UI.

## Release State

- Git tag: `v0.9.0rc1`
- Tag commit: `3b4cfa83ca74a0c0bcab981614b86bf876974059`
- Tag commit message: `Add Chinese README support`
- Tag pushed to origin: yes
- Tag moved or overwritten: no
- GitHub pre-release: pending; use the `Create v0.9.0rc1 Pre-release`
  workflow or manual GitHub UI.
- PyPI published: no
- Final stable `1.0`: no

## Bilingual README

- `README.md` language switch: yes
- `README.zh-CN.md`: yes
- Chinese release summary: yes

## Validation Summary

Latest known validation before the pre-release workflow was added:

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

The new `Create v0.9.0rc1 Pre-release` workflow should be run manually from the
GitHub Actions page to create the GitHub pre-release. If the release already
exists, the workflow prints its state and exits successfully.

## Manual GitHub Release Options

Option A, recommended:

```text
GitHub → Actions → Create v0.9.0rc1 Pre-release → Run workflow
```

Option B:

```text
GitHub → Releases → Draft a new release
Tag: v0.9.0rc1
Title: optical-spec-agent v0.9.0rc1
Notes: docs/github_release_draft_v0.9.0rc1.md
Mark as pre-release
```

Option C:

```bash
gh release create v0.9.0rc1 \
  --title "optical-spec-agent v0.9.0rc1" \
  --notes-file docs/github_release_draft_v0.9.0rc1.md \
  --prerelease \
  --latest=false
```

Do not upload `dist/` unless maintainers explicitly decide to do so. Do not
publish PyPI unless separately approved.

## Remaining Limitations

- No PyPI publish.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs remain MVP/scaffold.
- Workflow orchestration is local/synchronous preview.
- `v0.9.0rc1` is not final `1.0` stability.

## Recommended Next Action

- Run the manual GitHub Actions pre-release workflow.
- Observe early user feedback.
- Do not publish PyPI yet.
- Consider Chinese docs deep localization.
- Consider v1.0 API stabilization after RC feedback.
