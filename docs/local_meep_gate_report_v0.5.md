# Local Meep Gate Report v0.5

This report records local/manual Meep integration evidence for the v0.5
execution harness. It is not a default CI gate and does not claim production
solver validation.

## Run Environment

- Date recorded: 2026-04-30
- Repository path: `/Users/lizixiao/Desktop/光学设计agent/optical-spec-agent`
- Meep availability command:
  `micromamba run -n meep python -c "import meep"`
- Current Python probe:
  `/Users/lizixiao/.pyenv/versions/3.11.15/Library/Frameworks/Python.framework/Versions/3.11/bin/python -c "import meep"`
- Current Python probe result: unavailable, `ModuleNotFoundError: No module named 'meep'`
- Meep environment used: micromamba env `meep`
- `meep-check --json` result:
  `available=true`, `success=true`, `schema_version=execution_result.v0.1`,
  `run_id=meep-check-20260430-085041-54bc5ce5`,
  `created_at=2026-04-30T08:50:41.088430Z`

## Smoke Gate Result

- Command: `python scripts/local_meep_integration_gate.py --mode smoke --timeout 300`
- Status: run and passed
- Run ID: `local-gate-20260430-080323-4f364986`
- Created at: `2026-04-30T08:03:23.832128Z`
- Artifact directory:
  `runs/local-gate/local-gate-20260430-080323-4f364986`
- Generated artifacts:
  `generated_script.py`, `stdout.txt`, `stderr.txt`,
  `execution_result.json`, `run_manifest.json`

Execution result summary:

```json
{
  "schema_version": "execution_result.v0.1",
  "run_id": "local-gate-20260430-080323-4f364986",
  "expected_mode": "smoke",
  "success": true,
  "available": true,
  "returncode": 0,
  "required_outputs": [],
  "missing_outputs": [],
  "outputs": {},
  "errors": []
}
```

Run manifest summary:

```json
{
  "schema_version": "execution_result.v0.1",
  "run_id": "local-gate-20260430-080323-4f364986",
  "expected_mode": "smoke",
  "command": [
    "micromamba",
    "run",
    "-n",
    "meep",
    "python",
    "runs/local-gate/local-gate-20260430-080323-4f364986/generated_script.py"
  ],
  "success": true,
  "available": true,
  "returncode": 0,
  "outputs": {},
  "required_outputs": [],
  "missing_outputs": []
}
```

## Research-Preview Gate Result

- Command:
  `python scripts/local_meep_integration_gate.py --mode research-preview --timeout 3600`
- Status: run and failed
- Timeout setting: 3600 seconds
- Final run ID: `local-gate-20260430-081054-8a37d420`
- Created at: `2026-04-30T08:10:55.523611Z`
- Artifact directory:
  `runs/local-gate/local-gate-20260430-081054-8a37d420`
- Generated artifacts:
  `generated_script.py`, `stdout.txt`, `stderr.txt`,
  `execution_result.json`, `run_manifest.json`
- `scattering_spectrum.csv`: not generated
- `postprocess_results.json`: not generated
- `scattering_spectrum.png`: not generated

Execution result summary:

```json
{
  "schema_version": "execution_result.v0.1",
  "run_id": "local-gate-20260430-081054-8a37d420",
  "expected_mode": "research_preview",
  "success": false,
  "available": true,
  "returncode": 1,
  "required_outputs": [
    "scattering_spectrum.csv",
    "postprocess_results.json"
  ],
  "missing_outputs": [
    "scattering_spectrum.csv",
    "postprocess_results.json"
  ],
  "outputs": {},
  "errors": [
    "Meep script failed with return code 1",
    "Missing required output for research_preview: scattering_spectrum.csv",
    "Missing required output for research_preview: postprocess_results.json"
  ]
}
```

Run manifest summary:

```json
{
  "schema_version": "execution_result.v0.1",
  "run_id": "local-gate-20260430-081054-8a37d420",
  "expected_mode": "research_preview",
  "success": false,
  "available": true,
  "returncode": 1,
  "outputs": {},
  "required_outputs": [
    "scattering_spectrum.csv",
    "postprocess_results.json"
  ],
  "missing_outputs": [
    "scattering_spectrum.csv",
    "postprocess_results.json"
  ]
}
```

Final failure observed in `stderr.txt`:

```text
RuntimeError: meep: simulation fields are NaN or Inf
```

The failure occurred during the research-preview reference run before output
files were written. The execution harness correctly marked the run as failed
because the process returned non-zero and the research-preview required outputs
were missing.

## PML / Cell Issue Evidence

An earlier research-preview attempt failed immediately with:

```text
RuntimeError: meep: invalid boundary absorbers for this grid_volume
```

That failure was caused by research-preview cell dimensions being too small
relative to the two PML layers. The generated film and source also extended to
or into the PML region, which is not a safe Meep geometry for this local gate.

The research-preview template was minimally adjusted to:

- make the lateral cell dimensions larger than the two PML layers,
- keep the finite film inside the PML interior,
- keep the source inside the PML interior,
- add a small lateral safety margin between the finite film/source and PML.

This fix is reasonable because PML layers are absorbing boundary regions and
should not consume the entire transverse grid or be filled by the finite source
and metal film geometry. After the fix, the PML/cell error no longer appears.

Current status: the PML/cell issue is resolved for the local gate, but the
research-preview gate still does not pass because the dispersive Au film
simulation becomes numerically unstable and produces NaN/Inf fields during the
reference run.

## Limitations

- This report is local/manual gate evidence, not a default CI result.
- Ordinary CI does not require Meep to be installed.
- The smoke gate validates that a small generated Meep script can execute
  locally; it does not validate physical correctness.
- The research-preview script is still not production-grade.
- The research-preview failure means v0.5 has an auditable execution harness,
  but not a validated, converged research-preview simulation.
- Results here do not demonstrate physical convergence, material-model
  accuracy, or publication-ready scattering observables.
- Result parsing is still an early baseline around generated JSON artifacts,
  not a full solver automation pipeline.
