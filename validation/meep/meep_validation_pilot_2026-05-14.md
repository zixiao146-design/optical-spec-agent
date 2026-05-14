# Meep Optional Manual Validation Report - 2026-05-14

- Date: 2026-05-14
- Maintainer: local maintainer
- Project version: 0.9.0rc5.dev0
- Git commit: cb5e7b9f29950be44868edb6bfdbf571a7167a5c
- Adapter family: meep
- Solver name: Meep / PyMeep
- Solver version: 1.33.0
- Python executable: /opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python
- Input fixture: examples/specs/missing_wavelength_meep_preview.json
- Generated artifact: /tmp/osa-meep-validation-output/meep_preview.py
- Output artifact: /tmp/osa-meep-validation-output/meep_validation_result.json
- Command run:
  `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python /tmp/osa-meep-validation-output/meep_minimal_validation.py /tmp/osa-meep-validation-output/meep_preview.py /tmp/osa-meep-validation-output/meep_validation_result.json`
- Expected high-level result:
  PyMeep can execute the project-owned minimal validation path and confirm that
  the adapter-generated Meep preview artifact contains a `mp.Simulation`
  scaffold without proprietary software.
- Observed result:
  The opt-in command completed successfully. The project-owned validation script
  initialized a tiny 2D PyMeep simulation and completed one internal timestep.
- Diagnostics:
  PyMeep reported a 1 x 1 x 0 computational cell at resolution 10 and completed
  at `t = 0.05` with 1 timestep. No stderr summary was recorded.
- Pass/fail:
  pass
- Limitations:
  - This is a narrow optional manual validation of the Meep/PyMeep path.
  - This is not production-grade physical validation.
  - This is not a formal convergence proof.
  - This does not validate optical design correctness.
  - This does not make Meep a default dependency.
  - This does not add Meep to default pytest, smoke, quality gates, CI, or release validation.
- Whether this supports any release-note claim:
  yes, only a limited claim that the optional Meep manual validation path was
  exercised.
- Production-grade validation supported:
  no
- Formal convergence proof supported:
  no
- Should this be included in release notes:
  optional, as limited validation evidence only
