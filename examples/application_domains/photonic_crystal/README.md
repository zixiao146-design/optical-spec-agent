# Photonic crystal

Design domain: `photonic_crystal`

Natural-language goal:

- EN: Create a local preview for photonic crystal with no external solver execution.
- ZH: 为光子晶体创建本地预览，不运行外部求解器。

Materials: si, gaas, sio2, air

Linked requirement templates: photonic_crystal_band_preview

Expected calculators: none; adapter/material preview path

Expected adapters: mpb

Missing-input questions:

- What lattice type, lattice constant, and k-point path should be used?
- How many bands should the preview plan request?

Evidence boundary: Adapter-native MPB preview metadata; real band frequencies require explicit MPB execution.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
