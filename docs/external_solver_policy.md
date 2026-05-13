# External Solver Policy

External solvers are not run by default.

## Default behavior

- Default tests do not require Meep, MPB, Gmsh, Elmer, or Optiland.
- Default CI should remain offline with respect to external solver execution.
- Adapters may generate scripts/configs for external solvers, but generation is
  not execution.
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
