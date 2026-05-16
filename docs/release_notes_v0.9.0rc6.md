# Release Notes: v0.9.0rc6

## Summary

v0.9.0rc6 is the sixth release candidate for v0.9.0. It packages the
post-v0.9.0rc5 readiness work around TestPyPI Trusted Publishing, v1.0 public
contract freeze approval, PyPI publication readiness, and conservative
validation boundaries.

## Highlights

- TestPyPI Trusted Publishing completed for `0.9.0rc6.dev0`.
- Clean install from TestPyPI passed for `0.9.0rc6.dev0`.
- CI and GitHub Actions workflow gates were stabilized.
- v1.0 public contract freeze is approved and recorded.
- PyPI publication readiness checklist was added.
- PyPI post-publication verification plan was added.
- Publication decision boundaries remain explicit.

## TestPyPI Trusted Publishing Status

- TestPyPI uploaded and verified for `0.9.0rc6.dev0`: yes.
- TestPyPI upload for `0.9.0rc6`: not performed.
- The `0.9.0rc6.dev0` TestPyPI status record is
  `docs/testpypi_status_v0.9.0rc6.dev0.md`.

## v1.0 Public Contract Freeze Status

- v1.0 public contract freeze: approved.
- Freeze status record: `docs/v1_0_public_contract_freeze_status.md`.
- This freeze does not publish PyPI, create a tag, create a GitHub release, or
  release `v1.0.0`.

## PyPI Publication Readiness

- PyPI published: no.
- PyPI publication approval: not granted.
- PyPI readiness checklist: `docs/pypi_publication_readiness_checklist.md`.
- PyPI post-publication verification plan:
  `docs/pypi_post_publication_verification_plan.md`.

## Adapter Maturity

- Gmsh: Level 3.
- Meep: Level 3.
- MPB: Level 3.
- Optiland: Level 3.
- Elmer: Level 2 + Level-3-ready, install deferred.

## Verification

- quality gates: passed
- TestPyPI no-upload preflight: passed
- normal smoke: passed
- wheel smoke: passed
- pytest: passed
- python -m build: passed
- make check: passed
- CLI examples: passed
- dist files:
  - optical_spec_agent-0.9.0rc6-py3-none-any.whl
  - optical_spec_agent-0.9.0rc6.tar.gz

## Scope Limitations

- No PyPI publish.
- No TestPyPI upload for `0.9.0rc6`.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Proprietary solvers are not required by default.
- Elmer Level 3 validation remains deferred.

## PyPI/TestPyPI Status

- TestPyPI contains `0.9.0rc6.dev0`.
- PyPI remains unpublished.
- PyPI publication remains separately gated.

## Tag / Release Note

- `v0.9.0rc6` tag: not created yet.
- GitHub release for `v0.9.0rc6`: not created yet.
