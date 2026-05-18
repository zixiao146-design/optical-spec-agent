# Thin-film anti-reflection coating

Chinese title: 薄膜增透镀膜

Natural-language goal:

Design a local preview for a single-layer anti-reflection coating on glass at 550 nm, estimate the quarter-wave thickness, and inspect a wavelength sweep without running solvers.

中文目标：

为玻璃基底上的单层增透薄膜做本地预览设计，目标波长 550 nm，估算四分之一波厚度，并查看反射率随波长变化，不运行外部求解器。

Optical intent: thin film coating preview

Required inputs:
- incident_n
- substrate_n
- target_wavelength_nm
- coating_n or material choice
- wavelength_range_nm

Default assumptions:
- Normal incidence.
- Lossless constant-index preview.
- Single-layer quarter-wave helper before any validated stack model.

Suggested materials:
- sio2
- tio2
- al2o3
- glass_fused_silica_preview

Suggested adapter/tool path: preview-only; future TMM adapter candidate

Expected calculator or adapter/tool calls:
- requirements.match_template
- requirements.extract_optical_intent
- material_catalog.suggest
- example_registry.load
- agent_trace.build
- workflow_plan.preview
- adapter_preview.generate
- optics.thin_film.spectrum

Expected artifacts:
- requirement_match
- thin_film_spectrum
- quarter_wave_ar
- workflow_plan

Limitations: Sanity-checked preview formulas only; verify material constants and stack physics before conclusions.

Safety boundaries:

- No solver is executed by default.
- No external LLM is called by default.
- This template is preview/design-assist only.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No upload, tag, or release action is performed.
