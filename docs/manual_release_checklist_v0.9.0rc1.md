# Manual Release Checklist: `v0.9.0rc1`

Do not run these release steps automatically. This checklist is for a human
maintainer after review.

## Before Tag

- Confirm `main` has `pyproject.toml` version `0.9.0rc1`.
- Confirm `src/optical_spec_agent/__init__.py` has `__version__ = "0.9.0rc1"`.
- Confirm README describes `0.9.0rc1` as a release candidate, not final stable
  `1.0`.
- Confirm `README.md` has a language switch.
- Confirm `README.zh-CN.md` exists.
- Confirm Chinese README release status matches English README.
- Confirm `python scripts/check_release_readiness.py` reports ready.
- Confirm `make check` passed.
- Confirm `python -m build` and `twine check dist/*` passed.
- Confirm GitHub Actions passed.
- Confirm no generated `outputs/`, `dist/`, `build/`, or cache files are
  committed.

## Tag Commands

Run only after maintainer approval:

```bash
git tag v0.9.0rc1
git push origin v0.9.0rc1
```

## GitHub Release

- Use `docs/github_release_draft_v0.9.0rc1.md`.
- Mark the GitHub release as a pre-release.
- Do not mark it as the latest stable release if the GitHub UI allows avoiding
  that.
- Attach optional reports only if desired.
- Do not attach local `dist/` artifacts unless maintainers decide to do so.
- PyPI publishing requires separate approval.

## After Release

- Verify the release page.
- Verify the tag.
- If PyPI was separately approved and published, run a clean install test.
- Update docs only if necessary to distinguish the published RC from later
  main-branch development.
