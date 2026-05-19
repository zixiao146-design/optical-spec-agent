# Material Provenance Policy

The material library is a local preview/design-assist catalog. It is useful for
agent planning, material suggestions, and adapter-preview metadata, but it is
not a production-grade optical constants database.

## Provenance Fields

Each material record exposes:

- `provenance_type`: `curated_preview`, `placeholder`, `approximate_constant`, or `user_must_verify`.
- `source_note`: local note explaining the starter-catalog origin.
- `citation_note`: optional human-readable citation or review note.
- `wavelength_validity_note`: reminder that dispersion must be verified.
- `known_limitations`: preview limitations for the entry.
- `suitable_for` / `not_suitable_for`: local design-assist hints.
- `requires_user_verification`: always true for starter materials.
- `production_grade_optical_constants`: always false.

## Suitability Diagnostics

`POST /api/materials/diagnose` returns deterministic local suitability notes for
an application such as nanoparticle plasmonics, waveguides, thin-film coatings,
lenses, photonic crystals, or metasurfaces.

The endpoint reports rationale, warnings, missing context, and recommended
verification steps. It does not query external databases, execute solvers, call
external LLMs, or upgrade preview constants into production evidence.
There is no external material database lookup in the default backend.

## Boundaries

- Material constants are approximate preview values.
- Users must verify wavelength-dependent n/k data independently.
- The catalog does not claim production-grade physical validation.
- The catalog does not claim a formal convergence proof.

## Application Domain Coverage

The rc8.dev0 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.
