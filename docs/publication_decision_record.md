# Publication Decision Record

## Current status

- Current public prerelease: v0.9.0rc5
- Current main release draft: v0.9.0rc6
- TestPyPI uploaded: yes, for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc6: not performed
- PyPI published: no
- TestPyPI upload approval for 0.9.0rc6: pending
- PyPI publication approval: not granted
- Upload command authorized for 0.9.0rc6: no
- Latest TestPyPI upload attempt:
  `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`
- Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden
- TestPyPI Trusted Publishing status:
  `docs/testpypi_status_v0.9.0rc6.dev0.md`
- TestPyPI Trusted Publishing result: completed
- TestPyPI clean install verification: passed
- TestPyPI Trusted Publishing workflow:
  `.github/workflows/testpypi-trusted-publish.yml`
- TestPyPI Trusted Publishing workflow status: passed for 0.9.0rc6.dev0
- PyPI publication readiness checklist:
  `docs/pypi_publication_readiness_checklist.md`
- PyPI post-publication verification plan:
  `docs/pypi_post_publication_verification_plan.md`
- v1.0 public contract freeze: approved
- v1.0 public contract freeze status:
  `docs/v1_0_public_contract_freeze_status.md`

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

- Upload to TestPyPI only. Completed for `0.9.0rc6.dev0` through Trusted
  Publishing.
- Verify clean install from TestPyPI. Completed for `0.9.0rc6.dev0`; see
  `docs/testpypi_status_v0.9.0rc6.dev0.md`.
- Do not publish PyPI.

### Path C

- Upload to TestPyPI.
- Verify.
- Then separately approve PyPI publication.

## Required before Future TestPyPI Upload

- Explicit maintainer approval.
- Trusted Publishing configuration or a valid TestPyPI token.
- No-upload preflight passed.
- Quality gates passed.
- Version/tag strategy understood.
- Post-TestPyPI verification plan ready.

## Required before PyPI publication

- Explicit maintainer approval.
- TestPyPI completed or explicit skip recorded.
- PyPI token available.
- Final version chosen and not previously uploaded to PyPI.
- Quality gates, CI, build, and `twine check` passed.
- README, package metadata, and release notes reviewed.
- Yanking/rollback policy reviewed.
- Production/validation claims reviewed.
- Post-publication verification plan prepared.
- Release notes final.

## Current recommendation

Recommended current state: keep PyPI publication separately gated while v1.0
readiness engineering continues. TestPyPI upload and clean-install verification
are completed for `0.9.0rc6.dev0`, and the v1.0 public contract freeze is
approved; these do not authorize PyPI publication, tag creation, or GitHub
release creation.

Use `docs/pypi_publication_readiness_checklist.md` and
`docs/pypi_post_publication_verification_plan.md` before any future PyPI
approval. The current recommendation is: do not publish PyPI yet; decide PyPI
publication timing separately after reviewing the approved freeze package.

The earlier local token-based TestPyPI upload attempt failed with HTTP 403
Forbidden and remains recorded in
`docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`. The successful path was the
manual TestPyPI Trusted Publishing workflow documented in
`docs/testpypi_trusted_publishing.md` and recorded in
`docs/testpypi_status_v0.9.0rc6.dev0.md`.

Dependency-index caveat: a naive install using TestPyPI as the primary package
index failed because TestPyPI contains an unrelated `FASTAPI` package that can
shadow the real `fastapi` dependency. The successful verification installed
runtime dependencies from PyPI and installed `optical-spec-agent` from TestPyPI
with `--no-deps`.

This record authorizes TestPyPI upload only for `0.9.0rc6.dev0`. It does not
authorize PyPI publication, GitHub release creation, tag creation, production-
grade validation claims, or formal convergence proof claims.
