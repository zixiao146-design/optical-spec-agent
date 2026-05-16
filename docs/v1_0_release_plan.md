# v1.0.0 Release Plan

## Release philosophy

v1.0.0 should stabilize the documented public contract and preserve conservative
claims. It should not imply production-grade physical validation, formal
convergence proof, default external solver execution, default external LLM
access, or proprietary solver support.

## Proposed release sequence

- Continue `0.9.0rc7.dev0` engineering.
- Continue local Agent API readiness without starting full frontend
  implementation.
- Keep API response models and `examples/api/` frontend fixtures aligned with
  endpoint behavior.
- Keep `api_contract_version` 0.1, request validation, and error fixtures
  documented while the API remains a frontend-readiness / candidate API.
- Decide PyPI publication path.
- Prepare v1.0.0 release draft.
- Run quality gates.
- Build distributions.
- Verify dist filenames.
- Create annotated `v1.0.0` tag only after explicit approval.
- Create GitHub release only after explicit approval.
- Optionally publish PyPI only after separate explicit approval.
- Add post-release status doc.

## Required release artifacts

- `docs/github_release_draft_v1.0.0.md`
- `docs/release_notes_v1.0.0.md`
- `docs/release_readiness_v1.0.0.md`
- `docs/post_release_status_v1.0.0.md` after release
- PyPI status doc if PyPI is published

## Explicit non-actions until approval

- No `v1.0.0` tag.
- No GitHub release.
- No PyPI publication.
- No TestPyPI upload.
- No claim expansion.
- No full frontend implementation unless separately approved.
- No PyPI publication trigger from API fixture readiness alone.
- No separate v1.0 API contract freeze unless maintainers explicitly approve it.
- No default external solver, external LLM, network, or proprietary dependency.
