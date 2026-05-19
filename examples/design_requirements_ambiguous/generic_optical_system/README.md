# Generic Optical System

Natural-language goal: `Design an optical system.`

This goal is intentionally ambiguous. It does not specify whether the design is a coating, waveguide, lens, nanoparticle, photonic crystal, metasurface, or Gaussian beam case.

Expected safe behavior:
- Return no matched template.
- Report low/none confidence.
- Ask for the optical application, source, monitor, material system, geometry, and target observable.
- Do not call an external LLM.
- Do not execute any solver.
- Do not claim production-grade validation.
