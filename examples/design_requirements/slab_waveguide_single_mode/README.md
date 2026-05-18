# Slab waveguide single-mode estimate

Chinese title: 平板波导单模估计

Natural-language goal:

Estimate whether a SiN slab waveguide is likely single-mode near 1550 nm, sweep core thickness, and keep the result as a local design-assist preview.

中文目标：

估算 1550 nm 附近 SiN 平板波导是否可能单模，扫描芯层厚度，并保持为本地设计辅助预览。

Optical intent: waveguide mode preview

Required inputs:
- core_n
- cladding_n
- core_thickness_um
- wavelength_nm

Default assumptions:
- Symmetric slab-waveguide scalar V-number preview.
- Uses approximate single-mode threshold only.
- Does not solve ridge/asymmetric vector modes.

Suggested materials:
- si3n4
- sio2
- si
- air

Suggested adapter/tool path: mpb or elmer preview

Expected calculator or adapter/tool calls:
- requirements.match_template
- requirements.extract_optical_intent
- material_catalog.suggest
- example_registry.load
- agent_trace.build
- workflow_plan.preview
- adapter_preview.generate
- optics.waveguide.sweep

Expected artifacts:
- requirement_match
- waveguide_v_number_sweep
- single_mode_range
- workflow_plan

Limitations: Scalar V-number orientation only; not a mode-solver result.

Safety boundaries:

- No solver is executed by default.
- No external LLM is called by default.
- This template is preview/design-assist only.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No upload, tag, or release action is performed.
