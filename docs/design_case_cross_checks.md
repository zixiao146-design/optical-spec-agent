# Design Case Cross-Checks

Current public prerelease: v0.9.0rc6. Current main development version:
`0.9.0rc7.dev0`.

Design case cross-checks verify that each bundled optical design example can be
loaded, converted into a deterministic `AgentTaskSession`, and inspected through
the `tool_call_ledger` without running solvers or calling external LLMs.

## What Is Cross-Checked

For each example under `examples/optical_design/`, the backend verifies:

- `spec.json` exists.
- `expected_agent_trace.json` exists.
- A local agent task session can be built.
- Material suggestions are produced.
- An adapter recommendation is present.
- Expected calculator calls are recorded when the design family has a scalar
  preview calculator.
- Safety flags remain false.

## Example To Calculator Mapping

| Example | Expected calculator behavior |
| --- | --- |
| `thin_film_coating` | `optics.thin_film` preview should execute. |
| `waveguide_mode` | `optics.waveguide` preview should execute. |
| `lens_raytrace_preview` | `optics.paraxial` preview should execute. |
| `nanoparticle_plasmonics` | Material + adapter trace; no scalar calculator required. |
| `photonic_crystal_band` | Adapter/MPB trace; no scalar calculator required. |
| `dielectric_metasurface_preview` | Material + adapter trace; no scalar calculator required. |

## Status Semantics

- `pass`: required files exist and expected backend calls are present.
- `warning`: the example is usable but a non-blocking mismatch should be
  reviewed.
- `fail`: a required file, session, material suggestion, adapter recommendation,
  or expected calculator call is missing.

## How To Run

Use the API:

```bash
curl http://127.0.0.1:8000/api/design-case-cross-checks
```

Or run the smoke script:

```bash
./scripts/smoke_backend_report.sh
```

## Safety Boundaries

Cross-checks are preview/design-assist checks only. They do not run external
solvers, do not call external LLMs, do not access the network, do not upload
packages, do not create tags/releases, do not claim production-grade physical
validation, and do not claim formal convergence proof.

No production-grade physical validation is claimed.
