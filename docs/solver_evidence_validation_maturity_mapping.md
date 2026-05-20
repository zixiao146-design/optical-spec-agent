# Solver Evidence Validation Maturity Mapping

Current public prerelease: v0.9.0rc7.
Current main development version: `0.9.0rc8.dev0`.

This document explains how optional solver micro-benchmark evidence maps into
the conservative backend validation maturity model.

## Mapping Table

| Solver | Evidence status | Maturity mapping | Default gates | Boundary |
| --- | --- | --- | --- | --- |
| Gmsh | executed / passed / reviewed / accepted | optional manual mesh-generation smoke evidence | no solver execution | not optical correctness evidence |
| Optiland | executed / passed / reviewed / accepted | optional manual ray/path smoke evidence | no solver execution | not production-grade optical design validation |
| Meep | executed / passed / reviewed / accepted | optional manual PyMeep/FDTD smoke evidence | no solver execution | not production-grade FDTD validation |
| MPB | executed / passed / reviewed / accepted | optional manual MPB/band-structure smoke evidence | no solver execution | not production band-structure validation |
| Elmer | deferred / not executed | documented preview / deferred | no solver execution | not Level 3 |

## Maturity Interpretation

Optional manual solver evidence means a maintainer explicitly approved a
solver-specific opt-in run, the run passed, and a review decision accepted the
result as smoke evidence for that solver path. It does not make the solver a
default dependency and does not add solver execution to pytest, smoke, quality, or release gates.

## Non-claims

- No production-grade physical validation is claimed.
- No production-grade solver validation is claimed.
- No formal convergence proof is claimed.
- No optical correctness claim is made.
- PyPI publication remains separately gated and would not imply production-grade
  validation.

## Elmer

Elmer remains deferred until a maintainable `ElmerSolver` install route exists.
It is not Level 3 in this review.
