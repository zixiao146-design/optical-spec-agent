# Contributing to optical-spec-agent

Thanks for your interest! This guide covers how to set up, develop, and submit changes.

## Prerequisites

- Python 3.11+
- git

## Setup

```bash
git clone https://github.com/zixiao146-design/optical-spec-agent.git
cd optical-spec-agent
pip install -e ".[dev]"
```

## Development workflow

1. Create a branch from `main`:

   ```bash
   git checkout -b my-feature
   ```

2. Make your changes. Follow existing code style (line-length 100, type hints where practical).

3. Run the standard validation gate:

   ```bash
   make check
   ```

   `make check` is deterministic and local-only: pytest, key-field benchmark,
   semantic benchmark, mock LLM benchmark, workflow benchmark, docs/CLI checks,
   and artifact contract checks. It does not require Meep, MPB, Gmsh, Elmer,
   Optiland, or an external LLM provider.

   `make lint` is available for lint-focused cleanup work, but it is not the
   current CI gate. The repo still has pre-existing Ruff cleanup debt.

4. If you changed parser behavior, inspect exact benchmark drift before changing snapshots:

   ```bash
   python benchmarks/run_benchmark.py --mode exact
   ```

   Only refresh `benchmarks/golden_cases.json` after the parser drift is intentional and
   reviewable. Snapshot refreshes should be small, explicit commits:

   ```bash
   python benchmarks/run_benchmark.py --update
   python benchmarks/run_benchmark.py --mode exact
   ```

5. Commit and push, then open a Pull Request against `main`.

## Testing

- All tests live under `tests/`.
- Use `pytest -v` for verbose output.
- Use `pytest --cov=optical_spec_agent` for coverage.
- CI runs on Python 3.11 and 3.12.
- CI runs deterministic tests, parser benchmarks, semantic benchmark, and release
  engineering checks. Extended benchmark workflows remain local/mock-only.
- Real Meep execution is a manual/local gate. Ordinary CI does not require Meep.
- External MPB/Gmsh/Elmer/Optiland solver execution is not part of default CI.
- External LLM providers are not part of default CI; use the deterministic mock
  provider for parser tests.
- `make lint` runs Ruff. Treat existing lint cleanup as a separate, focused change.

## Release engineering checks

Use these when touching docs, CLI contracts, artifacts, or release notes:

```bash
make docs-check
make cli-check
make release-check
make artifact-check
python -m build
twine check dist/*
```

Do not create GitHub releases or tags from routine PR work. See
[`docs/versioning_policy.md`](docs/versioning_policy.md) and
[`docs/release_readiness_current.md`](docs/release_readiness_current.md).

## What to contribute

**Good first issues:**

- New keyword / regex patterns for parser coverage
- New golden cases for uncovered physical systems (e.g. grating, metasurface details)
- Validation rule improvements
- Documentation fixes and examples
- First-run and CLI documentation polish
- Local diagnostic report updates that do not change solver behavior
- Release engineering checks, artifact contracts, and CI documentation

**Needs discussion first (open an issue):**

- New structured sub-models or enum values
- LLM parser integration
- New solver adapters or major Meep physics/template changes
- Breaking schema changes
- Any claim that generated artifacts are production physical validation

## Commit style

- Use concise, imperative descriptions: `add RCWA solver keyword`, `fix sweep plan step extraction`.
- Keep commits focused — one logical change per commit.

## PR checklist

- [ ] Standard validation passes (`make check`)
- [ ] Lint checked if the PR is lint-focused (`make lint`)
- [ ] Exact benchmark drift reviewed if parser behavior changed
- [ ] Golden snapshots updated only when intentionally approved
- [ ] New code has tests
- [ ] Docs updated if CLI/artifact/release behavior changed
- [ ] Default tests do not require external solvers or external LLM providers
- [ ] No production validation claim was introduced
- [ ] No unnecessary changes outside the scope of the PR

## Code of conduct

Be respectful. We're all here to build useful optical simulation tooling.
