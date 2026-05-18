# Local Agent API Examples

These fixtures document the current local Agent API response shapes for a
future Agent Studio frontend. They are example request/response JSON files, not
a frontend implementation.

Current `api_contract_version`: 0.1.

## Guarantees

- No network access is required.
- No external solver execution is performed.
- No external LLM call is required.
- No proprietary solver is required.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.

## Fixture manifest

`frontend_fixture_manifest.json` lists each fixture with:

- fixture name
- endpoint
- method
- request file when applicable
- response file
- `no_network: true`
- `external_solver_executed: false`
- `external_llm_required: false`
- `proprietary_solver_required: false`
- `production_grade_validation_claimed: false`
- `formal_convergence_proof_claimed: false`

The manifest includes successful responses and stable error fixtures for
schema, heuristic parse, invalid specs, unsupported adapters, invalid workflow
requests, and disabled external LLM parsing. Future frontend work should use
these fixtures for local mock data and contract checks before any full UI
implementation begins.

The manifest also includes Material Library and Agent Collaboration fixtures:

- `materials_response.json`
- `material_detail_sio2_response.json`
- `material_suggestion_request.json`
- `material_suggestion_response.json`
- `agent_trace_request_nanoparticle.json`
- `agent_trace_response_nanoparticle.json`
- `examples_response.json`
- `example_detail_nanoparticle_response.json`
- `example_agent_trace_nanoparticle_response.json`
- `agent_session_request_nanoparticle.json`
- `agent_session_response_nanoparticle.json`
- `agent_session_tool_ledger_response.json`
- `agent_session_error_empty_goal_response.json`
- `tool_capabilities_response.json`
- `backend_capability_report_response.json`
- `design_case_cross_checks_response.json`
- `design_requirements_response.json`
- `design_requirement_thin_film_response.json`
- `design_requirement_match_thin_film_request.json`
- `design_requirement_match_thin_film_response.json`
- `design_requirement_match_nanoparticle_zh_request.json`
- `design_requirement_match_nanoparticle_zh_response.json`
- `thin_film_request.json`
- `thin_film_response.json`
- `thin_film_spectrum_request.json`
- `thin_film_spectrum_response.json`
- `quarter_wave_ar_request.json`
- `quarter_wave_ar_response.json`
- `paraxial_lens_request.json`
- `paraxial_lens_response.json`
- `paraxial_system_request.json`
- `paraxial_system_response.json`
- `two_lens_relay_request.json`
- `two_lens_relay_response.json`
- `gaussian_beam_request.json`
- `gaussian_beam_response.json`
- `gaussian_beam_series_request.json`
- `gaussian_beam_series_response.json`
- `gaussian_beam_focus_request.json`
- `gaussian_beam_focus_response.json`
- `waveguide_estimate_request.json`
- `waveguide_estimate_response.json`
- `waveguide_sweep_request.json`
- `waveguide_sweep_response.json`
- `waveguide_single_mode_range_request.json`
- `waveguide_single_mode_range_response.json`

These fixtures are local preview/design-assist data only. They do not perform
external material database lookup, solver execution, external LLM calls,
uploads, tags, or releases.

The Agent Command Center fixtures exercise `POST /api/agent-session` and show
how a natural language goal becomes optical intent, a design case, local plan
steps, sub-agent trace, permission gates, a tool-call ledger, local artifacts,
evidence, and next actions. The tool capabilities and optical calculator
fixtures show backend tool-call reality and preview/design-assist calculations.
Calculator fixtures include `quality`, `warnings`, `assumptions`, and
`limitations` fields; `quality.quality_level` is `sanity_checked_preview`.
Backend capability report fixtures show package status, sub-agent execution,
internal tool calls, calculator reference-case status, design-case cross-checks,
design requirement template status, and blocked external actions. Design
requirement fixtures show deterministic natural-language goal matching and the
resulting optical language summary without external LLM calls.
They preserve the same no-solver, no-external-LLM, no-upload, no-tag, and
no-release boundaries.

`scripts/check_api_fixtures.py` compares these fixtures with live FastAPI
`TestClient` response top-level shapes. `scripts/smoke_agent_api.sh` exercises
all current `/api/*` endpoints without starting a background server. Both
scripts preserve the no-network, no-solver, no-external-LLM, no-upload,
no-tag, and no-release boundaries.
