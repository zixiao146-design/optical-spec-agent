# Validation Gate

Version scope: current public prerelease `v0.9.0rc3`; current `main`
development version `0.9.0rc4.dev0`. `v0.9.0rc4.dev0` is not a release, the
`v0.9.0rc4` tag has not been created, and PyPI/TestPyPI remain unpublished.
Continue v1.0 readiness engineering and prepare a `v0.9.0rc4` release draft
only when accumulated changes should be published as another RC.

The validation strategy is open-source-solver-first. Proprietary solvers are not
default dependencies, and no proprietary license is required for default tests,
smoke, examples, or release validation.

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

## v0.9.0rc4 validation target

- Include contract tests from `d567660`.
- Include packaging gate tests from this sprint.
- Include TestPyPI dry-run gate checks.
- Include v1.0 stability gate checks.
- Include offline examples evidence from `examples/README.md`.
- Include adapter evidence fixtures for preview/scaffold outputs.
- Include expanded adapter family evidence for Gmsh, Elmer, MPB, and Optiland.
- Include workflow evidence fixtures for deterministic local replay.
- Include workflow-to-adapter planning evidence with no-execute behavior.
- Include schema compatibility policy checks.
- Include failure-mode regression for documented invalid inputs.
- Include optional wheel install smoke.
- Include documented CLI examples.
- Keep PyPI unpublished unless explicitly approved.
- Keep TestPyPI not uploaded unless explicitly approved.
- Do not create the `v0.9.0rc4` tag until project/version consistency, final
  smoke, wheel smoke, build, `make check`, and CLI examples pass.
- Adapter family evidence does not replace optional/manual external solver
  validation.
- No proprietary solver validation is part of the default gate.

## v1.0 validation target

- Define required physical validation standard.
- Define solver-backed validation plan.
- Define reproducibility expectations.
- Define supported adapter set.
- Define public API/CLI stability guarantees.
- Define what remains preview/scaffold after `v1.0`.
- Define release rollback policy.
- Define PyPI publication policy.
