# Repository Metadata

Copy-paste-ready content for GitHub settings and first issues.

---

## GitHub About (sidebar)

**Description:**

```
NL → structured spec JSON for optical simulation tasks. Rule-based parser + Pydantic validation with provenance tracking.
```

**Website:** *(leave empty for now — point to docs site when available)*

**Topics:**

```
optics
photonics
parser
pydantic
scientific-computing
simulation
specification
open-source-optics
meep
fdtd
fem
python
```

---

## First Issues

### Issue 1: Key-field benchmark with per-case threshold

**Title:** Add per-case key-field lists to all golden_cases.json entries

**Description:**
Current `key_fields` mode uses a shared `CORE_KEY_FIELDS` list. Each golden case should define its own `expected_key_fields` in `golden_cases.json` so that fitting tasks (golden-05) don't require `physical_system`, and simulation tasks can require more fields.

Steps:
- Add `expected_key_fields` to all 8 golden cases (golden-05 already has one)
- Document the expected list in `benchmarks/README.md`
- Verify with `python benchmarks/run_benchmark.py --mode key_fields`

**Labels:** `enhancement`, `good first issue`

---

### Issue 2: CLI `--format summary` human-readable output

**Title:** Add `--format summary` to CLI parse output

**Description:**
Currently `optical-spec parse` outputs raw JSON. Add a `--format summary` option that prints a concise human-readable table (field, value, status) similar to the demo tables in README.

This would make CLI demos more compelling and help users quickly scan parsed specs.

**Labels:** `enhancement`

---

### Issue 3: Add Meep-focused golden case

**Title:** Add a golden case specifically targeting Meep FDTD output fields

**Description:**
Most golden cases reference unspecified or commercial software. Add a new golden case (`golden-09`) where the input explicitly specifies Meep FDTD with full parameter detail (TFSF source, PML, mesh resolution, monitor placement), so the parsed spec is `is_executable: true` with all required simulation fields filled.

This would demonstrate that the parser can produce a Meep-ready spec and serve as the first test case for the v0.3 Meep adapter.

**Labels:** `enhancement`, `meep-adapter`

---

### Issue 4: Expand golden cases to 12

**Title:** Add 3 more golden cases: grating, coupled oscillator, bilingual edge case

**Description:**
Current 8 cases cover nanoparticle_on_film, waveguide, metasurface, and fitting. To improve parser coverage, add:

1. `golden-10`: Grating structure (Chinese) — covers `PhysicalSystem.grating`
2. `golden-11`: Coupled oscillator model (Chinese) — covers `SolverMethod.coupled_oscillator`
3. `golden-12`: Mixed Chinese-English input — tests bilingual robustness

Each case should include `expected_key_fields` and pass both benchmark modes.

**Labels:** `enhancement`

---

### Issue 5: CI integration — run benchmark in GitHub Actions

**Title:** Run golden-case benchmark in CI alongside pytest

**Description:**
The test workflow (`.github/workflows/test.yml`) runs `pytest` but not the benchmark. Add a step to run `python benchmarks/run_benchmark.py --mode all` in CI so that parser regressions are caught automatically.

This provides a second signal: pytest checks code-level correctness, benchmark checks parser output stability.

**Labels:** `ci`, `good first issue`
