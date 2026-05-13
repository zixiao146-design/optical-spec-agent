# Validation Gate

Version scope: current `main` development after the verified `v0.9.0rc2`
pre-release. Current main package version: `0.9.0rc3.dev0`.

## What must pass before a new RC

- `scripts/smoke_release.sh`
- `pytest`
- `make check`
- `python -m build`
- Documented offline CLI examples
- Packaging gate tests
- Adapter support matrix tests
- Workflow preview contract tests
- Release engineering checks
- Wheel install smoke if enabled

If wheel installation verification is enabled, run:

```bash
OSA_SMOKE_VERIFY_WHEEL=1 ./scripts/smoke_release.sh
```

## What physical validation currently means

Current tests validate local transformations, schemas, parser behavior,
diagnostics shape, generated artifacts, and sanity checks. They do not prove
production-grade physical correctness.

Physical diagnostics are preview/sanity aids unless a future document explicitly
defines a solver-backed validation standard. Default wavelength warnings mean a
local adapter default was applied and should be reviewed; they are not
production validation.

External solver validation remains optional/manual unless explicitly enabled by
maintainers.

## v0.9.0rc3 validation target

- Include contract tests from `d567660`.
- Include packaging gate tests from this sprint.
- Include optional wheel install smoke.
- Include documented CLI examples.
- Keep PyPI unpublished unless explicitly approved.
- Do not cut `v0.9.0rc3` until `project.version` is changed from
  `0.9.0rc3.dev0` to `0.9.0rc3` and final smoke passes.

## v1.0 validation target

- Define required physical validation standard.
- Define solver-backed validation plan.
- Define reproducibility expectations.
- Define supported adapter set.
- Define public API/CLI stability guarantees.
- Define what remains preview/scaffold after `v1.0`.
- Define release rollback policy.
- Define PyPI publication policy.
