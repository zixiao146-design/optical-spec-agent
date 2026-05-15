# Release Dry-run Operations

## Purpose

A release dry-run verifies readiness without creating tags, GitHub releases,
TestPyPI uploads, or PyPI publication.

## Dry-run Checklist

- Run only through manual `workflow_dispatch` or local maintainer command.
- `git status` is clean.
- Version state is understood.
- Quality gates pass.
- TestPyPI no-upload preflight passes.
- Build artifacts are generated locally.
- Dist filenames match `project.version`.
- Release notes draft exists if preparing a release candidate.
- Readiness doc exists.
- No tag is created.
- No GitHub release is created.
- No upload is performed.

## What Dry-run Must Not Do

- no automatic push/PR release action
- no `git tag`
- no tag push
- no `gh release create`
- no `twine upload`
- no PyPI/TestPyPI upload
- no secrets required
- no external solver, external LLM, or proprietary dependency

## Promotion After Dry-run

Only explicit maintainer approval can move a dry-run into any of these actions:

- tag creation
- GitHub prerelease creation
- TestPyPI upload
- PyPI publication

Each action requires a separate approval record or maintainer instruction. A
successful dry-run is evidence for readiness, not permission to publish.
