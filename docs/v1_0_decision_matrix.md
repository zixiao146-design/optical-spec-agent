# v1.0 Decision Matrix

## TestPyPI upload

- Current: granted for 0.9.0rc6.dev0 only
- Record: `docs/publication_decision_record.md`
- Options:
  - Approve upload.
  - Continue no-upload.
  - Skip with documented reason.
- Impact: decides whether package publication confidence includes a real
  TestPyPI exercise before v1.0, without authorizing PyPI publication by itself.
- Latest attempt: failed with HTTP 403 Forbidden; retry requires a TestPyPI
  token with sufficient upload/create-project permissions.

## PyPI publication

- Current: not approved
- Record: `docs/publication_decision_record.md`
- Options:
  - Publish after TestPyPI.
  - Delay.
  - GitHub-only release.
- Impact: determines whether v1.0 is distributed through PyPI or remains a
  GitHub release artifact until a later approval.

## Elmer Level 3

- Current: deferred
- Record: `docs/v1_0_public_contract_freeze_checklist.md`
- Options:
  - Keep deferred.
  - Run on Linux/Docker/remote environment.
  - Wait for maintainable macOS ARM package.
- Impact: affects adapter maturity completeness, but it is not a default gate
  because Elmer is not a default dependency and no production-grade physical
  validation is claimed.

## Production-grade physical validation

- Current: not claimed
- Record: `docs/v1_0_public_contract_freeze_checklist.md`
- Options:
  - Keep non-goal for v1.0.
  - Define separate validation program.
- Impact: controls project positioning and prevents optional narrow solver
  evidence from being overread as production-grade physical validation.

## Public contract freeze

- Current: candidate
- Checklist: `docs/v1_0_public_contract_freeze_checklist.md`
- Options:
  - Freeze before v1.0.
  - Allow further pre-v1 changes.
- Impact: determines whether CLI, schema, adapter, workflow, validation, and
  publication boundaries are stable enough to call the next milestone v1.0.

Public contract freeze remains a hard blocker until the maintainer confirms
the checklist. TestPyPI is authorized only for `0.9.0rc6.dev0`; PyPI publication remains not granted, Elmer remains deferred/non-blocking,
production-grade physical validation remains a non-goal unless explicitly
claimed, and formal convergence proof remains a non-goal unless explicitly
claimed.
