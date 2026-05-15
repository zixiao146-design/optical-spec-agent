# v1.0 Decision Matrix

## TestPyPI upload

- Current: pending
- Options:
  - Approve upload.
  - Continue no-upload.
  - Skip with documented reason.
- Impact: decides whether package publication confidence includes a real
  TestPyPI exercise before v1.0, without authorizing PyPI publication by itself.

## PyPI publication

- Current: not approved
- Options:
  - Publish after TestPyPI.
  - Delay.
  - GitHub-only release.
- Impact: determines whether v1.0 is distributed through PyPI or remains a
  GitHub release artifact until a later approval.

## Elmer Level 3

- Current: deferred
- Options:
  - Keep deferred.
  - Run on Linux/Docker/remote environment.
  - Wait for maintainable macOS ARM package.
- Impact: affects adapter maturity completeness, but it is not a default gate
  because Elmer is not a default dependency and no production-grade physical
  validation is claimed.

## Production-grade physical validation

- Current: not claimed
- Options:
  - Keep non-goal for v1.0.
  - Define separate validation program.
- Impact: controls project positioning and prevents optional narrow solver
  evidence from being overread as production-grade physical validation.

## Public contract freeze

- Current: candidate
- Options:
  - Freeze before v1.0.
  - Allow further pre-v1 changes.
- Impact: determines whether CLI, schema, adapter, workflow, validation, and
  publication boundaries are stable enough to call the next milestone v1.0.
