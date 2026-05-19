# Natural Language to Optical Language

This document defines the backend path from user goal to optical design language.

## Mapping Path

The current local backend maps:

natural language goal -> requirement template -> optical language summary -> design case -> material/geometry/adapter/calculator path -> tool-call ledger.

The mapper is deterministic and local. It does not call an external LLM.
For ambiguous or under-specified goals, it returns confidence, candidate
templates, missing disambiguation inputs, and recommended questions. It does
not silently choose a solver path for unknown goals.

## Optical Language Fields

- `physical_system`: the optical system family, such as `thin_film_stack`, `gaussian_beam`, `slab_waveguide`, `paraxial_lens_system`, `photonic_crystal`, `metasurface`, or `nanoparticle_on_film`.
- `material_system`: local preview material candidates.
- `geometry_model`: the local geometry abstraction, such as layer stack, Gaussian beam, slab waveguide, ABCD thin-lens system, periodic lattice, meta-atom array, or sphere-on-film scaffold.
- `solver_or_adapter_family`: open-source-first adapter or local calculator path.
- `calculator_or_tool_path`: the deterministic internal function or API route expected for preview.
- `evidence_boundary`: what the result does and does not prove.

## Examples

English coating goal:

> Design a local preview for a single-layer anti-reflection coating on glass at 550 nm.

Maps to:

- template: `thin_film_ar_coating`
- physical system: `thin_film_stack`
- tool path: `/api/optics/thin-film-spectrum` and `/api/optics/quarter-wave-ar`

Chinese nanoparticle goal:

> 请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。

Maps to:

- template: `nanoparticle_plasmonics`
- physical system: `nanoparticle_on_film`
- tool path: material catalog, agent trace, workflow preview, adapter preview

## Limitations

- The matcher is a heuristic, not semantic AI.
- Unknown goals return low-confidence safe guidance.
- Calculator outputs are preview/design-assist only.
- No external solver or external LLM is used by default.
- No production-grade physical validation or formal convergence proof is claimed.

## Source and Monitor Step

The optical-language path now includes deterministic source/monitor inference:

- `source_model`: source type, wavelength band, polarization, incidence
  direction, beam waist or mode index when relevant.
- `monitor_model`: monitor type, observable, region, sampling, and units.
- `optical_language_diagnostics`: missing inputs, defaults, ambiguity notes,
  blocking questions, `safe_to_preview`, and `safe_to_run_solver=false`.

For nanoparticle scattering previews, the default metadata is a
plane-wave-like source, 400-900 nm band, `linear_x` polarization, and a
scattering/extinction spectrum monitor. This is metadata only; no external
solver monitor result is produced.

See `docs/optical_language_source_monitor.md` and
`docs/source_monitor_missing_input_diagnostics.md`.

## Ambiguous and Missing Inputs

The rc8.dev0 backend distinguishes critical and optional missing inputs:

- `missing_critical_inputs`: values needed before a meaningful solver setup.
- `missing_optional_inputs`: values that improve preview fidelity.
- `recommended_questions`: deterministic follow-up questions.

`safe_to_preview` can remain true for local design-assist artifacts, while
`safe_to_run_solver` remains false by default. See
`docs/ambiguous_requirement_matching.md` and
`docs/missing_input_diagnostics.md`.

## Application Domain Coverage

The rc8.dev0 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.
