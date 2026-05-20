# Optiland Optional Micro-benchmark Evidence - 2026-05-20

Solver: Optiland

Benchmark type: optional manual micro-benchmark

Approval record:
`docs/optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md`

Command used:

```bash
OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1 \
OSA_OPTILAND_VALIDATION_REPORT=/tmp/osa-optiland-micro-benchmark-report.json \
OSA_OPTILAND_OUTPUT_DIR=/tmp/osa-optiland-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

Input fixture: `examples/specs/optiland_preview.json`

Output artifacts:

- `/tmp/osa-optiland-micro-benchmark-output/optiland_preview.py`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_minimal_validation.py`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_validation_result.json`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_stdout.log`
- `/tmp/osa-optiland-micro-benchmark-output/optiland_stderr.log`

Report path: `/tmp/osa-optiland-micro-benchmark-report.json`

Report summary:

- Optiland version: `0.6.0`
- Python executable: `/Users/lizixiao/.pyenv/shims/python`
- Optiland available: yes
- Optional validation enabled: yes
- Optiland executed: yes
- Passed: yes
- Exit code: `0`
- Generated adapter artifact: `/tmp/osa-optiland-micro-benchmark-output/optiland_preview.py`
- Validation script: `/tmp/osa-optiland-micro-benchmark-output/optiland_minimal_validation.py`
- Output artifact: `/tmp/osa-optiland-micro-benchmark-output/optiland_validation_result.json`
- Validation type: `tiny_project_owned_optiland_pilot`
- Minimal Optiland object: one wavelength, one field, one entrance-pupil aperture

Execution boundaries:

- External solver/package executed: yes, Optiland only
- Gmsh executed in this task: no
- Meep executed in this task: no
- MPB executed in this task: no
- Elmer executed in this task: no
- External LLM called: no
- PyPI/TestPyPI upload actions: no
- Tag/release actions: no
- Proprietary solver required: no

Non-claims:

- Production-grade physical validation claimed: no
- Formal convergence proof claimed: no
- Optical correctness claimed: no
- Lens design optimization validation claimed: no

Interpretation:

This evidence may be used only as optional manual Optiland ray/path smoke
evidence for the local adapter-generated scaffold and a tiny project-owned
Optiland object construction path. It does not change default pytest, smoke,
quality gate, release gate, upload, tag, or release behavior.
