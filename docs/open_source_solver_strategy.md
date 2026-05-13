# Open-source Solver Strategy

## Product positioning

optical-spec-agent is open-source-solver-first. The default project path targets
reproducible, local-first, inspectable simulation artifacts. The project
prioritizes open simulation backends, local artifact generation, offline
examples, and evidence fixtures that can run without proprietary licenses.

Proprietary commercial tools are not default dependencies.

中文说明：本项目优先服务开源仿真工具链。闭源商业软件不是默认依赖，不参与
默认测试、smoke 或 release validation。

## Preferred backend categories

- Open-source simulation backend: an inspectable solver backend that users may
  install and run manually outside the default tests.
- Open-source geometry / mesh backend: an inspectable geometry or meshing tool
  used to generate local artifacts for downstream simulation.
- Open-source multiphysics backend: an inspectable multiphysics tool that may
  consume generated local artifacts.
- Research-preview adapter: a working local artifact generator with conservative
  claims and optional/manual solver execution.
- MVP/scaffold adapter: a template or scaffold generator that is useful for
  review, but not solver-backed validation.
- Proprietary export-only future target: a possible future script/template
  export path for commercial tools, not a default dependency or validation gate.
- Unsupported / non-default tool: any tool not registered as an adapter and not
  required for default tests, smoke, examples, or release validation.

## Current open-source-first adapter families

| Adapter | Current status | Local artifact preview | External solver required to execute | External solver run by default | Evidence fixture | Production-grade physical validation claimed |
|---|---|---:|---:|---:|---:|---:|
| `meep` | research-preview | yes | yes, only for explicit manual execution | no | yes | no |
| `gmsh` | MVP/scaffold | yes | yes, only for external meshing | no | yes | no |
| `elmer` | MVP/scaffold | yes | yes, only for external FEM execution | no | yes | no |
| `mpb` | MVP/scaffold | yes | yes, only for external MPB execution | no | yes | no |
| `optiland` | MVP/scaffold | yes | yes, only for external Optiland execution | no | yes | no |

These adapters provide local artifact previews and regression evidence. They do
not prove solver-backed correctness, production-grade physical validation, or a
formal convergence result.

## Proprietary tool stance

Zemax, Lumerical, COMSOL, and proprietary Ansys optics tools are not default
project dependencies. They are not required for tests. They are not required for
smoke validation. They are not required for release validation. They are not
required for examples.

They may only be considered as future optional export targets if explicitly
scoped. Export-only support must not imply solver-backed validation, production
readiness, or default automation.

## Release validation policy

Default release validation must remain:

- local-first
- reproducible
- offline where possible
- no proprietary license required
- no external solver execution by default
- no external LLM required by default

Compatibility and validation evidence are tracked in
`docs/v1_0_compatibility_policy.md`, `docs/validation_evidence_manifest.md`,
`docs/open_source_solver_validation_plan.md`, and
`examples/examples_manifest.json`. The offline user journey is tracked in
`docs/offline_user_journey.md` and `examples/e2e/`; it remains no-network,
no-external-solver, no-external-LLM, and no-proprietary-solver by default.

## Why this matters

Open-source-first release engineering supports CI and regression tests, avoids
license-dependent release validation, improves reproducibility, enables public
examples and fixtures, and keeps physical claims conservative and evidence-based.

## Non-goals

- No production-grade physical validation claim.
- No formal convergence proof claim.
- No proprietary solver dependency by default.
- No automatic commercial tool execution.
- No PyPI/TestPyPI publication in this task.
