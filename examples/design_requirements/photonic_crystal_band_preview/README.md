# Photonic crystal band preview

Chinese title: 光子晶体能带预览

Natural-language goal:

Prepare a local photonic crystal band-structure preview workflow for MPB, including lattice/material assumptions and no solver execution.

中文目标：

为 MPB 准备本地光子晶体能带预览工作流，包含晶格和材料假设，不执行求解器。

Optical intent: photonic crystal band preview

Required inputs:
- lattice_type
- period
- material_indices
- num_bands
- k_path

Default assumptions:
- Schematic periodic lattice until geometry is reviewed.
- MPB adapter preview only.
- No convergence proof or solver run.

Suggested materials:
- si
- gaas
- sio2
- air

Suggested adapter/tool path: mpb

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
- mpb_adapter_preview
- workflow_plan
- agent_trace

Limitations: Adapter preview only; no band solver execution or formal convergence proof.

Safety boundaries:

- No solver is executed by default.
- No external LLM is called by default.
- This template is preview/design-assist only.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
- No upload, tag, or release action is performed.

Source and monitor preview metadata:
- Source type: mode_source
- Source wavelength start: None
- Source wavelength stop: None
- Polarization: None
- Incidence direction: None
- Monitor type: band_structure
- Observable: band diagram preview
- Monitor region: reciprocal-space k-path
- Monitor definitions are preview metadata; no external solver monitor is executed.

Required source inputs:
- mode_index

Required monitor inputs:
- observable
- sampling

Default source/monitor assumptions:
- Treat the case as an eigenmode/band-structure preview, not a driven source simulation.
- Default monitor is band-structure metadata over a k-path scaffold.
