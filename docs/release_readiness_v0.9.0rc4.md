# v0.9.0rc4 Development Readiness

## Baseline

- Current public prerelease: v0.9.0rc3
- v0.9.0rc3 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc3
- v0.9.0rc3 target commit: acc407df1822db99bed258b6165099f3e5c2e424
- Current main development version: 0.9.0rc4.dev0
- v0.9.0rc4 tag: not created
- PyPI/TestPyPI: not published / not uploaded

## Why main moved to 0.9.0rc4.dev0

`v0.9.0rc3` is already a published GitHub prerelease. Post-release commits on
`main` should not keep building as `0.9.0rc3`, because that version now refers
to the verified public candidate at commit `acc407d`.

`0.9.0rc4.dev0` marks post-rc3 development toward the next candidate.
`v0.9.0rc4.dev0` is not itself a public release.

## v0.9.0rc4 development goals

- TestPyPI gate dry-run foundation
- Packaging metadata hardening
- Wheel install smoke reliability
- v1.0 stability gate
- Optional external solver policy refinement
- Optional external LLM policy refinement
- Stronger offline example verification
- No PyPI/TestPyPI publication without explicit approval

## Required checks before future v0.9.0rc4 release draft

- `project.version` must be changed from `0.9.0rc4.dev0` to `0.9.0rc4`.
- `__version__` must match.
- `scripts/smoke_release.sh` passed.
- Wheel smoke passed.
- `pytest` passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- Dist filenames must contain `0.9.0rc4`.
- Release draft notes must exist.
- `v0.9.0rc4` tag must be absent before creation.
- PyPI/TestPyPI decision must be explicit.

## Non-goals

- Do not publish PyPI now.
- Do not upload TestPyPI now.
- Do not create `v0.9.0rc4` tag now.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
