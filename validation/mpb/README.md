# MPB Validation Reports

This directory is for optional manual MPB validation reports.

Default tests, smoke checks, quality gates, and release validation do not run
MPB. Reports here must not commit large solver output files and must not make
MPB a default dependency. MPB CLI is not required when the `meep.mpb` Python path
is available.

Reports in this directory do not claim production-grade physical validation,
formal convergence proof, or optical design correctness unless a future
maintainer-approved validation scope explicitly says otherwise.
