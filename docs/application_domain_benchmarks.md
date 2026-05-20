# Application Domain Benchmarks

The application-domain benchmark suite turns the local application-domain
registry into scenario evidence. It checks how the backend handles positive,
ambiguous, underconstrained, unsupported, and unsafe optical-design requests.

The benchmark is deterministic and local. It does not execute an external
solver, call an external LLM, upload packages, create tags, or create releases.
All benchmark results are preview/design-assist evidence and do not claim
production-grade physical validation or a formal convergence proof.

## Scenario Types

| Type | Purpose | Expected behavior |
| --- | --- | --- |
| `positive` | Supported local preview domain | Match the expected domain/template and record expected calculator or adapter behavior. |
| `ambiguous` | Multiple plausible optical domains | Preserve candidate domains and ask disambiguation questions instead of hard-matching unsafely. |
| `underconstrained` | Domain is recognizable but required inputs are missing | Report critical/optional missing inputs and recommended questions. |
| `unsupported` | Request needs unavailable or proprietary execution | Block or defer the action and recommend a local preview alternative. |
| `unsafe_or_blocked` | Request asks for overclaiming or unsafe proof | Block production-grade validation or formal convergence claims. |

## Coverage

The benchmark dataset lives under `examples/application_domain_benchmarks/`.
It includes positive scenarios for:

- `nanoparticle_plasmonics`
- `thin_film_coating`
- `slab_waveguide`
- `photonic_crystal`
- `dielectric_metasurface`
- `lens_ray_optics`
- `gaussian_beam_focusing`
- `imaging_system_preview`
- `fiber_coupling_preview`
- `polarization_optics_preview`

It also includes ambiguous, underconstrained, and unsupported cases such as
waveguide-versus-coating, lens-versus-Gaussian focus, missing focal length,
missing nanoparticle radius/material, full Zemax optimization, full Lumerical
FDTD, and production-grade validation requests.

## Evaluation Criteria

Each scenario records:

- expected primary domain and candidate domains
- expected confidence
- expected requirement template
- expected material, calculator, and adapter behavior
- expected missing critical and optional inputs
- expected recommended questions
- expected blocked actions
- preview-only safety flags

The evaluator compares those expectations against deterministic local domain
matching, requirement matching, an Agent Task Session when applicable, and the
tool-call ledger. It never executes solver code.

## API and Script

```bash
python scripts/evaluate_application_domain_benchmarks.py
```

API endpoints:

- `GET /api/application-domain-benchmarks`
- `GET /api/application-domain-benchmarks/{scenario_id}`
- `POST /api/application-domain-benchmarks/{scenario_id}/evaluate`
- `GET /api/application-domain-benchmark-results`

## Pass / Warn / Fail

- `pass`: expected deterministic preview behavior matched.
- `warn`: the backend behaved safely, but the scenario represents partial or
  deferred coverage.
- `fail`: the backend missed an expected match, question, blocked action, or
  tool behavior.

As of `0.9.0rc8`, the fiber coupling and polarization optics positive
benchmarks are closed by deterministic preview calculators:

- `fiber_coupling_preview_positive` records
  `optics.fiber_coupling.gaussian_mode_overlap`.
- `polarization_optics_preview_positive` records `optics.polarization.jones`.

Their calculator-level reference sanity cases are documented in
[`fiber_polarization_reference_cases.md`](fiber_polarization_reference_cases.md).

The benchmark suite is expected to report `19 pass / 0 warn / 0 fail` unless a
future scenario intentionally introduces a new deferred capability.

## Safety Boundary

The benchmark suite does not prove real solver monitor results. It does not
prove production-grade physical validation. It does not prove formal
convergence. External solvers, external LLMs, proprietary tools, uploads, tags,
and releases remain outside the default benchmark path.

The consolidated maturity label for this suite is
`benchmark_checked_preview`; see
[`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md).
