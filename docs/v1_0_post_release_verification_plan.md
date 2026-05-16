# v1.0.0 Post-release Verification Plan

## Required checks

- Verify GitHub tag target.
- Verify annotated tag object.
- Verify GitHub release `draft=false`.
- Verify GitHub release is `prerelease=false` or final release state,
  depending on maintainer decision.
- Verify release notes match the local draft.
- Clean install from GitHub source if applicable.
- Clean install from PyPI if PyPI is published.
- Run import version check.
- Run `optical-spec --help`.
- Run `optical-spec adapter-list --json`.
- Run validate / parse / workflow-plan examples.
- Add post-release status doc.
- Add PyPI status doc if applicable.
- Ensure no production-grade physical validation claim was added.
- Ensure no formal convergence proof claim was added.

## Publication boundary

This plan does not authorize tag creation, GitHub release creation, TestPyPI
upload, or PyPI publication. It only defines the verification work required
after a separately approved release or publication.

