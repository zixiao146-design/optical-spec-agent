# Lens ray optics

Design domain: `lens_ray_optics`

Natural-language goal:

- EN: Create a local preview for lens ray optics with no external solver execution.
- ZH: 为透镜光线光学创建本地预览，不运行外部求解器。

Materials: glass_bk7_preview, glass_fused_silica_preview, air

Linked requirement templates: paraxial_lens_imaging

Expected calculators: optics.paraxial.two_lens_relay, optics.paraxial.thin_lens

Expected adapters: optiland

Missing-input questions:

- What focal length, aperture, and field of view should be previewed?
- Is paraxial approximation acceptable for this first pass?

Evidence boundary: Paraxial calculator and Optiland preview metadata; real ray trace requires explicit execution.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
