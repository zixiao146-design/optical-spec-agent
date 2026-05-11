# Demo Artifacts

Demo artifacts show deterministic repo behavior. They are not solver results
unless a separate execution artifact explicitly records a local solver run.

## Regeneration

```bash
python scripts/regenerate_demo_outputs.py
```

By default this writes to:

```text
examples/outputs/release_demo/
```

The script generates:

- rule-based parser demo specs
- a mock/hybrid MPB-oriented spec
- an MPB adapter scaffold
- post-hoc diagnostic demo artifacts
- a `demo_manifest.json`

## Provenance

The demo generator uses local deterministic code paths only:

- no external LLM provider
- no external solver
- no Meep execution
- no network access

## Limitations

Demo artifacts are intended for onboarding and contract checks. They do not
prove simulation convergence or physical correctness.
