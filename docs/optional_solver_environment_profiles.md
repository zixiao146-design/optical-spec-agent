# Optional Solver Environment Profiles

Optional solver readiness is environment-specific. A solver may be unavailable
from the project Python while still being importable from a dedicated solver
environment such as `osa-solvers`.

## Profiles

| Profile | Purpose | Probe style | Default solver execution |
| --- | --- | --- | --- |
| `current` | Active Python and current `PATH` | Python import probes and command path probes | no |
| `osa-solvers` | Maintainer-local conda solver environment | Python import probes through `OSA_SOLVER_PYTHON` | no |
| `homebrew-cli` | CLI tools such as `gmsh` on current `PATH` | command path detection only | no |
| `deferred-elmer` | Elmer documentation state | deferred command readiness | no |

## Solver Python

Use `OSA_SOLVER_PYTHON` to point readiness detection at a solver-specific
Python interpreter:

```bash
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
python scripts/check_optional_solver_readiness.py
```

The script runs import-only probes such as `import meep` and
`import meep.mpb` in that interpreter. It does not run a Meep, MPB, Gmsh,
Optiland, or Elmer simulation.

The Meep decision packet uses this profile explicitly:
[`optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`](optional_solver_approval_records/meep_micro_benchmark_decision_packet.md).
The 2026-05-20 approved Meep-only micro-benchmark used this profile and is
recorded in `validation/meep/meep_micro_benchmark_2026-05-20.md`. Future Meep
reruns still require a fresh solver-specific approval phrase with an
`OSA_SOLVER_PYTHON` path.
The MPB decision packet also uses this profile:
[`optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`](optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md).
For MPB, `from meep import mpb` or `meep.mpb` import readiness is sufficient
for the profile check; an MPB CLI is not required if the Python path is
available. This is still import-only readiness and does not execute MPB.

## Solver-specific notes

- Gmsh readiness can be CLI/PATH based through `gmsh`.
- Meep readiness is usually a Python package check through `meep`.
- MPB readiness may be available through `meep.mpb` even when an `mpb` CLI is absent.
- Optiland readiness can be Python/package based and may also expose a CLI.
- Elmer remains deferred until a maintainable `ElmerSolver` install route exists.

## Boundaries

- No solver execution is performed by profile checks.
- Missing solvers are non-blocking.
- Readiness detection is not solver execution.
- Solver-backed micro-benchmarks still require explicit maintainer approval.
- TestPyPI, PyPI, tag, and release actions are unrelated and remain separately gated.
- No production-grade physical validation or formal convergence proof is claimed.

Execution approval is prepared separately in
[`optional_solver_micro_benchmark_execution_packet.md`](optional_solver_micro_benchmark_execution_packet.md)
and per-solver pending records under
[`optional_solver_approval_records/`](optional_solver_approval_records/).
