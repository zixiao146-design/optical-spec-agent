# Publication Decision Record

## Current status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- TestPyPI uploaded: no
- PyPI published: no
- TestPyPI upload approval: pending
- PyPI publication approval: not granted
- Upload command authorized: no

## Decisions not yet granted

- TestPyPI upload
- PyPI publication
- PyPI project name claim
- No production-grade validation claim
- No formal convergence proof claim

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

Recommended current state: keep TestPyPI/PyPI pending while v1.0 readiness
engineering continues, unless maintainer explicitly approves TestPyPI.

This record does not authorize `twine upload`, TestPyPI upload, or PyPI
publication.
