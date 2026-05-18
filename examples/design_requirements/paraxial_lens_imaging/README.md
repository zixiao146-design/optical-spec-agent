# Paraxial lens imaging preview

Chinese title: 近轴透镜成像预览

Natural-language goal:

Preview a simple lens imaging or two-lens relay design using ABCD matrices, then produce a local ray-optics workflow without running Optiland.

中文目标：

使用 ABCD 矩阵预览简单透镜成像或双透镜中继设计，然后生成本地光线光学工作流，不运行 Optiland。

Optical intent: lens ray tracing preview

Required inputs:
- focal_length_mm
- object_distance_mm
- lens_separation_mm optional
- wavelength optional

Default assumptions:
- Ideal thin lenses.
- First-order paraxial model.
- No aberration, aperture stop, or material dispersion model.

Suggested materials:
- glass_bk7_preview
- glass_fused_silica_preview
- air

Suggested adapter/tool path: optiland

Expected calculator or adapter/tool calls:
- requirements.match_template
- requirements.extract_optical_intent
- material_catalog.suggest
- example_registry.load
- agent_trace.build
- workflow_plan.preview
- adapter_preview.generate
- optics.paraxial.two_lens_relay

Expected artifacts:
- requirement_match
- paraxial_system
- two_lens_relay
- adapter_preview

Limitations: First-order paraxial preview only; not ray-trace validation.

Safety boundaries:

- No solver is executed by default.
- No external LLM is called by default.
- This template is preview/design-assist only.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No upload, tag, or release action is performed.
