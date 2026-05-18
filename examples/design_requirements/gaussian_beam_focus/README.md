# Gaussian beam focus preview

Chinese title: 高斯光束聚焦预览

Natural-language goal:

Preview Gaussian beam propagation and thin-lens focusing for a 1064 nm beam, including waist, Rayleigh range, and focused spot estimate without calling external tools.

中文目标：

预览 1064 nm 高斯光束的传播和薄透镜聚焦，给出光腰、瑞利长度和焦斑估计，不调用外部工具。

Optical intent: gaussian beam propagation preview

Required inputs:
- wavelength_nm
- input_waist_um
- propagation_range_mm
- focal_length_mm

Default assumptions:
- Fundamental paraxial Gaussian beam.
- Ideal thin lens.
- No aberration, clipping, or vector-field effects.

Suggested materials:
- air
- glass_bk7_preview
- glass_fused_silica_preview

Suggested adapter/tool path: local Gaussian beam calculator; no solver adapter required

Expected calculator or adapter/tool calls:
- requirements.match_template
- requirements.extract_optical_intent
- material_catalog.suggest
- example_registry.load
- agent_trace.build
- workflow_plan.preview
- adapter_preview.generate
- optics.gaussian_beam.series

Expected artifacts:
- requirement_match
- gaussian_beam_series
- gaussian_focus
- workflow_plan

Limitations: Paraxial Gaussian formulas only; not a vector diffraction or full lens validation.

Safety boundaries:

- No solver is executed by default.
- No external LLM is called by default.
- This template is preview/design-assist only.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No upload, tag, or release action is performed.

Source and monitor preview metadata:
- Source type: gaussian_beam
- Source wavelength start: None
- Source wavelength stop: None
- Polarization: scalar_paraxial
- Incidence direction: z_plus
- Monitor type: focal_spot
- Observable: beam radius and focused waist preview
- Monitor region: propagation axis / focal plane
- Monitor definitions are preview metadata; no external solver monitor is executed.

Required source inputs:
- wavelength_nm
- beam_waist_um

Required monitor inputs:
- observable
- monitor_region

Default source/monitor assumptions:
- Default to a 1064 nm scalar Gaussian beam when not specified.
- Default waist is 10 um for propagation preview.
- Default monitor is focal spot / beam radius preview.
