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
   make check         # pytest + key-field benchmark + semantic benchmark
   ```

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
- CI runs `pytest -q`, `python benchmarks/run_benchmark.py --mode key_fields`, and
  `python benchmarks/run_semantic_benchmark.py`.
- Real Meep execution is a manual/local gate. Ordinary CI does not require Meep.
- `make lint` runs Ruff. Treat existing lint cleanup as a separate, focused change.

## What to contribute

**Good first issues:**

- New keyword / regex patterns for parser coverage
- New golden cases for uncovered physical systems (e.g. grating, metasurface details)
- Validation rule improvements
- Documentation fixes and examples
- First-run and CLI documentation polish
- Local diagnostic report updates that do not change solver behavior

**Needs discussion first (open an issue):**

- New structured sub-models or enum values
- LLM parser integration
- New solver adapters or major Meep physics/template changes
- Breaking schema changes

## Commit style

- Use concise, imperative descriptions: `add RCWA solver keyword`, `fix sweep plan step extraction`.
- Keep commits focused — one logical change per commit.

## PR checklist

- [ ] Standard validation passes (`make check`)
- [ ] Lint checked if the PR is lint-focused (`make lint`)
- [ ] Exact benchmark drift reviewed if parser behavior changed
- [ ] Golden snapshots updated only when intentionally approved
- [ ] New code has tests
- [ ] No unnecessary changes outside the scope of the PR

## Code of conduct

Be respectful. We're all here to build useful optical simulation tooling.
