# Meep Manual Validation Reports

This directory is for optional manual Meep validation reports.

- Reports are added only after an explicit maintainer-approved opt-in run.
- Large Meep output files must stay outside the repository, usually under
  `/tmp`.
- Meep remains optional and is not a default dependency.
- Default pytest, smoke, quality gates, CI, and release validation do not run
  Meep.
- Reports here do not claim production-grade physical validation.
- Reports here do not claim a formal convergence proof.
