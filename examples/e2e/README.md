# Offline End-to-End User Journey

This directory captures an offline, local-first user journey for
`optical-spec-agent`.

It requires no network, executes no external solver, requires no external LLM,
and requires no proprietary optical software such as Zemax, Lumerical, COMSOL,
or proprietary Ansys optics tools.

No proprietary optical software is required.

The journey is evidence for the local CLI and preview contracts:

```bash
optical-spec --help
optical-spec validate examples/specs/minimal_nanoparticle.json
optical-spec parse examples/specs/minimal_nanoparticle.json --json
optical-spec adapter-list --json
optical-spec workflow-plan examples/workflows/local_preview_request.json --json
optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json
```

Outputs are preview and diagnostics artifacts. They are not production-grade
physical validation, not a formal convergence proof, and not solver-backed
correctness by default.
