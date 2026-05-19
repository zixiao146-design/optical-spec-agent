# Gaussian beam focusing

Design domain: `gaussian_beam_focusing`

Natural-language goal:

- EN: Create a local preview for gaussian beam focusing with no external solver execution.
- ZH: 为高斯光束聚焦创建本地预览，不运行外部求解器。

Materials: air, glass_fused_silica_preview

Linked requirement templates: gaussian_beam_focus

Expected calculators: optics.gaussian_beam.series, optics.gaussian_beam.focus

Expected adapters: optiland

Missing-input questions:

- What wavelength, input waist, and propagation/focal distance should be used?
- Should the preview include a thin lens focus estimate?

Evidence boundary: Gaussian beam calculator preview; not a measured or solver-derived focal field.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
