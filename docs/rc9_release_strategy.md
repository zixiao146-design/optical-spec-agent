# rc9 Release Strategy

`0.9.0rc9.dev0` is active development after the verified `v0.9.0rc8` GitHub
prerelease. It is not a public release.

## Strategy

- Keep main on `0.9.0rc9.dev0` while rc9 backend readiness work continues.
- Wait for a new substantive change or explicit maintainer decision before
  preparing a v0.9.0rc9 release draft.
- Do not create a v0.9.0rc9 tag now.
- Do not create a GitHub release now.
- Keep PyPI publication as a separate decision.
- Keep v1.0.0 planning and release approval as separate decisions.
- Track how rc9 differs from rc8 incrementally in readiness docs.

## Required checks before a future rc9 release draft

- Validation claim audit passed.
- Application benchmarks passed.
- Optional solver wrapper default no-execute passed.
- Backend evidence pack smoke passed.
- Backend capability/report smokes passed.
- Quality gates passed.
- Normal smoke passed.
- Wheel smoke passed.
- Pytest passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- Dist filenames contain `0.9.0rc9` only after the version is intentionally
  changed from `0.9.0rc9.dev0` to `0.9.0rc9`.

## Non-goals

- No TestPyPI upload now.
- No PyPI publication now.
- No tag or GitHub release now.
- No v1.0.0 release now.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No external solver or external LLM is required by default.
