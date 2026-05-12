# Release Engineering Playbook

This playbook captures the release process hardened during the `v0.9.0rc1` and
`v0.9.0rc2` release candidates.

## Release phases

1. Readiness preparation: update release notes, readiness docs, and known limitations.
2. Version bump: update `pyproject.toml` and `src/optical_spec_agent/__init__.py`.
3. Smoke validation: run a clean install/test/build/CLI smoke cycle.
4. Tag creation: create an annotated RC tag only after remote tag absence is verified.
5. GitHub pre-release creation: publish a pre-release from the checked-in draft notes.
6. Post-release verification: verify tag, release URL, draft status, pre-release flag, and notes.
7. Post-release status documentation: record the verified state in `docs/post_release_status_<version>.md`.
8. Next-candidate planning: document any post-release fixes in a new RC plan.

## Clean smoke command

```bash
OSA_SMOKE_VENV=/tmp/osa-smoke-<version> ./scripts/smoke_release.sh
```

The smoke script creates a fresh virtual environment, installs the project with
the `test` extra, runs `pytest`, builds the package, validates dist filenames,
and checks `optical-spec --help` when the console script is declared.

## Required verification

- `git status` is clean before tagging.
- The package version matches `pyproject.toml`.
- `src/optical_spec_agent/__init__.py` matches the package version.
- `python -m pip install -e ".[test]"` passes in a clean environment.
- `pytest` passes.
- `python -m build` passes.
- Dist filenames match the package version.
- `optical-spec --help` passes.
- Release notes source exists.
- Post-release status doc is created after the GitHub release is verified.

## Tag and release policy

- Use annotated tags for RC releases.
- Never move existing tags.
- Never re-tag `v0.9.0rc1` or `v0.9.0rc2`.
- Create a new RC tag for post-release fixes.
- GitHub pre-releases must have `draft=false` and `prerelease=true`.
- Release notes should match `docs/github_release_draft_<version>.md`.

## Token and credential safety

- Never paste tokens into chat, logs, docs, or commits.
- Use `read -s GH_TOKEN` for temporary local authentication when needed.
- Unset `GH_TOKEN` and `GITHUB_TOKEN` after use.
- Revoke exposed tokens immediately.
- Use least-privilege fine-grained tokens.
- Grant Contents read/write only when tag/release creation is required.

## Network failure handling

- `Empty reply from server` and TLS timeouts can happen during GitHub HTTPS operations.
- Do not reset or delete local work after a network failure.
- Keep local commits and retry push later.
- The GitHub API path can be used when git HTTPS is unstable.
- Stop before unsafe tag creation if remote tag existence cannot be verified.

## PyPI policy

- PyPI remains unpublished unless explicitly approved.
- Prefer TestPyPI first if packaging publication is later approved.
- Never publish during release engineering smoke without explicit approval.
