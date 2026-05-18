# Optical Calculator Reference Cases

These local JSON files capture deterministic sanity checks for the preview
optical calculators. They are formula-level reference cases used to keep the
backend meaningful as a design-assist tool.

They are not production-grade physical validation, do not execute external
solvers, do not call external LLMs, and do not access network material
databases. Formula references are local documented formulas and tolerance
checks, not external validation certificates.

## Cases

- `thin_film_single_interface_air_glass.json`: normal-incidence Fresnel
  interface, air to `n=1.5` glass, expected `R ~= 0.04`.
- `thin_film_quarter_wave_ar_550nm.json`: ideal single-layer quarter-wave AR
  coating at 550 nm with `n = sqrt(n_substrate)`.
- `gaussian_beam_rayleigh_range.json`: Rayleigh range
  `z_R = pi * w0^2 / lambda`.
- `paraxial_thin_lens_1to1.json`: thin lens, `f=50 mm`,
  `object_distance=100 mm`, expected image distance 100 mm and magnification
  -1.
- `waveguide_v_number_sanity.json`: scalar slab waveguide V-number formula.

## Safety

- Preview/design-assist only.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No external solver is executed.
- No external LLM is called.
