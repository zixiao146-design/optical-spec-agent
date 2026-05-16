# v1.0 Decision Matrix

## TestPyPI upload

- Current: completed for 0.9.0rc6.dev0
- Record: `docs/publication_decision_record.md`
- Status: `docs/testpypi_status_v0.9.0rc6.dev0.md`
- Options:
  - Keep the completed 0.9.0rc6.dev0 TestPyPI upload as evidence.
  - Approve a future TestPyPI upload for a later candidate.
  - Skip future TestPyPI upload with documented reason.
- Impact: decides whether package publication confidence includes a real
  TestPyPI exercise before v1.0, without authorizing PyPI publication by itself.
- Latest result: GitHub Actions Trusted Publishing passed for 0.9.0rc6.dev0,
  and clean install verification passed. The earlier local token attempt failed
  with HTTP 403 Forbidden and remains a historical record.
- Dependency-index caveat: the successful verification installed dependencies
  from PyPI and installed `optical-spec-agent` from TestPyPI with `--no-deps`
  because TestPyPI contains an unrelated `FASTAPI` package.

## PyPI publication

- Current: not approved
- Record: `docs/publication_decision_record.md`
- Readiness checklist: `docs/pypi_publication_readiness_checklist.md`
- Post-publication verification plan:
  `docs/pypi_post_publication_verification_plan.md`
- Options:
  - Publish after TestPyPI.
  - Delay.
  - GitHub-only release.
- Impact: determines whether v1.0 is distributed through PyPI or remains a
  GitHub release artifact until a later approval.
- Current recommendation: do not publish PyPI yet. Continue v1.0 readiness
  engineering and prepare PyPI only after the public contract freeze is
  confirmed.

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
- Confirmation package: `docs/v1_0_public_contract_freeze_confirmation.md`
- Frozen surface candidate: `docs/v1_0_contract_frozen_surface.md`
- Non-goals: `docs/v1_0_contract_non_goals.md`
- Breaking change policy: `docs/v1_0_breaking_change_policy.md`
- Maintainer confirmation: pending
- Options:
  - Freeze before v1.0.
  - Allow further pre-v1 changes.
- Impact: determines whether CLI, schema, adapter, workflow, validation, and
  publication boundaries are stable enough to call the next milestone v1.0.

Public contract freeze remains a hard blocker until the maintainer confirms
the checklist. TestPyPI is completed for `0.9.0rc6.dev0`; PyPI publication
remains not granted and is tracked by the PyPI publication readiness checklist,
Elmer remains deferred/non-blocking,
production-grade physical validation remains a non-goal unless explicitly
claimed, and formal convergence proof remains a non-goal unless explicitly
claimed.
