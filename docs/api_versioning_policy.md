# Local Agent API Versioning Policy

## Current status

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- Local Agent API status: frontend-readiness / candidate API
- Frontend implementation: not started
- PyPI: not published

## API contract version

- `api_contract_version`: "0.1"
- `package_version`: "0.9.0rc7.dev0"

The package version tracks Python package releases. The
`api_contract_version` tracks the frontend/API request and response shape.

The Local Agent API is not yet a separately frozen v1.0 API contract unless a
maintainer explicitly approves freezing it.

## Versioning rules

- Backward-compatible additions may occur in `api_contract_version` 0.1.
- Removing or renaming fields requires a new API contract version or explicit
  migration note.
- Safety flags must remain present and conservative.
- Preview endpoints may evolve but must remain documented.
- Breaking API changes require updates to `docs/api_migration_notes.md`.

## Current API guarantees

- No external solver by default.
- No external LLM by default.
- No proprietary solver by default.
- No production-grade validation claim.
- No formal convergence proof claim.
