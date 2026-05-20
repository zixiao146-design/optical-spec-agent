# rc9 PyPI Publication Decision Review

This review records why PyPI remains deferred during `0.9.0rc9.dev0`
development. It is not an upload approval record.

## Current status

- PyPI published: no
- PyPI approval: not granted
- TestPyPI only 0.9.0rc6.dev0 verified
- Current main dev: 0.9.0rc9.dev0
- Current public prerelease: v0.9.0rc8
- v0.9.0rc9 tag: not created
- v1.0.0 tag: not created
- Upload command authorized for PyPI: no
- Upload command authorized for TestPyPI: no

## Reasons to keep PyPI deferred

- The package is still pre-1.0.
- Backend scope has evolved quickly across rc7, rc8, and rc9 development.
- PyPI publication is permanent per version and cannot be treated as a scratch
  channel.
- Release distribution is currently GitHub prerelease only.
- PyPI publication must not imply production-grade validation.
- PyPI publication must not imply formal convergence proof or optical
  correctness.

## Reasons PyPI may be reconsidered

- v1.0 public contract freeze is approved for the documented surface.
- Release engineering, smoke checks, build checks, and quality gates are mature.
- TestPyPI Trusted Publishing was previously verified for 0.9.0rc6.dev0.
- Backend evidence is more mature after rc8.
- Optional solver evidence is documented with explicit preview and smoke
  boundaries.

## Required explicit decision paths

- GitHub-only continue: keep using GitHub prereleases and no PyPI upload.
- TestPyPI latest preflight/upload: requires explicit approval for the selected
  version and must not imply PyPI approval.
- PyPI pre-release publication: requires explicit PyPI approval and conservative
  release notes.
- PyPI stable only after v1.0.0 approval: requires v1.0.0 release approval,
  final versioning, release notes, and final verification.

## Current recommendation

Keep PyPI deferred. No upload command is authorized. Revisit this decision only
after a separate rc9/v1.0 decision review.
