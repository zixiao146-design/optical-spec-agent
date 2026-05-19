# Dielectric metasurface

Design domain: `dielectric_metasurface`

Natural-language goal:

- EN: Create a local preview for dielectric metasurface with no external solver execution.
- ZH: 为介质超表面创建本地预览，不运行外部求解器。

Materials: tio2, si3n4, si, sio2

Linked requirement templates: dielectric_metasurface_preview

Expected calculators: none; adapter/material preview path

Expected adapters: meep, gmsh

Missing-input questions:

- What phase profile or focusing target should the metasurface implement?
- What period, height, and polarization should define the unit-cell preview?

Evidence boundary: Material/geometry/adapter preview; no full-wave metasurface result is computed by default.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
