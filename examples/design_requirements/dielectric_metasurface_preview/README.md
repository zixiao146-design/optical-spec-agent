# Dielectric metasurface preview

Chinese title: 介质超表面预览

Natural-language goal:

Create a local preview workflow for a dielectric metasurface unit-cell array, suggest materials and adapters, and keep all outputs preview-only.

中文目标：

为介质超表面单元阵列创建本地预览工作流，推荐材料和适配器，并保持所有输出为预览。

Optical intent: dielectric metasurface preview

Required inputs:
- target_wavelength_nm
- phase_profile
- period
- meta_atom_geometry
- substrate_material

Default assumptions:
- Unit-cell/array geometry remains schematic.
- Material indices are preview values.
- No FDTD solver execution by default.

Suggested materials:
- tio2
- si3n4
- si
- sio2

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
- meep_gmsh_preview
- agent_trace

Limitations: Geometry/material preview only; no metasurface efficiency validation.

Safety boundaries:

- No solver is executed by default.
- No external LLM is called by default.
- This template is preview/design-assist only.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No upload, tag, or release action is performed.

Source and monitor preview metadata:
- Source type: plane_wave
- Source wavelength start: None
- Source wavelength stop: None
- Polarization: linear_x
- Incidence direction: normal
- Monitor type: phase_profile
- Observable: phase profile / far-field preview
- Monitor region: transmission plane or far-field proxy
- Monitor definitions are preview metadata; no external solver monitor is executed.

Required source inputs:
- wavelength_nm
- polarization
- incidence_direction

Required monitor inputs:
- observable
- monitor_region

Default source/monitor assumptions:
- Default to normal-incidence linear_x plane wave at 633 nm.
- Default monitor is phase-profile/far-field preview metadata.
