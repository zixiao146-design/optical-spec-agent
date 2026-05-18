# Local Agent API Curl Examples

These examples are for local frontend handoff and API smoke testing. They do not execute solvers,
and they also do not call an external LLM, do not publish packages, and do not require external network access beyond the local API server.

Start the API first:

```bash
python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000
```

## Health

```bash
curl http://127.0.0.1:8000/api/health
```

## Version

```bash
curl http://127.0.0.1:8000/api/version
```

## Adapters

```bash
curl http://127.0.0.1:8000/api/adapters
```

## Schema

```bash
curl http://127.0.0.1:8000/api/schema
```

## Parse

```bash
curl -X POST http://127.0.0.1:8000/api/parse \
  -H "Content-Type: application/json" \
  --data @examples/api/parse_request_heuristic.json
```

## Validate

```bash
curl -X POST http://127.0.0.1:8000/api/validate \
  -H "Content-Type: application/json" \
  --data @examples/api/validate_request_minimal.json
```

## Workflow Plan

```bash
curl -X POST http://127.0.0.1:8000/api/workflow-plan \
  -H "Content-Type: application/json" \
  --data @examples/api/workflow_plan_request.json
```

## Adapter Preview

```bash
curl -X POST http://127.0.0.1:8000/api/adapter-preview \
  -H "Content-Type: application/json" \
  --data @examples/api/adapter_preview_gmsh_request.json
```

## Validation Evidence

```bash
curl http://127.0.0.1:8000/api/validation-evidence
```

## Readiness

```bash
curl http://127.0.0.1:8000/api/readiness
```

All examples are local, synchronous, preview-first API calls intended for a
future frontend developer to copy while building against `api_contract_version`
0.1.

## Material Library And Agent Trace

```bash
curl http://127.0.0.1:8000/api/examples
curl http://127.0.0.1:8000/api/examples/nanoparticle_plasmonics
curl -X POST http://127.0.0.1:8000/api/examples/nanoparticle_plasmonics/agent-trace \
  -H "Content-Type: application/json" \
  --data '{}'
curl http://127.0.0.1:8000/api/materials
curl http://127.0.0.1:8000/api/materials/sio2
curl -X POST http://127.0.0.1:8000/api/materials/suggest \
  -H "Content-Type: application/json" \
  --data @examples/api/material_suggestion_request.json
curl -X POST http://127.0.0.1:8000/api/agent-trace \
  -H "Content-Type: application/json" \
  --data @examples/api/agent_trace_request_nanoparticle.json
curl -X POST http://127.0.0.1:8000/api/agent-session \
  -H "Content-Type: application/json" \
  --data @examples/api/agent_session_request_nanoparticle.json
curl http://127.0.0.1:8000/api/tool-capabilities
curl -X POST http://127.0.0.1:8000/api/optics/thin-film \
  -H "Content-Type: application/json" \
  --data @examples/api/thin_film_request.json
curl -X POST http://127.0.0.1:8000/api/optics/thin-film-spectrum \
  -H "Content-Type: application/json" \
  --data @examples/api/thin_film_spectrum_request.json
curl -X POST http://127.0.0.1:8000/api/optics/quarter-wave-ar \
  -H "Content-Type: application/json" \
  --data @examples/api/quarter_wave_ar_request.json
curl -X POST http://127.0.0.1:8000/api/optics/paraxial-lens \
  -H "Content-Type: application/json" \
  --data @examples/api/paraxial_lens_request.json
curl -X POST http://127.0.0.1:8000/api/optics/paraxial-system \
  -H "Content-Type: application/json" \
  --data @examples/api/paraxial_system_request.json
curl -X POST http://127.0.0.1:8000/api/optics/two-lens-relay \
  -H "Content-Type: application/json" \
  --data @examples/api/two_lens_relay_request.json
curl -X POST http://127.0.0.1:8000/api/optics/gaussian-beam \
  -H "Content-Type: application/json" \
  --data @examples/api/gaussian_beam_request.json
curl -X POST http://127.0.0.1:8000/api/optics/gaussian-beam-series \
  -H "Content-Type: application/json" \
  --data @examples/api/gaussian_beam_series_request.json
curl -X POST http://127.0.0.1:8000/api/optics/gaussian-beam-focus \
  -H "Content-Type: application/json" \
  --data @examples/api/gaussian_beam_focus_request.json
curl -X POST http://127.0.0.1:8000/api/optics/waveguide-estimate \
  -H "Content-Type: application/json" \
  --data @examples/api/waveguide_estimate_request.json
curl -X POST http://127.0.0.1:8000/api/optics/waveguide-sweep \
  -H "Content-Type: application/json" \
  --data @examples/api/waveguide_sweep_request.json
curl -X POST http://127.0.0.1:8000/api/optics/waveguide-single-mode-range \
  -H "Content-Type: application/json" \
  --data @examples/api/waveguide_single_mode_range_request.json
```

The Example Gallery and material examples use local repo files and the local
preview material catalog only. The agent-trace examples render a deterministic
Agent Trace Timeline. The agent-session example renders an Agent Command Center
task session with permission gates, a tool-call ledger, and local artifacts.
Tool capabilities and optical calculator examples are backend reality checks
and design-assist previews. These examples do not call an external LLM, run
solvers, upload packages, or create tags/releases.
