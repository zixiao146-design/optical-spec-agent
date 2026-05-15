# Gmsh Level 3 Readiness

## Current Status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- Adapter family: gmsh
- Current maturity: Level 3 - Optional manual solver validation
- Evidence report: `validation/gmsh/gmsh_validation_pilot_2026-05-14.md`
- PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0
- v0.9.0rc6 tag: not created

## Evidence Summary

The optional Gmsh validation pilot was explicitly enabled on 2026-05-14 with
`OSA_RUN_OPTIONAL_GMSH_VALIDATION=1`. The script generated a local `.geo`
artifact from `examples/specs/gmsh_preview.json` through the project Gmsh
adapter, then ran Gmsh against that generated artifact in `/tmp`.

Result:

- Gmsh path: `/opt/homebrew/bin/gmsh`
- Gmsh version: `4.15.2-git`
- Input fixture: `examples/specs/gmsh_preview.json`
- Generated artifact: `/tmp/osa-gmsh-validation-output/gmsh_preview.geo`
- Output artifact: `/tmp/osa-gmsh-validation-output/gmsh_preview.msh`
- Passed: yes
- Level 3 achieved: yes, for this narrow optional manual validation path

## Boundaries

- Default pytest does not run Gmsh.
- Default smoke and quality gates do not execute Gmsh.
- Release validation does not require Gmsh.
- Gmsh remains an optional external open-source tool.
- This evidence does not claim production-grade physical validation.
- This evidence does not claim a formal convergence proof.
- This evidence does not validate optical correctness.
- Proprietary solvers are not required.

## Next Step Toward Level 4

The next maturity step would be a reproducible solver-backed benchmark with
documented environment assumptions, high-level expected results, and acceptance
criteria. That benchmark has not been defined or approved yet.
