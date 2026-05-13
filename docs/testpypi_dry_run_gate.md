# TestPyPI Dry-run Gate

## Current status

- TestPyPI uploaded: no
- PyPI published: no
- Current public prerelease: v0.9.0rc3
- Current main development version: 0.9.0rc4.dev0
- Product positioning: open-source-solver-first
- Proprietary solvers are not default dependencies

## Purpose

This document defines what must be checked before any future TestPyPI upload is
approved. It does not authorize upload.

## Required dry-run checks

- `python -m build` passes.
- Wheel/sdist filenames match `project.version`.
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
- Approval must be recorded in docs or release notes.
- Default smoke/release scripts must never upload automatically.

## Upload non-goals

- This task does not upload TestPyPI.
- This task does not publish PyPI.
- This task does not create release artifacts beyond local dist.
- This task does not create GitHub release.

## Future command placeholders

DO NOT RUN WITHOUT APPROVAL:

```bash
python -m twine upload --repository testpypi dist/*
```

- Do not run this command in this task.
- Token must never be committed or printed.
