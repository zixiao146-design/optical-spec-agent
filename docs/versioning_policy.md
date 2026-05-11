# Versioning Policy

This project separates package versions from main-branch preview capability.
That distinction is intentional because optical workflow features often land as
auditable scaffolds before they become formal releases.

## Status Labels

| Label | Meaning |
|---|---|
| Packaged version | The version in `pyproject.toml` and installed package metadata. |
| Formal GitHub release | A manually created tag/release. It may lag behind `main`. |
| Main branch preview capability | Implemented on `main`, tested locally/CI, but not necessarily tagged. |
| Release candidate | A main-branch capability that has draft notes and quality gates, but no release tag yet. |
| Draft release notes | Planning/review notes only. They do not imply a release exists. |

## Current Policy For 0.x

- `0.x` releases may add capabilities quickly, but user-visible contracts should
  stay documented and test-covered.
- Breaking schema changes require explicit release notes and schema stability
  documentation.
- The default parser remains rule-based unless a release explicitly changes it.
- External solvers and external LLM providers are optional/manual unless a future
  release says otherwise.

## README Language Rules

- A packaged version must not be described as containing unreleased main-branch
  preview work.
- Main-branch capabilities should be called preview, scaffold, evaluation, or
  release-candidate work until a formal tag exists.
- Adapter scaffolds, diagnostics, workflow reports, and mock LLM evaluation must
  not be described as production solver results.
- Release notes must say "Draft" unless a tag/release has actually been created.

## Version Bump Options

- Option A: keep `pyproject.toml` at `0.5.0` and label v0.6-v0.9 work as
  unreleased main-branch preview. This is conservative and avoids implying a
  formal release has shipped.
- Option B: bump to `0.8.0` when parser foundation is the next intended package
  release. This highlights the LLM parser milestone but leaves workflow work as
  preview.
- Option C: bump to `0.9.0` when workflow orchestration is intended to ship as
  the next formal release and all release-readiness gates are accepted.

Do not create release tags or GitHub releases from automation in this repo.
