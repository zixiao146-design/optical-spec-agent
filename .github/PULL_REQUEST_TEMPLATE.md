## Summary

Brief description of what this PR does and why.

## Changes

- item 1
- item 2

## Files changed

- `path`: why it changed

## Test plan

- [ ] `make check` passes
- [ ] `make docs-check` / `make cli-check` run if docs or CLI changed
- [ ] `make release-check` run if release/readiness files changed
- [ ] `make lint` clean, or lint debt is explicitly out of scope
- [ ] Golden cases reviewed if parser changed: `python benchmarks/run_benchmark.py --mode exact`
- [ ] New tests added (if applicable)

## Release and safety checklist

- [ ] Benchmarks affected? Explain impact.
- [ ] Docs updated for user-visible behavior.
- [ ] No production-grade physical validation claim introduced.
- [ ] Default tests do not require Meep or external solvers.
- [ ] Default tests do not require an external LLM provider.
- [ ] Release note or changelog entry needed?
