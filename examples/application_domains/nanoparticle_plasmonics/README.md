# Nanoparticle plasmonics

Design domain: `nanoparticle_plasmonics`

Natural-language goal:

- EN: Create a local preview for nanoparticle plasmonics with no external solver execution.
- ZH: 为纳米颗粒等离激元创建本地预览，不运行外部求解器。

Materials: ag, au, sio2, air, water

Linked requirement templates: nanoparticle_plasmonics

Expected calculators: none; adapter/material preview path

Expected adapters: meep, gmsh

Missing-input questions:

- What particle material, size, and surrounding medium should be used?
- Should the observable be scattering, extinction, or near-field enhancement?

Evidence boundary: Material/adapter/source-monitor preview; real scattering spectra require explicit solver execution.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
