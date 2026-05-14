# Optiland Optional Manual Validation Report - 2026-05-14

- Date: 2026-05-14
- Maintainer: local maintainer
- Project version: 0.9.0rc5.dev0
- Git commit: 5fab004bca79036f7fc88d43397f76d00e73cc43
- Adapter family: optiland
- Backend name: Optiland
- Backend version: 0.6.0
- Python executable: /opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python
- Input fixture: `examples/specs/optiland_preview.json`
- Generated artifact: `/tmp/osa-optiland-validation-output/optiland_preview.py`
- Output artifact: `/tmp/osa-optiland-validation-output/optiland_validation_result.json` (not committed)
- Command run:
  `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python /tmp/osa-optiland-validation-output/optiland_minimal_validation.py /tmp/osa-optiland-validation-output/optiland_preview.py /tmp/osa-optiland-validation-output/optiland_validation_result.json`
- Expected high-level result:
  Optiland can execute the project-owned minimal validation path without
  proprietary software.
- Observed result:
  The opt-in pilot generated the Optiland adapter scaffold and executed a tiny
  project-owned Optiland path that constructs an `Optic` with one wavelength,
  one field, and one entrance-pupil aperture, then serializes it to a local JSON
  artifact under `/tmp`.
- Diagnostics:
  Optiland imported successfully, the adapter-generated scaffold contained the
  expected guarded import and builder function, and the tiny `Optic` metadata
  path completed without critical stderr diagnostics.
- Pass/fail:
  pass
- Limitations:
  - This is a narrow optional manual validation of the Optiland path.
  - This is not production-grade optical validation.
  - This is not a formal convergence proof.
  - This does not validate optical design correctness.
  - This does not make Optiland a default dependency.
- Whether this supports any release-note claim:
  yes, only a limited claim that the optional Optiland manual validation path
  was exercised.
- Production-grade validation supported:
  no
- Formal convergence proof supported:
  no
- Should this be included in release notes:
  optional, as limited validation evidence only
