# Application Domain Registry

The application domain registry is a local preview/design-assist map from broad
optical-design domains to requirement templates, material suitability checks,
expected calculators, adapter preview families, and missing-input questions.
It is deterministic and does not call an external LLM, execute an external
solver, or query an online material database.

## Registered Domains

| Domain | Requirement templates | Materials | Calculator / adapter path |
| --- | --- | --- | --- |
| `nanoparticle_plasmonics` | `nanoparticle_plasmonics` | Ag, Au, SiO2, air, water | Meep/Gmsh preview metadata |
| `thin_film_coating` | `thin_film_ar_coating` | SiO2, TiO2, Al2O3, BK7 preview | thin-film spectrum and quarter-wave AR preview |
| `slab_waveguide` | `slab_waveguide_single_mode` | Si, Si3N4, SiO2, air | waveguide V-number sweep, MPB/Elmer preview |
| `photonic_crystal` | `photonic_crystal_band_preview` | Si, GaAs, SiO2, air | MPB band-structure preview metadata |
| `dielectric_metasurface` | `dielectric_metasurface_preview` | TiO2, Si3N4, Si, SiO2 | Meep/Gmsh preview metadata |
| `lens_ray_optics` | `paraxial_lens_imaging` | BK7 preview, fused silica preview, air | paraxial calculator and Optiland preview |
| `gaussian_beam_focusing` | `gaussian_beam_focus` | air, fused silica preview | Gaussian beam series/focus preview |
| `imaging_system_preview` | `paraxial_lens_imaging` | BK7 preview, fused silica preview, air | paraxial relay and Optiland preview |
| `fiber_coupling_preview` | `gaussian_beam_focus`, `slab_waveguide_single_mode` | fused silica preview, SiO2, Si3N4 | partial Gaussian/waveguide preview; coupling solver deferred |
| `polarization_optics_preview` | `dielectric_metasurface_preview` | TiO2, Si3N4, SiO2, fused silica preview | partial metadata; dedicated polarization model deferred |

## API

- `GET /api/application-domains`
- `GET /api/application-domains/{domain_id}`
- `POST /api/application-domains/match`
- `GET /api/application-domains/{domain_id}/cross-check`
- `GET /api/application-domain-cross-checks`

## Benchmarks

The registry is exercised by
[`application_domain_benchmarks.md`](application_domain_benchmarks.md). The
benchmark suite adds positive, ambiguous, underconstrained, unsupported, and
unsafe/blocked scenarios so maintainers can see how domain matching, material
coverage, requirement templates, calculators/adapters, missing-input questions,
and blocked actions behave together.

## Safety Boundary

The registry records preview-only coverage. Material constants remain local
starter values that require user verification. Calculator and adapter paths are
design-assist scaffolds, not production-grade physical validation. External
solvers and external LLMs are not required or executed by default.
