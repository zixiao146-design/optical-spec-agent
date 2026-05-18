"""Local preview optical design calculators.

These helpers are deterministic design-assist calculations. They do not run
external solvers, do not call external LLMs, and do not claim production-grade
physical validation.
"""

from .models import CalculatorQuality
from .gaussian_beam import (
    focus_gaussian_beam_thin_lens,
    gaussian_beam_parameters,
    propagate_gaussian_beam,
    propagate_gaussian_beam_series,
)
from .paraxial import (
    abcd_free_space,
    abcd_thin_lens,
    analyze_two_lens_relay,
    compose_abcd,
    propagate_ray,
    summarize_paraxial_system,
    thin_lens,
)
from .thin_film import (
    calculate_thin_film_spectrum,
    calculate_thin_film_stack,
    design_quarter_wave_ar_coating,
    summarize_thin_film_result,
)
from .waveguide import (
    single_mode_estimate,
    slab_waveguide_sweep,
    slab_waveguide_v_number,
    suggest_single_mode_thickness_range,
)

__all__ = [
    "abcd_free_space",
    "abcd_thin_lens",
    "analyze_two_lens_relay",
    "calculate_thin_film_spectrum",
    "calculate_thin_film_stack",
    "CalculatorQuality",
    "compose_abcd",
    "design_quarter_wave_ar_coating",
    "focus_gaussian_beam_thin_lens",
    "gaussian_beam_parameters",
    "propagate_gaussian_beam",
    "propagate_gaussian_beam_series",
    "propagate_ray",
    "single_mode_estimate",
    "slab_waveguide_sweep",
    "slab_waveguide_v_number",
    "suggest_single_mode_thickness_range",
    "summarize_paraxial_system",
    "summarize_thin_film_result",
    "thin_lens",
]
