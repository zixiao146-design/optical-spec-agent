# Fiber coupling preview

Design domain: `fiber_coupling_preview`

Natural-language goal:

- EN: Create a local preview for fiber coupling preview with no external solver execution.
- ZH: 为光纤耦合预览创建本地预览，不运行外部求解器。

Materials: glass_fused_silica_preview, sio2, si3n4, air

Linked requirement templates: gaussian_beam_focus, slab_waveguide_single_mode

Expected calculators: optics.gaussian_beam.focus, optics.waveguide.sweep

Expected adapters: mpb, optiland

Missing-input questions:

- What fiber mode field diameter and wavelength should be assumed?
- Is the target coupling into a fiber, waveguide, or free-space focus?

Evidence boundary: Partial domain coverage; scalar Gaussian/waveguide previews only, no real coupling efficiency solver.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
