# v1.0 Public Contract Freeze Checklist

## Current status

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- v1.0.0: not released
- v0.9.0rc7 tag: not created
- PyPI: not published
- TestPyPI: uploaded for 0.9.0rc6.dev0
- TestPyPI verified: yes
- Clean install from TestPyPI: passed
- Maintainer confirmation: approved
- Freeze approval date: 2026-05-16
- Freeze baseline commit: 6e7ddf9c1811685c12db16bffb55cd76455267fe

## Approved frozen contract areas

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
| CLI command names | approved frozen | Documented in `docs/cli_contract.md` and guarded by CLI tests. |
| CLI examples | approved frozen | Offline examples and commands are covered by examples tests. |
| Schema public fields | approved frozen | Public top-level fields are documented and tested. |
| Adapter registry names | approved frozen | `meep`, `mpb`, `gmsh`, `elmer`, and `optiland` are documented and tested. |
| Workflow-plan public keys | approved frozen | Public top-level keys are documented and guarded; workflow internals remain preview. |
| Examples manifest | approved frozen | Paths and no-network/no-solver/no-LLM/no-proprietary guarantees are tested. |
| Packaging metadata | approved frozen for version semantics, not PyPI-published | Local build and wheel smoke pass; TestPyPI has `0.9.0rc6.dev0`, while PyPI remains unpublished. |
| TestPyPI decision | completed for 0.9.0rc6.dev0 | Trusted Publishing upload and clean install verification are recorded in `docs/testpypi_status_v0.9.0rc6.dev0.md`; future uploads require explicit approval per version. |
| PyPI publication decision | not granted | PyPI publication remains blocked pending explicit maintainer approval. |
| Elmer Level 3 | deferred/non-blocking | Elmer remains Level 2 + Level-3-ready pending ElmerSolver availability and explicit opt-in validation. |
| Production-grade physical validation | non-goal unless explicitly claimed | Current docs do not claim production-grade physical validation. |
| Formal convergence proof | non-goal unless explicitly claimed | Current docs do not claim a formal convergence proof. |

## Remaining hard blockers

- PyPI publication decision.

## Confirmation package

- `docs/v1_0_public_contract_freeze_confirmation.md`
- `docs/v1_0_contract_frozen_surface.md`
- `docs/v1_0_contract_non_goals.md`
- `docs/v1_0_breaking_change_policy.md`
- `docs/v1_0_public_contract_freeze_status.md`

## Required before v1.0 final

- Public contract freeze approval remains recorded in
  `docs/v1_0_public_contract_freeze_status.md`.
- TestPyPI/PyPI strategy decided.
- Release notes explicitly state validation scope.
- Quality gates pass.
- No accidental default solver/LLM/proprietary dependency.
- No overclaiming physical validation.
