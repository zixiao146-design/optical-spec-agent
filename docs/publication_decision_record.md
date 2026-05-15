# Publication Decision Record

## Current status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- TestPyPI uploaded: no
- PyPI published: no
- TestPyPI upload approval: granted for 0.9.0rc6.dev0 only
- PyPI publication approval: not granted
- Upload command authorized: TestPyPI only
- Latest TestPyPI upload attempt:
  `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`
- Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden

## Decisions not yet granted

- PyPI publication
- PyPI project name claim
- No production-grade validation claim
- No formal convergence proof claim
- GitHub tag creation for v0.9.0rc6
- GitHub release creation for v0.9.0rc6

## Possible publication paths

### Path A

- Continue GitHub prereleases only.
- No TestPyPI.
- No PyPI.

### Path B

- Upload to TestPyPI only.
- Verify clean install from TestPyPI.
- Do not publish PyPI.

### Path C

- Upload to TestPyPI.
- Verify.
- Then separately approve PyPI publication.

## Required before TestPyPI upload

- Explicit maintainer approval.
- TestPyPI token available.
- No-upload preflight passed.
- Quality gates passed.
- Version/tag strategy understood.
- Post-TestPyPI verification plan ready.

## Required before PyPI publication

- Explicit maintainer approval.
- TestPyPI completed or explicit skip recorded.
- PyPI token available.
- Yanking/rollback policy reviewed.
- Production/validation claims reviewed.
- Release notes final.

## Current recommendation

Recommended current state: upload `0.9.0rc6.dev0` to TestPyPI only, verify a
clean install from TestPyPI, and keep PyPI publication separately gated while
v1.0 readiness engineering continues.

The latest TestPyPI upload attempt failed with HTTP 403 Forbidden, so TestPyPI
remains not uploaded until a token with sufficient TestPyPI permissions is used.

This record authorizes TestPyPI upload only for `0.9.0rc6.dev0`. It does not
authorize PyPI publication, GitHub release creation, tag creation, production-
grade validation claims, or formal convergence proof claims.
