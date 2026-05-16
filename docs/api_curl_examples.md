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
