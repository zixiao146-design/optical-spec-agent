# rc9 Go / No-go Matrix

This matrix records maintainer-facing next decisions for `0.9.0rc9.dev0`.
It does not approve tags, releases, TestPyPI upload, or PyPI publication.

| Decision | Current recommendation | Required approval | Blockers | Evidence status | Risk | Next action |
|---|---|---|---|---|---|---|
| Prepare v0.9.0rc9 release draft | Not yet | Maintainer release-draft approval | Need a substantive rc9 change or explicit decision | rc8 evidence closed; rc9 audit package in progress | Premature RC churn | Continue backend hardening |
| Publish TestPyPI | No | Explicit TestPyPI approval for selected version | Upload command not authorized | TestPyPI only 0.9.0rc6.dev0 verified | Confusing version channel | Keep no-upload preflight only |
| Publish PyPI | No | Explicit PyPI publication approval | PyPI decision not granted | PyPI checklist exists; package unpublished | Permanent public package claim | Keep PyPI deferred |
| Prepare v1.0.0 planning package | Possible later, not this task | Maintainer planning approval | v1.0.0 approval not granted | Public contract freeze approved | Over-committing before decision | Revisit after rc9 audit review |
| Create v1.0.0 release | No | Explicit v1.0.0 release approval | Final version, notes, verification missing | v1.0 readiness docs exist | Premature stable release | Do not create tag/release |
| Resume frontend polish | Optional future | Maintainer frontend-scope approval | Not a backend blocker | Local MVP and demo package exist | Distracting from backend readiness | Keep as future work |
| Continue backend hardening | Yes | Current maintainer direction is sufficient | None for docs/tests audit | Benchmarks, evidence, and gates exist | Low | Continue conservative backend work |

## Boundary

- No production-grade physical validation is claimed.
- No production-grade solver validation is claimed.
- No formal convergence proof is claimed.
- No optical correctness claim is made.
- Elmer remains deferred and not Level 3.
