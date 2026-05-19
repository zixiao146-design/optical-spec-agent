# Slab waveguide

Design domain: `slab_waveguide`

Natural-language goal:

- EN: Create a local preview for slab waveguide with no external solver execution.
- ZH: 为平板波导创建本地预览，不运行外部求解器。

Materials: si, si3n4, sio2, air

Linked requirement templates: slab_waveguide_single_mode

Expected calculators: optics.waveguide.sweep, optics.waveguide.single_mode_range

Expected adapters: mpb, elmer

Missing-input questions:

- What core/cladding materials and operating wavelength should be used?
- Is this TE-like, TM-like, or polarization-agnostic?

Evidence boundary: Waveguide V-number preview; full mode solving requires explicit solver execution.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
