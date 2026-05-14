# Manual Solver Validation Report Template

- Date:
- Maintainer:
- Project version:
- Git commit:
- Adapter family:
- Solver name:
- Solver version:
- Solver installation method:
- Input fixture:
- Generated artifact:
- Command run manually:
- Expected high-level result:
- Observed result:
- Diagnostics:
- Pass/fail:
- Limitations:
- Whether this supports any release note claim:
- Whether this supports production-grade validation: no by default
- Whether this should be included in release notes:

Filling this template does not by itself imply production-grade validation.
Manual validation is optional and not part of default CI.

Proprietary tools should not use this template unless separately approved as
export-only/manual evidence. Export-only/manual evidence must not imply
solver-backed correctness unless the actual solver-backed validation is
explicitly recorded.

The Gmsh-specific pilot template is
`docs/manual_solver_validation_reports/gmsh_validation_pilot_template.md`.

The Meep-specific report schema is
`docs/manual_solver_validation_reports/meep_validation_report_schema.json`.

The MPB-specific report schema is
`docs/manual_solver_validation_reports/mpb_validation_report_schema.json`.
