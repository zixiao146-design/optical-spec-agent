# Nanoparticle plasmonics scattering preview

Chinese title: 纳米颗粒等离激元散射预览

Natural-language goal:

Generate a local preview workflow for silver or gold nanoparticle scattering on a thin film, suggest materials and an open-source adapter path, and do not run external solvers.

中文目标：

为银或金纳米颗粒位于薄膜上的散射问题生成本地预览工作流，推荐材料和开源适配器路径，不运行外部求解器。

Optical intent: nanoparticle plasmonics / scattering preview

Required inputs:
- particle_material
- particle_size_nm
- film_material
- gap_nm
- wavelength_range_nm

Default assumptions:
- Open-source-first Meep/Gmsh preview path.
- Material constants must be verified before conclusions.
- No FDTD solver execution by default.

Suggested materials:
- ag
- au
- sio2
- water
- air

Suggested adapter/tool path: meep with gmsh geometry preview

Expected calculator or adapter/tool calls:
- requirements.match_template
- requirements.extract_optical_intent
- material_catalog.suggest
- example_registry.load
- agent_trace.build
- workflow_plan.preview
- adapter_preview.generate

Expected artifacts:
- requirement_match
- material_suggestions
- agent_trace
- adapter_preview

Limitations: Adapter/material preview only; no scattering spectrum solver result.

Safety boundaries:

- No solver is executed by default.
- No external LLM is called by default.
- This template is preview/design-assist only.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No upload, tag, or release action is performed.
