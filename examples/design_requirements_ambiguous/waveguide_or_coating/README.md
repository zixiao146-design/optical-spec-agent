# Waveguide Or Coating

Natural-language goal: `Design a waveguide and thin-film coating preview.`

This request mixes two design families: waveguide mode estimation and thin-film coating design.

Expected safe behavior:
- Return multiple candidate templates.
- Ask which design family should take priority.
- Ask for missing wavelength, material, geometry, and observable inputs.
- Do not call an external LLM.
- Do not execute a solver.
- Keep all outputs preview/design-assist.
