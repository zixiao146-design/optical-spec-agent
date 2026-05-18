# Optical Calculator Case Integration

This document records how local preview calculators are integrated into optical
design cases and Agent Task Sessions.

## Current case mapping

| Example / goal family | Calculator calls | What is computed | What is not computed |
| --- | --- | --- | --- |
| `thin_film_coating` | `optics.thin_film.spectrum`, `POST /api/optics/thin-film-spectrum`, `POST /api/optics/quarter-wave-ar` | Normal-incidence wavelength sweep and quarter-wave AR starting point. | No material dispersion fitting, no angle/polarization-grade coating design, no production validation. |
| `waveguide_mode` | `optics.waveguide.sweep`, `POST /api/optics/waveguide-sweep`, `POST /api/optics/waveguide-single-mode-range` | Scalar slab V-number sweep and likely single-mode thickness range. | No vector eigenmode solve, no ridge/asymmetric mode validation. |
| `lens_raytrace_preview` | `optics.paraxial.two_lens_relay`, `POST /api/optics/two-lens-relay` | Ideal thin-lens relay estimate and ABCD summary. | No full ray trace, no aberration or glass optimization. |
| Gaussian beam goals | `optics.gaussian_beam.series`, `POST /api/optics/gaussian-beam-series`, `POST /api/optics/gaussian-beam-focus` | Beam propagation samples and ideal thin-lens focus estimate. | No M², clipping, aberration, or measured beam validation. |
| Nanoparticle/metasurface goals | material and adapter previews only | Material suggestions, adapter recommendation, workflow/artifact preview. | No scalar calculator is applied unless the goal also asks for a supported calculator family. |

## Tool-call ledger behavior

`POST /api/agent-session` includes `tool_call_ledger`. When a supported case is
detected, the relevant calculator record is marked `executed=true` with
`tool_kind=internal_python`. External solver, external LLM, upload, publish, tag,
and release records remain `executed=false`.

Each calculator artifact now carries `quality.quality_level=sanity_checked_preview`.
Where applicable, `quality.reference_case` points to a formula sanity check
documented in `docs/optical_calculator_reference_cases.md`.

`docs/design_case_cross_checks.md` and `GET /api/design-case-cross-checks`
now verify the current case mapping against real `AgentTaskSession` output. The
cross-checks prove which examples call calculators and which examples rely on
material/adapter traces only.

## Safety boundary

All calculator integration is local and deterministic:

- No external solver is executed.
- No external LLM is called.
- No network material database lookup is performed.
- No PyPI/TestPyPI upload is performed.
- No tag or GitHub release is created.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
