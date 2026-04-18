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

3. Run tests and lint:

   ```bash
   make test          # pytest -v
   make lint          # ruff check src/ tests/
   ```

4. If you changed parser behavior, update golden cases:

   ```bash
   python benchmarks/run_benchmark.py --update
   ```

   Then verify:

   ```bash
   python benchmarks/run_benchmark.py
   ```

5. Commit and push, then open a Pull Request against `main`.

## Testing

- All tests live under `tests/`.
- Use `pytest -v` for verbose output.
- Use `pytest --cov=optical_spec_agent` for coverage.
- CI runs on Python 3.11 and 3.12. Make sure your change passes on both.

## What to contribute

**Good first issues:**

- New keyword / regex patterns for parser coverage
- New golden cases for uncovered physical systems (e.g. grating, metasurface details)
- Validation rule improvements
- Documentation fixes and examples

**Needs discussion first (open an issue):**

- New structured sub-models or enum values
- LLM parser integration
- Solver adapter work (Meep, MPB, Elmer, Optiland)
- Breaking schema changes

## Commit style

- Use concise, imperative descriptions: `add RCWA solver keyword`, `fix sweep plan step extraction`.
- Keep commits focused — one logical change per commit.

## PR checklist

- [ ] Tests pass (`make test`)
- [ ] Lint clean (`make lint`)
- [ ] Golden cases updated if parser behavior changed
- [ ] New code has tests
- [ ] No unnecessary changes outside the scope of the PR

## Code of conduct

Be respectful. We're all here to build useful optical simulation tooling.
