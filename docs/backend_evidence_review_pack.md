# Backend Evidence Review Pack

The backend evidence review pack is a maintainer-facing summary of what the
local backend actually proves today. It is a preview/design-assist review
artifact. It is not production-grade physical validation, does not claim a
formal convergence proof, and does not execute external solvers.

## Generate the Pack

```bash
python scripts/generate_backend_evidence_pack.py \
  --json-out /tmp/osa-backend-evidence-pack.json \
  --markdown-out /tmp/osa-backend-evidence-pack.md
```

The generated `/tmp` files are review artifacts and should not be committed by
default.

## Smoke Check

```bash
./scripts/smoke_backend_evidence_pack.sh
```

The smoke script verifies that the generated JSON and Markdown include the
expected sections and safety markers.

## Review Decision

The maintained review decision is recorded in
[`backend_evidence_review_decision.md`](backend_evidence_review_decision.md).
That decision records backend evidence as sufficient to prepare a
`v0.9.0rc7` release draft, while keeping `v0.9.0rc7` tag creation, GitHub
release creation, PyPI publication, TestPyPI upload, and `v1.0.0` release
approval separate and not granted.

## Sections

- Package and release status: current public prerelease, main development
  version, PyPI/TestPyPI state, and no tag/release actions.
- Sub-agent reality: whether each deterministic backend role exists and runs in
  a sample session.
- Tool-call reality: internal tools executed, calculator tools executed, and
  blocked external actions.
- Optical calculators: thin-film, paraxial, Gaussian beam, and waveguide
  preview calculators with sanity reference cases and failure modes.
- Design-case cross-checks: optical design examples mapped to expected
  calculators, adapters, and tool-call ledger entries.
- Source / monitor / observable diagnostics: deterministic inference,
  missing-input diagnostics, observable taxonomy, and adapter-native mapping.
- Adapter-native golden coverage: Meep, MPB, Gmsh, Elmer, and Optiland golden
  preview cases with metadata, fragment, and safety checks.
- Blocked or deferred capabilities: external solver execution, external LLM,
  publication, tag/release, Elmer Level 3, production-grade validation, and
  formal convergence proof.
- Maintainer review questions: prompts for deciding what to review or deepen
  next.

## Interpreting Status

`pass` means the local deterministic evidence matched the expected preview
contract. `warn` means a capability is intentionally partial or deferred. `fail`
means a local evidence check did not match the expected contract.

## Limitations

- No external solver is executed by default.
- No external LLM is called by default.
- No TestPyPI/PyPI upload is performed.
- No Git tag or GitHub release is created.
- Adapter-native monitor metadata is preview-only and is not a real solver
  monitor result.
- Calculator outputs are sanity-checked preview/design-assist results, not
  production-grade physical validation.
