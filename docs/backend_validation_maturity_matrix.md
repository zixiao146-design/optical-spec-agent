# Backend Validation Maturity Matrix

This matrix consolidates backend evidence levels for `0.9.0rc8.dev0`.
It is a conservative maintainer view: every row is preview/design-assist
evidence, no production-grade physical validation is claimed, and no formal
convergence proof is claimed.

## Maturity Levels

| Level | Meaning |
| --- | --- |
| `documented_preview` | Behavior and limitations are documented, but the evidence is not a physical validation result. |
| `fixture_guarded_preview` | Stable fixtures, API shapes, or metadata-diff checks guard the behavior. |
| `sanity_checked_preview` | Local analytic calculators have reference sanity cases and failure-mode tests. |
| `benchmark_checked_preview` | Deterministic scenario benchmarks check routing, diagnostics, missing inputs, and blocked actions. |
| `optional_manual_solver_validated` | Manual solver validation may exist for selected adapters, but external solvers are not run by default. |
| `production_grade_not_claimed` | Explicit boundary marker: production-grade validation is outside current claims. |

## Current Matrix

| Area | Component | Current level | Evidence | Limitation |
| --- | --- | --- | --- | --- |
| Materials | material library | `documented_preview` | material provenance docs and tests | User must verify constants; not a production-grade optical constants database. |
| Requirements | design requirement templates | `fixture_guarded_preview` | requirement fixtures and matching tests | Heuristic matching only; ambiguous goals generate questions. |
| Requirements | natural-language to optical-language | `fixture_guarded_preview` | ambiguous matching and missing-input tests | No external LLM by default; confidence is routing evidence. |
| Calculators | thin-film | `sanity_checked_preview` | single-interface and quarter-wave AR reference cases | Transfer-matrix preview only. |
| Calculators | paraxial | `sanity_checked_preview` | thin-lens, ABCD, and relay reference cases | First-order optics only. |
| Calculators | Gaussian beam | `sanity_checked_preview` | Rayleigh range and beam-radius reference cases | Scalar paraxial model only. |
| Calculators | waveguide | `sanity_checked_preview` | V-number and sweep reference cases | Slab-waveguide approximation only. |
| Calculators | fiber coupling | `sanity_checked_preview` | Gaussian overlap reference cases | Scalar Gaussian mode-overlap approximation only. |
| Calculators | polarization | `sanity_checked_preview` | Jones polarizer and waveplate reference cases | Jones-calculus preview only. |
| Optical language | source/monitor diagnostics | `fixture_guarded_preview` | source/monitor inference fixtures and tests | Monitor records are preview metadata. |
| Optical language | observable diagnostics | `fixture_guarded_preview` | observable taxonomy fixtures and tests | Observable fit is not a computed physical result. |
| Adapters | adapter-native source/monitor mapping | `fixture_guarded_preview` | adapter mapping fixtures and tests | Real adapter results require explicit solver execution. |
| Adapters | adapter golden coverage | `fixture_guarded_preview` | golden cases and strict metadata diff | Metadata checks are not solver monitor outputs. |
| Application domains | domain benchmarks | `benchmark_checked_preview` | 19 pass / 0 warn / 0 fail scenario suite | Benchmarks test deterministic behavior, not physical correctness. |
| Agents | sub-agent task sessions | `fixture_guarded_preview` | audit script and tool-call ledger tests | Roles are deterministic local backend roles. |
| Agents | tool-call ledger | `fixture_guarded_preview` | ledger tests and evidence pack | Ledger shows local tool calls and blocked external actions. |
| Frontend | Agent Studio | `documented_preview` | UI smoke and docs | UI/demo surface only, not validation evidence. |

## What Is Not Claimed

- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No real solver monitor result is claimed by default.
- No external solver execution is performed by default.
- No external LLM is required by default.
- Elmer remains Level 2 + Level-3-ready; Level 3 is deferred.

Run:

```bash
python scripts/audit_validation_claims.py
```

The audit blocks unsafe claim language while allowing explicit negated forms.

