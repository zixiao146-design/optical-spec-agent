# Draft Release Notes v0.6

Draft only. This document summarizes the v0.6 local diagnostics work on main.

## Summary

v0.6 adds post-hoc physical diagnostics around generated specs and local Meep
artifacts. The recommended user entry point is:

```bash
optical-spec diagnose outputs/my_spec.json --output-dir outputs
```

## Added

- `optical-spec diagnose`
- `mesh_report.csv`
- `flux_report.csv`
- `execution_diagnostics.json`
- `diagnostic_preview.png`
- local physical-candidate and observable/mesh diagnostic reports

## Limitations

- No production-grade physical validation.
- No formal convergence proof.
- Diagnostics do not run Meep.
- Meep execution remains optional/local through `meep-run`.
