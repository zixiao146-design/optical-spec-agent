# Validation Gate

Version scope: current public prerelease `v0.9.0rc4`; current `main`
development version `0.9.0rc5.dev0`. `v0.9.0rc5.dev0` is not a release, the
`v0.9.0rc5` tag has not been created, and PyPI/TestPyPI remain unpublished.
Continue v1.0 readiness engineering and prepare a `v0.9.0rc5.dev0` development version
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

## v0.9.0rc5.dev0 validation target

- Include contract tests from `d567660`.
- Include packaging gate tests from this sprint.
- Include TestPyPI dry-run gate checks.
- Include v1.0 stability gate checks.
- Include offline examples evidence from `examples/README.md`.
- Include adapter evidence fixtures for preview/scaffold outputs.
- Track adapter maturity with `docs/adapter_maturity_model.md`.
- Keep the Gmsh optional validation pilot opt-in only; default validation does
  not run Gmsh.
- Include the 2026-05-14 Gmsh Level 3 optional manual validation report as
  narrow evidence only; do not make Gmsh a default gate.
- Keep the Meep optional validation pilot opt-in only; default validation does
  not run Meep.
- Include the 2026-05-14 Meep Level 3 optional manual validation report as
  narrow evidence only; do not make Meep a default gate.
- Keep the MPB optional validation pilot opt-in only; default validation does
  not run MPB and does not require MPB CLI.
- Include the 2026-05-14 MPB Level 3 optional manual validation report as
  narrow evidence only; do not make MPB a default gate.
- Keep the Optiland optional validation pilot opt-in only; default validation
  does not run Optiland.
- Include the 2026-05-14 Optiland Level 3 optional manual validation report as
  narrow evidence only; do not make Optiland a default gate.
- Include expanded adapter family evidence for Gmsh, Elmer, MPB, and Optiland.
- Include workflow evidence fixtures for deterministic local replay.
- Include workflow-to-adapter planning evidence with no-execute behavior.
- Include schema compatibility policy checks.
- Include v1.0 compatibility policy checks.
- Include validation evidence manifest checks.
- Include examples manifest checks.
- Include offline user journey evidence from `docs/offline_user_journey.md` and
  `examples/e2e/`.
- Include error model checks from `docs/error_model.md`.
- Include pre-v1 migration notes from `docs/migration_notes_pre_v1.md`.
- Include public contract freeze candidate checks from
  `docs/v1_0_public_contract_freeze.md`, `docs/public_contract_manifest.json`,
  and `docs/public_contract_change_checklist.md`.
- Include optional open-source solver validation plan checks.
- Include optional open-source solver validation preflight checks that detect
  solver availability without executing solvers.
- Keep manual solver validation reports separate from default release gates.
- Include failure-mode regression for documented invalid inputs.
- Include optional wheel install smoke.
- Include documented CLI examples.
- Keep PyPI unpublished unless explicitly approved.
- Keep TestPyPI not uploaded unless explicitly approved.
- Do not create the `v0.9.0rc5` tag until project/version consistency, final
  smoke, wheel smoke, build, `make check`, and CLI examples pass.
- Adapter family evidence does not replace optional/manual external solver
  validation.
- No proprietary solver validation is part of the default gate.
- `scripts/open_solver_validation_preflight.sh` must remain no-execution and
  safe when solvers are unavailable.
- Current public prerelease remains `v0.9.0rc4`, current main development
  version remains `0.9.0rc5.dev0`, the `v0.9.0rc5` tag has not been created,
  and PyPI/TestPyPI remain unpublished/not uploaded.

## v1.0 validation target

- Define required physical validation standard.
- Define solver-backed validation plan.
- Define reproducibility expectations.
- Define supported adapter set.
- Define public API/CLI stability guarantees.
- Define what remains preview/scaffold after `v1.0`.
- Define release rollback policy.
- Define PyPI publication policy.
