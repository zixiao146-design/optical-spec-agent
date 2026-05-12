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

Recommended path:

- Option A: use the manual GitHub Actions workflow
  `.github/workflows/create-prerelease.yml`.
- Option B: manually create the release in the GitHub UI.
- Option C: use a local `gh` CLI if it is installed and authenticated.

Option A is preferred because local network access and local `gh` availability
have been unreliable during the release-candidate preparation.

### Option A: GitHub Actions Workflow

1. Open GitHub Actions.
2. Select **Create v0.9.0rc1 Pre-release**.
3. Click **Run workflow**.
4. Use:
   - `tag = v0.9.0rc1`
   - `title = optical-spec-agent v0.9.0rc1`
5. Confirm the workflow exits successfully.
6. Check the Releases page.

The workflow does not publish PyPI, does not upload `dist/`, and does not create
or move the tag. If the GitHub release already exists, it prints the existing
release state and exits successfully.

### Option B: GitHub UI

- Use `docs/github_release_draft_v0.9.0rc1.md`.
- Mark the GitHub release as a pre-release.
- Do not mark it as the latest stable release if the GitHub UI allows avoiding
  that.
- Attach optional reports only if desired.
- Do not attach local `dist/` artifacts unless maintainers decide to do so.
- PyPI publishing requires separate approval.

### Option C: Local `gh` CLI

Run only if `gh` is installed and authenticated:

```bash
gh release create v0.9.0rc1 \
  --title "optical-spec-agent v0.9.0rc1" \
  --notes-file docs/github_release_draft_v0.9.0rc1.md \
  --prerelease \
  --latest=false
```

## After Release

- Verify the release page.
- Verify the tag.
- If PyPI was separately approved and published, run a clean install test.
- Update docs only if necessary to distinguish the published RC from later
  main-branch development.
