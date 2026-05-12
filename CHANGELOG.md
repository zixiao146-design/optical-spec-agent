# Changelog

This changelog distinguishes formal packaged releases from draft main-branch
work. See `docs/versioning_policy.md` for status definitions.

## 0.9.0rc1 candidate

- v0.6-style local diagnostics via `optical-spec diagnose`.
- v0.7-style adapter registry and MPB/Gmsh/Elmer/Optiland MVP scaffold
  generation.
- v0.8-style rule/LLM/hybrid parser foundation with deterministic mock
  provider and LLM benchmark.
- v0.9-style synchronous local workflow orchestration, replay, reports, and
  workflow benchmark.
- Release-engineering checks for CLI surface, docs consistency, artifact
  contracts, and release readiness.

This candidate has not been tagged or published yet. It remains pending manual
maintainer approval for a GitHub release and any PyPI publication.

## v0.5.0

- Meep execution harness baseline.
- Structured `ExecutionResult`.
- `meep-check` and `meep-run`.
- Auditable artifacts such as `stdout.txt`, `stderr.txt`,
  `execution_result.json`, and `run_manifest.json`.

## Earlier Draft Notes

See:

- `docs/release_notes_v0.2.0.md`
- `docs/release_notes_v0.5.0.md`
- `docs/release_notes_v0.7.0.md`
- `docs/release_notes_v0.8.0.md`
- `docs/release_notes_v0.9.0.md`
