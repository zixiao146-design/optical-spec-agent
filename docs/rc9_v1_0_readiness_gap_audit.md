# rc9 v1.0 Readiness Gap Audit

This audit records the post-v0.9.0rc8 state of `main` and separates v1.0
readiness evidence from release, PyPI, and production-validation decisions.

## Current state

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- PyPI: not published
- TestPyPI: only 0.9.0rc6.dev0 uploaded/verified
- v0.9.0rc9 tag: not created
- v1.0.0 tag: not created
- v1.0 public contract freeze: approved
- Application domain benchmarks: 19 pass / 0 warn / 0 fail
- Optional solver evidence loop closed for Gmsh, Optiland, Meep, and MPB
- Elmer remains deferred and not Level 3

## Stable enough for v1.0 consideration

- CLI/API public contract freeze is approved for the documented surface.
- No-network examples and local API fixtures remain part of the default evidence.
- Backend evidence pack and backend capability report are available.
- Application domain benchmarks cover positive, ambiguous, underconstrained,
  unsupported, and blocked/unsafe requests.
- Material provenance and material-suitability diagnostics are documented.
- Validation maturity boundaries and preview boundary policy are explicit.
- Optional solver smoke evidence exists for Gmsh, Optiland, Meep, and MPB.
- Elmer deferred status is clearly documented and is not upgraded to Level 3.

## Remaining hard blockers

- Explicit v1.0.0 release approval is not granted.
- PyPI publication decision is not granted.
- Final v1.0.0 version is not set.
- Final v1.0.0 release notes are not prepared.
- Final v1.0.0 release verification has not been run.

## Remaining soft blockers

- TestPyPI for the latest version may be optionally repeated or skipped only by
  explicit maintainer decision.
- Frontend/demo polish remains useful but is not a backend blocker.
- Elmer Level 3 remains deferred but non-blocking if the deferral stays
  visible in release notes, scorecards, and readiness docs.
- Additional analytic reference cases may improve confidence but are not a
  prerequisite for maintaining the current preview/design-assist boundary.

## Non-blockers / deferred

- No production-grade physical validation is claimed.
- No production-grade solver validation is claimed.
- No formal convergence proof is claimed.
- No optical correctness claim is made.
- Elmer Level 3 remains deferred.
- Proprietary solver integration remains non-default/export-only.
- External LLM usage remains optional and not required by default.
- PyPI publication remains separately gated until explicitly approved.

## Recommendation

Continue rc9.dev0 readiness/backend engineering. Do not prepare v1.0.0 without
separate approval, and review the PyPI decision as its own gate before any
upload command is authorized.
