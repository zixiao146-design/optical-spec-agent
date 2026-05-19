# Imaging system preview

Design domain: `imaging_system_preview`

Natural-language goal:

- EN: Create a local preview for imaging system preview with no external solver execution.
- ZH: 为成像系统预览创建本地预览，不运行外部求解器。

Materials: glass_bk7_preview, glass_fused_silica_preview, air

Linked requirement templates: paraxial_lens_imaging

Expected calculators: optics.paraxial.two_lens_relay

Expected adapters: optiland

Missing-input questions:

- What magnification and image plane should the preview target?
- What aperture and field should constrain the imaging system?

Evidence boundary: Paraxial imaging preview; real spot/MTF requires explicit ray-trace execution.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
