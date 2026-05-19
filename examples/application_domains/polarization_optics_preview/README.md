# Polarization optics preview

Design domain: `polarization_optics_preview`

Natural-language goal:

- EN: Create a local preview for polarization optics preview with no external solver execution.
- ZH: 为偏振光学预览创建本地预览，不运行外部求解器。

Materials: tio2, si3n4, sio2, glass_fused_silica_preview

Linked requirement templates: dielectric_metasurface_preview

Expected calculators: none; adapter/material preview path

Expected adapters: meep

Missing-input questions:

- What input and output polarization states should be transformed?
- Is the target a polarizer, waveplate, or metasurface polarization element?

Evidence boundary: Deferred/partial coverage; no production polarization model or solver result is claimed.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
