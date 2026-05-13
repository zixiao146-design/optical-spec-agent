# External Solver Policy

External solvers are not run by default.

Current public prerelease: `v0.9.0rc3`. Current main development version:
`0.9.0rc4.dev0`. `v0.9.0rc4.dev0` is not a release, the `v0.9.0rc4` tag has
not been created, and PyPI/TestPyPI remain unpublished. Continue v1.0 readiness
engineering and prepare a `v0.9.0rc4` release draft only when accumulated
changes should be published as another RC.

## Default behavior

- Default tests do not require Meep, MPB, Gmsh, Elmer, or Optiland.
- Default CI should remain offline with respect to external solver execution.
- Adapters may generate scripts/configs for external solvers, but generation is
  not execution.
- Adapter family evidence fixtures cover local scaffold generation for Meep,
  Gmsh, Elmer, MPB, and Optiland; they do not execute those solvers.
- Generated artifacts are preview/scaffold unless solver-backed validation is
  performed and recorded.

## Optional solver validation

Optional solver validation may be run manually by maintainers or users. If a
future automated optional gate is added, it should document:

- Required solver versions.
- Required environment variables or commands.
- Input fixtures and expected artifacts.
- Runtime expectations and skip behavior.
- Clear distinction from default CI.

## Claims policy

No solver-specific physical claim should be made without evidence. In
particular:

- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No external solver validation is implied by adapter generation alone.

## Future gate guidance

External solver gates should be opt-in, clearly marked, and safe to skip in
default release engineering checks.
