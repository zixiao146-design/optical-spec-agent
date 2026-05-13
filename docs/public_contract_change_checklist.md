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

Before v1.0, breaking changes are allowed but should be documented. After v1.0,
public contract changes should be more conservative.

external solver, external LLM, and proprietary solver dependencies must not
become default accidentally.
