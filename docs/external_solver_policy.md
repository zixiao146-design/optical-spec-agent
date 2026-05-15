# External Solver Policy

External solvers are not run by default. optical-spec-agent is
open-source-solver-first: the default route is local artifact preview and
offline evidence, not automatic solver execution.

Current public prerelease: `v0.9.0rc4`. Current main release draft:
`0.9.0rc5`. `v0.9.0rc5` release draft is not a public release, the `v0.9.0rc5` tag has
not been created, and PyPI/TestPyPI remain unpublished. Continue v1.0 readiness
engineering and prepare a `v0.9.0rc5` release draft only when accumulated
changes should be published as another RC.

## Default behavior

- Default tests do not require Meep, MPB, Gmsh, Elmer, or Optiland.
- Default CI should remain offline with respect to external solver execution.
- No solver, open-source or proprietary, is run by default in smoke or release
  validation.
- No proprietary license is required for tests, examples, smoke, or release
  validation.
- Adapters may generate scripts/configs for external solvers, but generation is
  not execution.
- Adapter family evidence fixtures cover local scaffold generation for Meep,
  Gmsh, Elmer, MPB, and Optiland; they do not execute those solvers.
- Generated artifacts are preview/scaffold unless solver-backed validation is
  performed and recorded.

## Open-source optional solvers vs proprietary tools

Open-source optional solvers may be used for optional/manual validation if they
are installed by the user. Current open-source-first adapter families are Meep,
MPB, Gmsh, Elmer, and Optiland.

Proprietary commercial tools, including Zemax, Lumerical, COMSOL, and
proprietary Ansys optics tools, are not default targets. Closed-source
commercial solver validation must be explicit, manual, non-default, and
separately documented. Future proprietary support, if any, should be
export-only by default and must not imply solver-backed correctness.

## Optional solver validation

Optional solver validation may be run manually by maintainers or users. If a
future automated optional gate is added, it should document:

- Required solver versions.
- Required environment variables or commands.
- Input fixtures and expected artifacts.
- Runtime expectations and skip behavior.
- Clear distinction from default CI.

The optional open-source solver validation path is tracked in
`docs/open_source_solver_validation_plan.md`. That plan does not make Meep,
Gmsh, Elmer, MPB, Optiland, or any other solver a default dependency.
The availability harness in `scripts/open_solver_validation_preflight.sh` only
uses command detection and does not execute solvers. Manual validation reports
should use `docs/manual_solver_validation_report_template.md`.

## Claims policy

No solver-specific physical claim should be made without evidence. In
particular:

- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No external solver validation is implied by adapter generation alone.

## Future gate guidance

External solver gates should be opt-in, clearly marked, and safe to skip in
default release engineering checks.
Pytest marker policy for optional solver validation is documented in
`docs/pytest_marker_policy.md`; default `pytest` remains no-solver.

## Offline journey and error handling

The default offline journey in `docs/offline_user_journey.md` and
`examples/e2e/` does not execute Meep, MPB, Gmsh, Elmer, Optiland, or any
proprietary solver. Missing optional solvers should not break documented
default examples. Local failure expectations are documented in
`docs/error_model.md`.
