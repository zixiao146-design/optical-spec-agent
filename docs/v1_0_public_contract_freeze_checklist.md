# v1.0 Public Contract Freeze Checklist

## Current status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- v1.0.0: not released
- v0.9.0rc6 tag: not created
- PyPI: not published
- TestPyPI: not uploaded

## Candidate-stable contract areas

- Console script: `optical-spec`
- Documented CLI commands
- Documented no-network examples
- Examples manifest paths
- Schema public fields
- Adapter registry names
- `adapter-list --json` top-level shape
- `workflow-plan --json` public top-level keys
- Package metadata: `project.name`, `project.version`, console script
- No-default external solver / no-default external LLM / no-default
  proprietary solver guarantees

## Areas still preview / not frozen

- Adapter generated-script internals
- Workflow internal implementation details
- Scaffold/MVP adapter output details
- Optional solver validation internals
- External LLM-assisted parsing path
- Proprietary export-only future targets
- Production-grade physical validation
- Formal convergence proof

## Freeze checklist

| Area | Status | Notes |
|---|---|---|
| CLI command names | ready | Documented in `docs/cli_contract.md` and guarded by CLI tests. |
| CLI examples | ready | Offline examples and commands are covered by examples tests. |
| Schema public fields | candidate-ready | Public top-level fields are documented and tested, but final v1.0 confirmation is still required. |
| Adapter registry names | ready | `meep`, `mpb`, `gmsh`, `elmer`, and `optiland` are documented and tested. |
| Workflow-plan public keys | candidate-ready | Public top-level keys are documented and guarded; workflow internals remain preview. |
| Examples manifest | ready | Paths and no-network/no-solver/no-LLM/no-proprietary guarantees are tested. |
| Packaging metadata | ready for RC, not PyPI-published | Local build and wheel smoke pass; PyPI/TestPyPI remain unpublished/unuploaded. |
| TestPyPI decision | pending | Upload is not approved and no upload command is authorized. |
| PyPI publication decision | not granted | PyPI publication remains blocked pending explicit maintainer approval. |
| Elmer Level 3 | deferred/non-blocking | Elmer remains Level 2 + Level-3-ready pending ElmerSolver availability and explicit opt-in validation. |
| Production-grade physical validation | non-goal unless explicitly claimed | Current docs do not claim production-grade physical validation. |
| Formal convergence proof | non-goal unless explicitly claimed | Current docs do not claim a formal convergence proof. |

## Required before v1.0 final

- Maintainer confirms public contract freeze.
- TestPyPI/PyPI strategy decided.
- Release notes explicitly state validation scope.
- Quality gates pass.
- No accidental default solver/LLM/proprietary dependency.
- No overclaiming physical validation.
