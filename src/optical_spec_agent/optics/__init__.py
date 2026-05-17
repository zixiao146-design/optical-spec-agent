"""Local preview optical design calculators.

These helpers are deterministic design-assist calculations. They do not run
external solvers, do not call external LLMs, and do not claim production-grade
physical validation.
"""

from .gaussian_beam import gaussian_beam_parameters, propagate_gaussian_beam
from .paraxial import abcd_free_space, abcd_thin_lens, propagate_ray, thin_lens
from .thin_film import calculate_thin_film_stack
from .waveguide import single_mode_estimate, slab_waveguide_v_number

__all__ = [
    "abcd_free_space",
    "abcd_thin_lens",
    "calculate_thin_film_stack",
    "gaussian_beam_parameters",
    "propagate_gaussian_beam",
    "propagate_ray",
    "single_mode_estimate",
    "slab_waveguide_v_number",
    "thin_lens",
]
