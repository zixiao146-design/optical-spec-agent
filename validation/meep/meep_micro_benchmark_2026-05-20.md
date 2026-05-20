# Meep Optional Micro-benchmark Evidence - 2026-05-20

Solver: Meep / PyMeep

Benchmark type: optional manual micro-benchmark

Approval record:
`docs/optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md`

Decision packet:
`docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`

Command used:

```bash
OSA_RUN_OPTIONAL_MEEP_VALIDATION=1 \
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_MEEP_VALIDATION_REPORT=/tmp/osa-meep-micro-benchmark-report.json \
OSA_MEEP_OUTPUT_DIR=/tmp/osa-meep-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

`OSA_SOLVER_PYTHON` path:
`/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`

Input fixture: `examples/specs/missing_wavelength_meep_preview.json`

Output artifacts:

- `/tmp/osa-meep-micro-benchmark-output/meep_preview.py`
- `/tmp/osa-meep-micro-benchmark-output/meep_minimal_validation.py`
- `/tmp/osa-meep-micro-benchmark-output/meep_validation_result.json`
- `/tmp/osa-meep-micro-benchmark-output/meep_stdout.log`
- `/tmp/osa-meep-micro-benchmark-output/meep_stderr.log`

Report path: `/tmp/osa-meep-micro-benchmark-report.json`

Report summary:

- Meep version: `1.33.0`
- Python executable: `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`
- Meep available: yes
- Optional validation enabled: yes
- Meep executed: yes
- Passed: yes
- Exit code: `0`
- Generated adapter artifact: `/tmp/osa-meep-micro-benchmark-output/meep_preview.py`
- Validation script: `/tmp/osa-meep-micro-benchmark-output/meep_minimal_validation.py`
- Output artifact: `/tmp/osa-meep-micro-benchmark-output/meep_validation_result.json`
- Validation type: `tiny_project_owned_pilot`
- Adapter artifact contains `mp.Simulation`: yes
- Minimal PyMeep run: one tiny 2D sanity simulation, `ran_until = 0.01`

Execution boundaries:

- External solver/package executed: yes, Meep only
- MPB executed: no
- Gmsh executed in this task: no
- Optiland executed in this task: no
- Elmer executed: no
- External LLM called: no
- PyPI/TestPyPI upload actions: no
- Tag/release actions: no
- Proprietary solver required: no

Non-claims:

- Production-grade physical validation claimed: no
- Production-grade FDTD validation claimed: no
- Formal convergence proof claimed: no
- Optical correctness claimed: no
- FDTD convergence validation claimed: no

Interpretation:

This evidence may be used only as optional manual PyMeep/FDTD smoke evidence for
the local adapter-generated scaffold and a tiny project-owned PyMeep execution
path. It verifies import/run plumbing and that the generated preview artifact
contains a Meep simulation scaffold. It does not prove optical correctness,
FDTD convergence, production readiness, or any production-grade physical
validation claim.

Gmsh and Optiland remain previously executed and reviewed under separate
approval records. They were not rerun in this Meep task. MPB remains a separate
decision even though `meep.mpb` was detected by import-only readiness checks.
Elmer remains deferred.

The generated `/tmp` artifacts are intentionally not committed. This repository
record preserves the report summary and safety boundaries.
