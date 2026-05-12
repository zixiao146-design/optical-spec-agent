# Post-Tag Status: v0.9.0rc1

This document records the public status after the `v0.9.0rc1` tag was created.
It is intentionally separate from `docs/final_rc_gate_v0.9.0rc1.md` because the
tag points at the already-verified release-candidate commit.

## Tag Status

- Tag: `v0.9.0rc1`
- Tag commit: `3b4cfa83ca74a0c0bcab981614b86bf876974059`
- Tag commit message: `Add Chinese README support`
- Tag pushed to origin: yes
- Tag moved or overwritten: no

## GitHub Pre-Release Status

- GitHub pre-release created: no
- Reason: `gh` CLI was not installed in the local release environment.
- Manual release draft: `docs/github_release_draft_v0.9.0rc1.md`
- Release must be marked as a pre-release.
- PyPI publication remains out of scope and requires separate approval.

## Verification Snapshot

- `pyproject.toml`: `version = "0.9.0rc1"`
- `src/optical_spec_agent/__init__.py`: `__version__ = "0.9.0rc1"`
- `README.md`: includes the English / Simplified Chinese language switch.
- `README.zh-CN.md`: exists and documents the release candidate in Chinese.
- Latest local gates before tagging: passed.
- Latest public Actions observed through the GitHub API for commit `3b4cfa8`:
  `CI` success and `Tests` success.

## Manual GitHub Release Steps

```bash
# Already completed:
git tag v0.9.0rc1
git push origin v0.9.0rc1

# Still manual:
# 1. Open GitHub Releases.
# 2. Draft a new release for tag v0.9.0rc1.
# 3. Title: optical-spec-agent v0.9.0rc1.
# 4. Notes: use docs/github_release_draft_v0.9.0rc1.md.
# 5. Mark the release as a pre-release.
# 6. Do not publish PyPI unless separately approved.
```

## Remaining Limitations

- No production-grade physical validation.
- No formal convergence proof.
- No full solver automation.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs remain MVP/scaffold.
- Workflow orchestration is local/synchronous preview.
- `v0.9.0rc1` is not final `1.0` stability.
