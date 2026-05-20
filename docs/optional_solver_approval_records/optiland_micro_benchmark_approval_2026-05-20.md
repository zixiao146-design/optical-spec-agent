# Optiland Optional Micro-benchmark Approval - 2026-05-20

Approval status: approved for this Optiland run

Solver: Optiland

Execution authorized: yes, Optiland only

Other solvers authorized: no

PyPI/TestPyPI/tag/release authorized: no

Required approval phrase:

> I approve running the optional Optiland micro-benchmark for optical-spec-agent.

Expected command:

```bash
OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1 \
OSA_OPTILAND_VALIDATION_REPORT=/tmp/osa-optiland-micro-benchmark-report.json \
OSA_OPTILAND_OUTPUT_DIR=/tmp/osa-optiland-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

Expected artifacts:

- `/tmp/osa-optiland-micro-benchmark-output/optiland_preview.py`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_minimal_validation.py`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_validation_result.json`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_stdout.log`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_stderr.log`

Expected report:

- `/tmp/osa-optiland-micro-benchmark-report.json`

Cleanup notes:

- Generated `/tmp/osa-optiland-micro-benchmark-*` files are local run artifacts.
- Commit only the Markdown evidence summary and manifest/doc updates.
- Do not commit raw generated artifacts unless a separate artifact policy approves them.

Non-claims:

- no production-grade physical validation
- no formal convergence proof
- no optical correctness claim
- no PyPI/TestPyPI upload authorization
- no tag/release authorization
- no v1.0.0 release authorization

Scope guard:

- Gmsh is not authorized to run again in this task.
- Meep is not authorized in this task.
- MPB is not authorized in this task.
- Elmer is not authorized in this task and remains deferred.
