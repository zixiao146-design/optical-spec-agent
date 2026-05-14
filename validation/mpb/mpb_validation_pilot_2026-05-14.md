# MPB Optional Manual Validation Report - 2026-05-14

- Date: 2026-05-14
- Maintainer: local maintainer
- Project version: 0.9.0rc5.dev0
- Git commit: 464ad103f81f9bef4c3919e2f355fc030d82b32c
- Adapter family: mpb
- Solver name: MPB via PyMeep
- Solver version: 1.33.0
- Python executable: /opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python
- MPB CLI availability: unavailable; not required for this pilot
- Input fixture: `examples/specs/mpb_preview.json`
- Generated artifact: `/tmp/osa-mpb-validation-output/mpb_preview.py`
- Output artifact: `/tmp/osa-mpb-validation-output/mpb_validation_result.json` (not committed)
- Command run:
  `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python /tmp/osa-mpb-validation-output/mpb_minimal_validation.py /tmp/osa-mpb-validation-output/mpb_preview.py /tmp/osa-mpb-validation-output/mpb_validation_result.json`
- Expected high-level result:
  MPB/PyMeep can execute the project-owned minimal validation path without
  proprietary software.
- Observed result:
  The opt-in pilot generated the MPB adapter scaffold and executed a tiny
  project-owned `mpb.ModeSolver` path with one k-point, one band, and resolution
  4. The validation result JSON was written to `/tmp`.
- Diagnostics:
  MPB initialized a 2D mode-solver grid, solved one TE band at one k-point, and
  exited successfully. No critical stderr diagnostics were recorded.
- Pass/fail:
  pass
- Limitations:
  - This is a narrow optional manual validation of the MPB/PyMeep path.
  - This is not production-grade physical validation.
  - This is not a formal convergence proof.
  - This does not validate optical design correctness.
  - This does not make MPB a default dependency.
  - This does not require MPB CLI.
- Whether this supports any release-note claim:
  yes, only a limited claim that the optional MPB manual validation path was
  exercised.
- Production-grade validation supported:
  no
- Formal convergence proof supported:
  no
- Should this be included in release notes:
  optional, as limited validation evidence only
