# Lens Optimization Underconstrained

Natural-language goal: `Help me optimize a lens.`

The lens family is identifiable, but focal length, aperture, field of view, wavelength, and object/image constraints are absent.

Expected safe behavior:
- Return the paraxial lens template with medium confidence.
- Report missing critical and optional inputs.
- Ask for focal length, aperture, field of view, and object distance.
- Do not execute Optiland or any external ray-trace tool by default.
- Do not call an external LLM.
- Do not claim production-grade physical validation.
