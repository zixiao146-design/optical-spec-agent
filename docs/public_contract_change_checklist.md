# Public Contract Change Checklist

When modifying CLI, schema, adapter, workflow, examples, or package metadata,
check:

- Does this change affect a documented CLI command?
- Does this change affect a JSON output top-level key?
- Does this change affect a public schema field?
- Does this change affect adapter registry names?
- Does this change affect examples paths?
- Does this change affect `workflow-plan` public keys?
- Does this change require migration notes?
- Does this change require release notes?
- Does this change require updating `docs/public_contract_manifest.json`?
- Does this change require updating tests?

The v1.0 public contract freeze is maintainer-approved as of 2026-05-16.
Changes to the approved frozen public surface require maintainer approval.
Breaking changes require explicit migration notes, release notes, and public
contract manifest updates.

Preview/scaffold internals may still change when they are not documented as
frozen public surface.

external solver, external LLM, and proprietary solver dependencies must not
become default accidentally.
