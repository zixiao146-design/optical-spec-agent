# Material Library

The material library is a local preview catalog for optical design assistance.
It helps Agent Studio suggest starter materials for examples and workflow
planning, but it is not a production-grade optical constants database.

Current status:
- Current public prerelease: v0.9.0rc7
- Current main release draft: 0.9.0rc8
- API contract version: 0.1
- Material catalog status: local preview / design-assist
- PyPI: not published

Included starter materials:
- air
- water
- sio2
- si
- si3n4
- tio2
- al2o3
- au
- ag
- ito
- gaas
- glass_bk7_preview
- glass_fused_silica_preview

Suggestion rules:
- nanoparticle plasmonics -> Au, Ag, SiO2, water, air
- dielectric metasurface -> TiO2, Si3N4, Si, SiO2
- waveguide -> Si, SiO2, Si3N4
- thin film coating -> SiO2, TiO2, Al2O3
- lens/ray optics -> BK7 preview, fused silica preview, air
- photonic crystal band -> Si, GaAs, SiO2, air

Material provenance:
- Every starter material exposes `provenance_type`, `source_note`,
  `wavelength_validity_note`, `known_limitations`, `requires_user_verification`,
  and `production_grade_optical_constants=false`.
- Numeric n/k values are approximate preview constants unless a future entry
  documents stronger reviewed provenance.
- `POST /api/materials/diagnose` returns suitability rationale, warnings,
  missing context, and recommended verification for one material/application
  pair.
- See `docs/material_provenance_policy.md` for the catalog policy.

Safety boundaries:
- Material values are approximate preview/design-assist hints.
- Users must verify material constants before physical conclusions.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No external solver is executed by default.
- No external LLM is called by default.
- No network material database lookup is performed.

Frontend use:
- Agent Studio exposes a Material Library page.
- The page shows local material records and material suggestions.
- The page links materials to bundled Example Gallery cases where applicable.
- The page must display that material data is preview-only.
