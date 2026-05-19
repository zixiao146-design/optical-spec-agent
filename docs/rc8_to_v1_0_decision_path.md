# rc8.dev0 to v1.0 Decision Path

Current public prerelease: `v0.9.0rc7`.
Current main development version: `0.9.0rc8.dev0`.

This path keeps post-rc7 backend engineering separate from future `v0.9.0rc8`,
PyPI, and `v1.0.0` decisions.

## Gate 1: Continue rc8.dev0 Backend Engineering

Status: open and active.

Required posture:

- Keep package version at `0.9.0rc8.dev0` until a release draft is approved.
- Keep `v0.9.0rc8` tag absent.
- Keep `v1.0.0` tag absent.
- Keep PyPI unpublished.
- Keep TestPyPI upload for `0.9.0rc8.dev0` unperformed unless explicitly
  approved.
- Continue backend evidence hardening without overclaiming validation.

Recommended work:

- Close gaps from `docs/rc8_capability_gap_audit.md`.
- Keep roadmap classifications in `docs/rc8_backend_roadmap.md` current.
- Keep backend evidence pack and capability report passing.
- Keep public contract freeze stable.

## Gate 2: Decide Whether to Prepare a Future v0.9.0rc8 Draft

Status: not approved.

Before preparing a release draft, maintainers should confirm:

- Backend evidence smoke passes.
- Backend capability smoke passes.
- Adapter-native golden checker passes.
- Sub-agent audit passes.
- API fixtures pass.
- TestPyPI no-upload preflight passes.
- Quality gates, pytest, build, make check, normal smoke, and wheel smoke pass.
- `project.version` and `__version__` are ready to move from
  `0.9.0rc8.dev0` to `0.9.0rc8`.
- Release draft notes and readiness docs exist.
- `v0.9.0rc8` tag remains absent before creation.
- PyPI/TestPyPI decision remains explicit.

## Gate 3: Decide PyPI Publication Separately

Status: not granted.

PyPI publication remains independent from:

- GitHub prerelease creation.
- TestPyPI upload success.
- Backend evidence readiness.
- v1.0 public contract freeze approval.

Before any PyPI action:

- Use `docs/pypi_publication_decision.md`.
- Use `docs/pypi_publication_readiness_checklist.md`.
- Use `docs/pypi_post_publication_verification_plan.md`.
- Require explicit maintainer approval for the exact package version.

## Gate 4: Decide v1.0.0 Planning

Status: not approved.

`v1.0.0` planning can begin only after maintainers decide that:

- The frozen public contract remains acceptable.
- PyPI publication strategy is decided.
- rc8 backend gaps are either closed or explicitly deferred.
- Validation boundaries remain conservative.
- Elmer Level 3 remains deferred unless actual opt-in validation is completed.
- No production-grade physical validation claim is added.
- No formal convergence proof claim is added.

## Not Authorized by This Path

- Creating `v0.9.0rc8` tag.
- Creating any GitHub release.
- Uploading TestPyPI.
- Publishing PyPI.
- Creating `v1.0.0` tag or release.
- Moving existing tags.
- Running external solvers by default.
- Calling external LLMs by default.
- Marking Elmer as Level 3.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.

## Recommendation

Continue v1.0 readiness/backend engineering in `0.9.0rc8.dev0`, then revisit
the `v0.9.0rc8` release-draft decision only after the rc8 capability gaps are
reviewed and the standard evidence checks pass.
