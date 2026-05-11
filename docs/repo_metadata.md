# Repository Metadata

Copy-paste-ready content for GitHub settings and focused follow-up issues.

---

## GitHub About

**Description:**

```text
NL optical task → validated spec JSON → solver input scaffolds → optional Meep artifacts.
```

**Website:** leave empty until a docs site exists.

**Topics:**

```text
optics
photonics
meep
fdtd
mpb
gmsh
elmer
ray-tracing
pydantic
scientific-computing
simulation
specification
python
open-source-optics
```

---

## Suggested Issues

### Issue 1: Add a README hero workflow transcript

**Title:** Add a checked-in transcript for the README hero workflow

**Description:**
The README now documents the main product path:

```text
natural language optical task -> validated spec JSON -> Meep script -> optional execution artifacts
```

Add a small checked-in transcript or example output under `examples/outputs/` that shows the
commands and key output files from the hero workflow without requiring Meep to be installed.

Acceptance criteria:

- Shows `optical-spec parse ... --output outputs/hero_spec.json`
- Shows `optical-spec validate outputs/hero_spec.json`
- Shows `optical-spec meep-generate ... --mode research-preview`
- Clearly marks `meep-run` as optional/local

**Labels:** `documentation`, `good first issue`

---

### Issue 2: Add a docs index for Meep local diagnostics

**Title:** Add a short index page for local Meep diagnostic reports

**Description:**
There are several local/manual Meep diagnostic reports for v0.5 and v0.6. Add one short index
page that explains which report to read first and what each report proves or does not prove.

Suggested file:

```text
docs/meep_diagnostics_index.md
```

Acceptance criteria:

- Links to the v0.5 local gate report
- Links to stability matrix, physical pre-study, candidate hardening, observable diagnostics,
  and mesh/monitor diagnostics
- Repeats that these are local/manual diagnostics, not production validation

**Labels:** `documentation`, `meep`

---

### Issue 3: Document exact snapshot review workflow

**Title:** Document the exact benchmark snapshot review workflow

**Description:**
The CI gate intentionally runs key-field and semantic benchmarks, not automatic snapshot
updates. Add a short section to `benchmarks/README.md` explaining how to review exact snapshot
drift safely.

Acceptance criteria:

- Shows `python benchmarks/run_benchmark.py --mode exact`
- Says not to run `--update` until drift is reviewed
- Explains that snapshot refreshes should be separate, explicit commits

**Labels:** `documentation`, `benchmark`

---

### Issue 4: Add a no-Meep smoke check for generated research-preview scripts

**Title:** Add a no-Meep syntax smoke check command for generated scripts

**Description:**
The project can generate Meep scripts even when Meep is not installed. Add a documented command
or helper that validates generated script syntax with `py_compile` without attempting to import
or run Meep.

Acceptance criteria:

- Does not require Meep
- Does not execute a simulation
- Fits the hero workflow as a lightweight confidence check

**Labels:** `developer-experience`, `meep`

---

### Issue 5: Keep GitHub metadata aligned with current release status

**Title:** Review GitHub About and README release status before v0.6 release

**Description:**
Before cutting a future v0.6 release, review the GitHub About description, README current scope,
and release notes so they distinguish:

- v0.5.0 released execution harness
- v0.6 local/manual diagnostics
- what is still not production-grade solver automation

**Labels:** `release`, `documentation`

---

### Issue 6: Clean existing Ruff lint debt

**Title:** Clean existing Ruff findings and promote `make lint` to a required gate

**Description:**
`make lint` now runs `ruff check src/ tests/`, but the repository has pre-existing Ruff
findings such as unused imports, unused local variables, and a few unnecessary f-string
prefixes. Clean these in a focused PR without changing parser behavior or Meep physics.

Acceptance criteria:

- `make lint` passes
- No parser benchmark snapshots are changed
- `make check` still passes
- CONTRIBUTING can promote lint back to a required PR checklist item

**Labels:** `cleanup`, `developer-experience`
