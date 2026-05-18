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
| Thin-film spectrum / quarter-wave AR helper | yes | yes | yes |
| Paraxial lens preview calculator | yes | yes | yes |
| Paraxial system / two-lens relay helper | yes | yes | yes |
| Gaussian beam preview calculator | yes | yes | yes |
| Gaussian beam series / focus helper | yes | yes | yes |
| Waveguide V-number preview calculator | yes | yes | yes |
| Waveguide sweep / single-mode range helper | yes | yes | yes |

## Case Integration

Agent task sessions now attach calculator result summaries where applicable:

- `thin_film_coating` records thin-film spectrum and quarter-wave AR helpers.
- `waveguide_mode` records waveguide V-number sweep and single-mode range helpers.
- `lens_raytrace_preview` records a paraxial two-lens relay helper.
- Gaussian beam goals record propagation series and thin-lens focus helpers.

These calls are internal Python design-assist calculations and are recorded in
`tool_call_ledger`; external solvers remain unexecuted.

Calculator responses now expose `quality`, `warnings`, `assumptions`, and
`limitations`. Formula-level reference cases are documented in
`docs/optical_calculator_reference_cases.md`; they are sanity checks, not
production-grade validation.

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
