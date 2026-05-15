# v1.0 Readiness Gap Audit

## Current baseline

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- v0.9.0rc6 tag: not created
- PyPI: not published
- TestPyPI: not uploaded
- TestPyPI upload approval: granted for 0.9.0rc6.dev0 only
- PyPI publication approval: not granted

## Strong areas

- Release engineering.
- Annotated tag / GitHub prerelease process.
- Post-release status process.
- Quality gates.
- TestPyPI no-upload preflight.
- Wheel install smoke.
- CLI examples.
- Offline user journey.
- Examples manifest.
- Public contract manifest.
- v1.0 public contract freeze checklist.
- Publication decision record.
- Open-source-solver-first strategy.
- Proprietary solver non-default policy.
- Adapter maturity evidence for Gmsh / Meep / MPB / Optiland.
- Python-aware solver preflight.

## Remaining gaps

- Elmer Level 3 validation deferred.
- TestPyPI upload approval granted for 0.9.0rc6.dev0 only; upload/install
  verification is the next TestPyPI evaluation step.
- The latest TestPyPI upload attempt failed with HTTP 403 Forbidden and is
  recorded in `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`.
- PyPI publication not approved.
- v1.0 final public contract freeze not finalized.
- `docs/v1_0_public_contract_freeze_checklist.md` exists but still needs
  maintainer confirmation before v1.0.
- `docs/publication_decision_record.md` authorizes TestPyPI only for
  `0.9.0rc6.dev0`; the first upload attempt failed with HTTP 403 Forbidden,
  and PyPI remains not granted.
- Production-grade physical validation not claimed.
- Formal convergence proof not claimed.
- Workflow remains local/synchronous preview.
- Adapter outputs may still be MVP/scaffold unless explicitly validated.

## Blocker classification

| Item | Classification | Rationale | Next action |
|---|---|---|---|
| PyPI decision | Hard blocker for v1.0 | v1.0 distribution must have an explicit publication decision, whether PyPI, GitHub-only, or delayed. | Record an explicit maintainer decision before v1.0. |
| TestPyPI upload | Soft blocker, possibly hard depending publication plan | TestPyPI is not required for GitHub-only prereleases, but it becomes a release confidence gate if PyPI publication is planned. | Approve, skip with documented reason, or keep deferred. |
| Elmer Level 3 | Deferred/non-blocker | Elmer remains Level 2 + Level-3-ready; missing ElmerSolver is documented and non-blocking for default gates. | Revisit only when a maintainable install route exists. |
| Production-grade physical validation | Deferred/non-blocker unless v1.0 claims production-grade validation | The project does not claim production-grade physical validation. | Keep claims conservative or define a separate validation program. |
| Formal convergence proof | Deferred/non-blocker unless explicitly claimed | The project does not claim a formal convergence proof. | Keep as a non-goal unless requirements change. |
| Public contract freeze | Hard blocker for v1.0 | CLI, schema, adapter, workflow, validation, and publication boundaries must be frozen or explicitly scoped before v1.0. | Finalize `docs/v1_0_public_contract_freeze.md` and manifest checks. |
| Quality gates | Already satisfied, must remain passing | Local quality gates, smoke, build, docs, and CLI checks are established. | Re-run before each RC or v1.0 transition. |
| Workflow preview | Future work unless final v1.0 claims expand | Workflow orchestration remains local/synchronous preview. | Keep scope clear or define future automation. |

## Recommended v1.0 path

- Finalize public contract freeze.
- Use `docs/v1_0_public_contract_freeze_checklist.md` as the executable
  freeze checklist.
- Keep production claims conservative.
- Decide TestPyPI upload explicitly through `docs/publication_decision_record.md`.
- Decide PyPI publication explicitly through `docs/publication_decision_record.md`.
- Keep Elmer deferred unless a maintainable install route appears.
- Prepare v0.9.0rc6 only if new hardening justifies another release candidate.
