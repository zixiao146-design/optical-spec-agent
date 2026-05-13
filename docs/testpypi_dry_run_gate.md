# TestPyPI Dry-run Gate

## Current status

- TestPyPI uploaded: no
- PyPI published: no
- Current public prerelease: v0.9.0rc3
- Current main development version: 0.9.0rc4.dev0
- Product positioning: open-source-solver-first
- Proprietary solvers are not default dependencies
- v0.9.0rc4 tag: not created
- PyPI/TestPyPI remain unpublished/not uploaded
- TestPyPI upload approval record:
  `docs/testpypi_upload_approval_v0.9.0rc4.dev0.md`
- TestPyPI upload approval status: pending
- TestPyPI upload authorized: no
- PyPI publication approval: not granted

## Purpose

This document defines what must be checked before any future TestPyPI upload is
approved. It does not authorize upload.

## No-upload preflight

`scripts/testpypi_preflight.sh` performs the repeatable local preflight before
any future TestPyPI decision. It runs a local build, `python -m twine check
dist/*`, dist filename checks, clean wheel installation, package version import
checks, and `optical-spec --help`.

The preflight does not upload. It does not publish. It does not create tags. It
does not create GitHub releases. It prints `NO UPLOAD PERFORMED`.

## Required dry-run checks

- `python -m build` passes.
- `scripts/testpypi_preflight.sh` passes.
- Wheel/sdist filenames match `project.version`.
- `python -m twine check dist/*` passes.
- Wheel install smoke passes.
- `pip install -e ".[test]"` passes.
- `pytest` passes.
- `make check` passes.
- `optical-spec --help` passes.
- Documented CLI examples pass offline.
- Metadata is reviewed.
- README/readme field is correct.
- License metadata is acceptable.
- Dependencies are reasonable.
- Package imports cleanly after wheel install.
- No proprietary license is required.
- External solvers are not run by default.
- External LLM access is not required by default.

## Manual approval requirement

- TestPyPI upload requires explicit maintainer approval.
- PyPI upload requires explicit maintainer approval.
- The approval record remains pending until a maintainer explicitly grants
  TestPyPI upload approval.
- Approval must be recorded in docs or release notes.
- Default smoke/release scripts must never upload automatically.
- No token should be printed or committed.

## Upload non-goals

- This task does not upload TestPyPI.
- This task does not publish PyPI.
- This task does not create release artifacts beyond local dist.
- This task does not create GitHub release.
- This task does not create tags.

## Future command placeholders

DO NOT RUN WITHOUT APPROVAL:

```bash
python -m twine upload --repository testpypi dist/*
```

- Do not run this command in this task.
- Token must never be committed or printed.
