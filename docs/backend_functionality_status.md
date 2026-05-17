# Backend Functionality Status

Current public prerelease: v0.9.0rc6. Current main development version:
`0.9.0rc7.dev0`.

This document records what the backend can actually import, call, execute, or
block.

## Installed / Callable / Executed

| Capability | Installed/importable | Callable | Executed in backend smoke |
| --- | --- | --- | --- |
| Material library | yes | yes | yes |
| Optical design example registry | yes | yes | yes |
| Agent trace builder | yes | yes | yes |
| Agent task session builder | yes | yes | yes |
| Tool-call ledger | yes | yes | yes |
| Thin-film preview calculator | yes | yes | yes |
| Paraxial lens preview calculator | yes | yes | yes |
| Gaussian beam preview calculator | yes | yes | yes |
| Waveguide V-number preview calculator | yes | yes | yes |

## Sub-agent Reality

The current sub-agents are deterministic backend roles, not separate installed
autonomous packages. `scripts/audit_sub_agents.py` reports this honestly:
role names are present in traces, callable backend functions exist, but
importable `SpecAgent` / `MaterialAgent` / similar classes are not currently
installed as standalone classes.

## External Solvers

External solvers are not run by default. `/api/tool-capabilities` may detect
whether Meep, Gmsh, MPB, ElmerSolver, or Optiland appear importable or on PATH,
but detection is not execution. Elmer remains Level 2 + Level-3-ready with
install deferred.

## Publication / Release Actions

The backend does not expose TestPyPI upload, PyPI publication, git tag creation,
or GitHub release creation endpoints. PyPI remains unpublished, and publication
approval remains not granted.

## Verification

Use:

```bash
python scripts/audit_sub_agents.py
./scripts/smoke_backend_capabilities.sh
```

Both scripts are local-only and print:

- NO SOLVER EXECUTION PERFORMED
- NO EXTERNAL LLM CALLED
- NO UPLOAD PERFORMED
- NO TAG CREATED
- NO RELEASE CREATED

