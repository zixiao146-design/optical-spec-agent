# v0.9.0rc6 Release Draft Readiness

## Baseline

- Current public prerelease: v0.9.0rc5
- v0.9.0rc5 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc5
- Current main release draft: v0.9.0rc6
- v0.9.0rc6 tag: not created
- GitHub release: not created
- v1.0.0: not released
- PyPI: not published
- PyPI publication approval: not granted
- TestPyPI uploaded and verified for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc6: not performed
- v1.0 public contract freeze: approved

## Included Post-rc5 Hardening

- TestPyPI Trusted Publishing verification for 0.9.0rc6.dev0.
- Clean install from TestPyPI for 0.9.0rc6.dev0.
- TestPyPI dependency-index caveat documented.
- CI workflow gates stabilized.
- v1.0 public contract freeze approved.
- PyPI publication readiness checklist.
- PyPI post-publication verification plan.
- Publication decision boundaries.
- Adapter maturity maintained.
- No-overclaim validation boundaries preserved.

## Required Checks Before Tag Creation

- Git status clean.
- `project.version == 0.9.0rc6`.
- `optical_spec_agent.__version__ == 0.9.0rc6`.
- `v0.9.0rc6` tag absent.
- Quality gates passed.
- TestPyPI no-upload preflight passed.
- Smoke passed.
- Wheel smoke passed.
- Pytest passed.
- Build passed.
- `make check` passed.
- CLI examples passed.
- Dist filenames contain `0.9.0rc6`.
- No PyPI upload.
- No TestPyPI upload for rc6.
- No tag/release until approval.

## Release Draft Scope

- This draft packages the approved v1.0 public contract freeze and the
  successful 0.9.0rc6.dev0 TestPyPI Trusted Publishing verification.
- TestPyPI verification applies to `0.9.0rc6.dev0`; the `0.9.0rc6` release
  draft has not been uploaded to TestPyPI.
- PyPI publication remains separately gated and not approved.
- Elmer remains Level 2 + Level-3-ready with installation deferred.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- External solvers, external LLM providers, and proprietary solvers are not
  default dependencies.

## Next Step

- After maintainer approval, create annotated `v0.9.0rc6` tag.
- Create GitHub prerelease.
- Verify `draft=false` and `prerelease=true`.
- Add `docs/post_release_status_v0.9.0rc6.md`.
- Do not publish PyPI unless separately approved.
