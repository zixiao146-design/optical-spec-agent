# v0.9.0rc4 Release Readiness

## Baseline

- Current public prerelease: v0.9.0rc3
- v0.9.0rc3 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc3
- v0.9.0rc3 target commit: acc407df1822db99bed258b6165099f3e5c2e424
- v0.9.0rc4 draft version: 0.9.0rc4
- v0.9.0rc4 tag: not created
- GitHub release: not created
- PyPI/TestPyPI: not published / not uploaded

## Included post-rc3 hardening

- Open-source-solver-first strategy
- Proprietary solver non-default/export-only policy
- Expanded adapter evidence fixtures
- Examples manifest
- Validation evidence manifest
- Optional open-source solver validation plan
- Offline user journey
- Error model
- Pre-v1 migration notes
- Public contract freeze candidate
- Public contract manifest
- TestPyPI no-upload preflight
- TestPyPI upload approval record, still pending
- Packaging and validation gates

## Required checks before tag creation

- `git status` clean
- `project.version == 0.9.0rc4`
- `__version__ == 0.9.0rc4`
- `v0.9.0rc4` tag absent locally/remotely
- `scripts/testpypi_preflight.sh` passed
- `scripts/smoke_release.sh` passed
- Wheel smoke passed
- `pytest` passed
- `python -m build` passed
- `make check` passed
- CLI examples passed
- E2E examples passed
- Dist filenames contain `0.9.0rc4`
- Release draft exists
- No PyPI/TestPyPI publication

## Current verification

- `scripts/testpypi_preflight.sh`: passed
- `scripts/smoke_release.sh`: passed
- Wheel install smoke: passed
- `pytest`: 429 passed, 4 warnings
- `python -m build`: passed
- `make check`: passed
- CLI examples: passed
- E2E examples: passed
- Dist files:
  - `optical_spec_agent-0.9.0rc4-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc4.tar.gz`
- PyPI: not published
- TestPyPI: not uploaded

## Next step

After maintainer approval:

1. Create an annotated `v0.9.0rc4` tag.
2. Push the tag.
3. Create the GitHub prerelease.
4. Verify `draft=false` and `prerelease=true`.
5. Create `docs/post_release_status_v0.9.0rc4.md`.

Do not publish PyPI/TestPyPI unless explicitly approved.
