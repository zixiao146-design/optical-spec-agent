# Maintainer Operations Checklist

## Routine Development

- Keep `main` in `.dev0` after a public release candidate is published.
- Run quality gates before large pushes.
- Keep the working tree clean before release operations.
- Do not move tags.

## Before RC Release Draft

- Bump version from `.dev0` to the target `rcN`.
- Release draft notes exist.
- Readiness doc exists.
- Release notes exist.
- Quality gates pass.
- No upload is performed.

## Before Tag Creation

- Maintainer approval is recorded or explicitly provided.
- Tag is absent locally and remotely.
- HEAD is verified.
- Use annotated tags only.
- Do not upload TestPyPI/PyPI unless separately approved.

## Before TestPyPI Upload

- Approval record exists.
- Approval is granted.
- No-upload preflight passed.
- TestPyPI token is available securely.
- PyPI remains separately gated.

## Before PyPI Publication

- TestPyPI has been evaluated, or an explicit skip is recorded.
- PyPI approval is granted.
- Rollback/yank policy is reviewed.
- Production claims are reviewed.
- Release notes are final.
